# encryption_utils.py
from cryptography.fernet import Fernet
import os
import base64

# Chemin vers le fichier de clé

FERNET_KEY = os.environ.get('FERNET_KEY', b'Y6ePPqintYMQTz2p4oFDssUz4ilVPptrbNpPkIxkSoE=')

# Initialiser Fernet avec la clé
cipher_suite = Fernet(FERNET_KEY)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(token):
    return cipher_suite.decrypt(token).decode()

