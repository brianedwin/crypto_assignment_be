import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import pyotp
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.models.models import User
from app.schemas.user import UserCreate, UserLogin

# Load environment variables
load_dotenv()

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY", "DEFAULT_SECRET_KEY")  # Ambil dari .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Auth Router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Fungsi Hashing Password
def hash_password(password: str):
    return pwd_context.hash(password)

# Fungsi Verifikasi Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fungsi Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Fungsi Generate OTP Secret
def generate_otp_secret():
    return pyotp.random_base32()

# REGISTER USER
@router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Cek apakah username sudah ada
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    # Hash password
    hashed_password = hash_password(user.password)

    # Generate OTP Secret
    otp_secret = generate_otp_secret()

    # Simpan user ke database
    new_user = User(
        full_name=user.full_name,
        username=user.username,
        password=hashed_password,
        id_number=user.id_number,
        role="customer",  # Default sebagai customer
        otp_secret=otp_secret  # Simpan OTP secret ke database
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "otp_secret": otp_secret}


# CUSTOMER LOGIN
@router.post("/customer-login", response_model=dict)
def customer_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.role == "customer").first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not db_user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account is pending verification by a bank employee")
    # Verifikasi OTP
    if not db_user.otp_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not set up for this account")

    totp = pyotp.TOTP(db_user.otp_secret)
    if not totp.verify(user.otp_code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP code")

    # Buat token JWT
    access_token = create_access_token({"sub": db_user.username, "role": db_user.role})

    return {"access_token": access_token, "token_type": "bearer", "role": db_user.role}

# EMPLOYEE LOGIN
@router.post("/employee-login", response_model=dict)
def employee_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.role == "employee").first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verifikasi OTP
    if not db_user.otp_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not set up for this account")

    totp = pyotp.TOTP(db_user.otp_secret)
    if not totp.verify(user.otp_code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP code")

    # Buat token JWT
    access_token = create_access_token({"sub": db_user.username, "role": db_user.role})

    return {"access_token": access_token, "token_type": "bearer"}

# ADMIN LOGIN
@router.post("/admin-login", response_model=dict)
def admin_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.role == "admin").first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Verifikasi OTP
    if not db_user.otp_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not set up for this account")

    totp = pyotp.TOTP(db_user.otp_secret)
    if not totp.verify(user.otp_code):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid OTP code")

    # Buat token JWT
    access_token = create_access_token({"sub": db_user.username, "role": db_user.role})

    return {"access_token": access_token, "token_type": "bearer"}

# OAuth2 scheme untuk mendapatkan token dari header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Fungsi untuk memverifikasi dan mendekode token JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return {"username": user.username, "role": user.role, "role": user.role}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

