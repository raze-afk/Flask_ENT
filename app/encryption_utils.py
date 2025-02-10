# encryption_utils.py
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.environ.get('FERNET_KEY')

# If FERNET_KEY is not set, generate a new key and set it
if not FERNET_KEY:
    FERNET_KEY = Fernet.generate_key().decode()  # Generate key and decode to string
    os.environ['FERNET_KEY'] = FERNET_KEY
    print("Generated new key:", FERNET_KEY)

# Initialiser Fernet avec la clé
cipher_suite = Fernet(FERNET_KEY.encode())

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(token):
    return cipher_suite.decrypt(token).decode()
