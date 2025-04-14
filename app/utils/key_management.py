import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# Path ke RSA Private Key
PRIVATE_KEY_PATH = "~/mybank-backend/rsa_private.pem"

# Fungsi untuk mendekripsi AES Key
def decrypt_aes_key():
    try:
        # Baca RSA Private Key
        with open(PRIVATE_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Baca AES Key terenkripsi dari file
        with open(os.getenv("ENCRYPTED_AES_KEY"), "rb") as enc_file:
            encrypted_aes_key = enc_file.read()

        # Dekripsi AES Key
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return aes_key

    except Exception as e:
        print(f"Error decrypting AES key: {e}")
        return None

