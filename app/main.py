from fastapi import FastAPI
from app.routes import auth
from app.database import engine
from app.models import models
from fastapi.middleware.cors import CORSMiddleware
from app.routes import protected, admin, employee, customer, transactions

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",  
    "https://dwinson-csm.duckdns.org" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tambahkan Router
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(admin.router)
app.include_router(employee.router)
app.include_router(customer.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {"message": "Welcome to MyBank API"}

