from pydantic import BaseModel, condecimal
from decimal import Decimal

class TransferRequest(BaseModel):
    receiver_username: str
    amount: condecimal(gt=0, decimal_places=2)  # Pastikan amount > 0 dan memiliki 2 angka desimal

