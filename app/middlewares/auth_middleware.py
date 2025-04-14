from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.routes.auth import get_current_user
from app.database import get_db
from app.models.models import User
# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "DEFAULT_SECRET_KEY")
ALGORITHM = "HS256"

# OAuth2 scheme untuk mendapatkan token dari header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Fungsi untuk verifikasi token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": username, "role": role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Middleware untuk memeriksa apakah user memiliki role tertentu
def role_required(allowed_roles: list):
    def decorator(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        db_user = db.query(User).filter(User.username == user["username"]).first()

        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        if db_user.role == "customer" and not db_user.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account is pending verification")

        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission")

        return user
    return decorator

