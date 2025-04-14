from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship
from decimal import Decimal
from datetime import datetime
from app.config import Base
from app.utils.encryption import encrypt_data, decrypt_data

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Disimpan dalam bentuk hash
    id_number = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)  # "customer", "employee", "admin"
    otp_secret = Column(String, unique=True, nullable=True)
    is_verified = Column(Boolean, default=False)
    balance = Column(Numeric(precision=18, scale=2), nullable=False, default=Decimal('0.00'))

    # Relasi transaksi sebagai pengirim
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_id", back_populates="sender")

    # Relasi transaksi sebagai penerima
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_id", back_populates="receiver")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_encrypted = Column(String, nullable=False)  # Simpan jumlah dalam bentuk terenkripsi
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    signature = Column(String, nullable=False)

    # Hubungan ke User sebagai pengirim
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_transactions")

    # Hubungan ke User sebagai penerima
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_transactions")

    # Properti untuk mendekripsi jumlah transaksi saat diakses
    @property
    def amount(self):
        if self.amount_encrypted:  # Cek apakah data tidak kosong
            return Decimal(decrypt_data(self.amount_encrypted))
        return 0.0  # Jika tidak ada data, kembalikan 0

    @amount.setter
    def amount(self, value):
        self.amount_encrypted = encrypt_data(str(Decimal(value).quantize(Decimal('0.01'))))
