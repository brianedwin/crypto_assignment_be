from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

# Kunci AES harus panjang 32 byte (256 bit)
SECRET_KEY = os.getenv("AES_SECRET_KEY", "mybank_super_secure_key").encode()

# Fungsi untuk menghasilkan kunci AES dari SECRET_KEY
def derive_key(salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(SECRET_KEY)

# Fungsi untuk mengenkripsi data menggunakan AES-256 dengan PKCS7 padding
def encrypt_data(data: str) -> str:
    salt = os.urandom(16)  # Salt acak
    key = derive_key(salt)
    iv = os.urandom(16)  # Inisialisasi vektor (IV)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Gunakan PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Gabungkan salt, IV, dan hasil enkripsi, lalu encode ke base64
    return base64.b64encode(salt + iv + encrypted_data).decode()

# Fungsi untuk mendekripsi data terenkripsi
def decrypt_data(encrypted_data: str) -> str:
    try:
        encrypted_data = base64.b64decode(encrypted_data)
    except Exception as e:
        raise ValueError("Transaction integrity check failed")
    
    salt = encrypted_data[:16]  # Ambil salt
    iv = encrypted_data[16:32]  # Ambil IV
    ciphertext = encrypted_data[32:]  # Ambil data terenkripsi

    key = derive_key(salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Hapus padding PKCS7
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()

