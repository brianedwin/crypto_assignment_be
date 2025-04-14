from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.middlewares.auth_middleware import role_required

router = APIRouter(prefix="/employee", tags=["Employee"])

# GET - Melihat daftar Customer yang belum diverifikasi
@router.get("/pending-customers")
def get_pending_customers(db: Session = Depends(get_db), employee: dict = Depends(role_required(["employee"]))):
    pending_customers = db.query(User).filter(User.role == "customer", User.is_verified == False).all()
    return {"pending_customers": [{"username": user.username, "full_name": user.full_name} for user in pending_customers]}

# POST - Employee Approve/Reject Customer
@router.post("/verify-customer")
def verify_customer(username: str, approve: bool, db: Session = Depends(get_db), employee: dict = Depends(role_required(["employee"]))):
    customer = db.query(User).filter(User.username == username, User.role == "customer").first()
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    if approve:
        customer.is_verified = True
        db.commit()
        return {"message": f"Customer {username} has been approved"}
    else:
        db.delete(customer)
        db.commit()
        return {"message": f"Customer {username} has been rejected"}

