from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging
from decimal import Decimal

from app.database import get_db
from app.models.models import User, Transaction
from app.middlewares.auth_middleware import role_required
from app.schemas.transaction import TransferRequest
from app.utils.signature import create_signature, verify_signature
from app.utils.encryption import encrypt_data, decrypt_data

# Inisialisasi logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ✅ Transfer uang antar pengguna
@router.post("/transfer")
def transfer_money(
    transfer: TransferRequest, 
    db: Session = Depends(get_db), 
    customer: dict = Depends(role_required(["customer"]))
):
    sender = db.query(User).filter(User.username == customer["username"]).with_for_update().first()
    receiver = db.query(User).filter(User.username == transfer.receiver_username).first()

    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    if sender.balance < transfer.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

    try:
        # Pastikan waktu transaksi dicatat sebelum membuat tanda tangan
        transaction_time = datetime.utcnow().isoformat(timespec="milliseconds")

        # Enkripsi jumlah transaksi
        encrypted_amount = encrypt_data(str(transfer.amount))

        print("Encrypted Amount with AES:", encrypted_amount)

        # Format data transaksi untuk ditandatangani
        transaction_data = f"{sender.id}:{receiver.id}:{transfer.amount}:{transaction_time}"
        signature = create_signature(transaction_data)

        # Update saldo pengirim & penerima
        sender.balance -= Decimal(transfer.amount)
        receiver.balance += Decimal(transfer.amount)

        # Simpan transaksi dengan data yang sudah terenkripsi
        transaction = Transaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount_encrypted=encrypted_amount,
            transaction_type="transfer",
            created_at=datetime.fromisoformat(transaction_time),
            signature=signature
        )
        db.add(transaction)

        # Commit perubahan
        db.commit()

        return {"message": "Transfer successful", "new_balance": sender.balance}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Transaction Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transaction failed. Please try again."
        )


# ✅ Melihat riwayat transaksi pengguna yang sedang login
@router.get("/history")
def get_transaction_history(
    db: Session = Depends(get_db),
    customer: dict = Depends(role_required(["customer"]))
):
    user = db.query(User).filter(User.username == customer["username"]).first()

    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)
    ).order_by(Transaction.created_at.desc()).all()

    return {
        "transactions": [
            {
                "id": tx.id,
                "sender": tx.sender.username,
                "receiver": tx.receiver.username,
                "amount": decrypt_data(tx.amount_encrypted),  # Akan otomatis didekripsi
                "transaction_type": tx.transaction_type,
                "created_at": tx.created_at
            }
            for tx in transactions
        ]
    }


# ✅ **Melihat riwayat transaksi customer (untuk Bank Employee)**
@router.get("/history/{customer_username}")
def get_customer_transaction_history(
    customer_username: str,
    db: Session = Depends(get_db),
    employee: dict = Depends(role_required(["employee"]))
):
    user = db.query(User).filter(User.username == customer_username, User.role == "customer").first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)
    ).order_by(Transaction.created_at.desc()).all()

    return {
        "transactions": [
            {
                "id": tx.id,
                "sender": tx.sender.username,
                "receiver": tx.receiver.username,
                "amount": decrypt_data(tx.amount_encrypted),  # Otomatis didekripsi
                "transaction_type": tx.transaction_type,
                "created_at": tx.created_at
            }
            for tx in transactions
        ]
    }


# ✅ Cek transaksi customer dengan validasi tanda tangan digital
@router.get("/customer-transactions")
def get_customer_transactions(
    db: Session = Depends(get_db), 
    customer: dict = Depends(role_required(["customer"]))
):
    user = db.query(User).filter(User.username == customer["username"]).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    transactions = db.query(Transaction).filter(
        (Transaction.sender_id == user.id) | (Transaction.receiver_id == user.id)
    ).order_by(Transaction.created_at.desc()).all()

    if not transactions:
        return {"message": "No transactions found."}

    transaction_list = []
    for txn in transactions:
        if not txn.created_at:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Transaction timestamp missing")

        try:
            # ✅ Tangani jika data terenkripsi tidak valid
            amount_decrypted = decrypt_data(txn.amount_encrypted)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction integrity check failed")


        # Dekripsi jumlah transaksi sebelum verifikasi tanda tangan
        amount_decrypted = decrypt_data(txn.amount_encrypted)

        # Format ulang data transaksi untuk verifikasi
        transaction_time = txn.created_at.isoformat(timespec="milliseconds")
        transaction_data = f"{txn.sender_id}:{txn.receiver_id}:{amount_decrypted}:{transaction_time}"

        # Verifikasi tanda tangan
        if not verify_signature(transaction_data, txn.signature):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transaction integrity check failed")

        transaction_list.append({
            "id": txn.id,
            "sender": txn.sender.username,
            "receiver": txn.receiver.username,
            "amount": amount_decrypted,
            "transaction_type": txn.transaction_type,
            "created_at": txn.created_at
        })

    return {"transactions": transaction_list}

