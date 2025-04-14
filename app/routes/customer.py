from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.models import User
from app.middlewares.auth_middleware import role_required
from app.schemas.user import UserUpdatePassword

router = APIRouter(prefix="/customer", tags=["Customer"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fungsi untuk hash password baru
def hash_password(password: str):
    return pwd_context.hash(password)

# PATCH - Customer Mengubah Password
@router.patch("/update-password")
def update_customer_password(user_update: UserUpdatePassword, db: Session = Depends(get_db), customer: dict = Depends(role_required(["customer"]))):
    db_user = db.query(User).filter(User.username == customer["username"]).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Verifikasi password lama
    if not pwd_context.verify(user_update.old_password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")

    # Update password baru
    db_user.password = hash_password(user_update.new_password)
    db.commit()

    return {"message": "Password updated successfully"}

