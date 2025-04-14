import hashlib
import hmac
import os

# Gunakan kunci rahasia untuk HMAC
SIGNATURE_SECRET = os.getenv("SIGNATURE_SECRET", "mybank_signature_secret").encode()

# Fungsi untuk membuat tanda tangan digital (HMAC)
def create_signature(transaction_data: str) -> str:
    signature = hmac.new(SIGNATURE_SECRET, transaction_data.encode(), hashlib.sha256).hexdigest()
    return signature

# Fungsi untuk memverifikasi tanda tangan digital
def verify_signature(transaction_data: str, signature: str) -> bool:
    expected_signature = create_signature(transaction_data)
    return hmac.compare_digest(expected_signature, signature)

