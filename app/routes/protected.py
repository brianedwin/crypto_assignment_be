from fastapi import APIRouter, Depends
from app.middlewares.auth_middleware import verify_token, role_required


router = APIRouter(prefix="/protected", tags=["Protected"])

# Endpoint yang bisa diakses oleh semua user yang login
@router.get("/profile")
def get_user_profile(user: dict = Depends(role_required(["customer", "employee", "admin"]))):
    return {"message": "Welcome to your profile!", "username": user["username"], "role": user["role"]}

# Endpoint yang hanya bisa diakses oleh Bank Employee
@router.get("/customer-transactions")
def get_all_customer_transactions(user: dict = Depends(role_required(["employee"]))):
    return {"message": "Access granted: You can view all customer transactions"}

# Endpoint yang hanya bisa diakses oleh Admin
@router.get("/manage-employees")
def manage_employees(user: dict = Depends(role_required(["admin"]))):
    return {"message": "Access granted: You can manage bank employees"}
