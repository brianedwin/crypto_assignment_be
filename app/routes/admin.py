from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import pyotp

from app.database import get_db
from app.models.models import User
from app.middlewares.auth_middleware import role_required
from app.schemas.user import UserCreate

router = APIRouter(prefix="/admin", tags=["Admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fungsi Generate OTP Secret
def generate_otp_secret():
    return pyotp.random_base32()

@router.post("/create-employee")
def create_employee(user: UserCreate, db: Session = Depends(get_db), admin: dict = Depends(role_required(["admin"]))):
    # Cek apakah username sudah ada
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Generate OTP Secret untuk Employee
    otp_secret = generate_otp_secret()

    # Buat akun Bank Employee
    new_employee = User(
        full_name=user.full_name,
        username=user.username,
        password=hashed_password,
        id_number=user.id_number,
        role="employee",
        otp_secret=otp_secret
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Bank Employee account created successfully", "username": user.username}

# GET - Melihat daftar Employee
@router.get("/get-employees")
def get_all_employees(db: Session = Depends(get_db), admin: dict = Depends(role_required(["admin"]))):
    employees = db.query(User).filter(User.role == "employee").all()
    return {"employees": [{"username": emp.username, "full_name": emp.full_name} for emp in employees]}

# DELETE - Menghapus Employee
@router.delete("/delete-employee")
def delete_employee(username: str, db: Session = Depends(get_db), admin: dict = Depends(role_required(["admin"]))):
    employee = db.query(User).filter(User.username == username, User.role == "employee").first()

    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": f"Employee {username} has been deleted successfully"}
