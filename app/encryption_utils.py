# encryption_utils.py
from cryptography.fernet import Fernet
import os
import base64

# Chemin vers le fichier de clé
key_file = '../secret.key'

# Générer une nouvelle clé et la sauvegarder dans un fichier si elle n'existe pas
if not os.path.exists(key_file):
    key = Fernet.generate_key()  # Génère une clé de 32 bytes
    with open(key_file, 'wb') as f:
        f.write(key)
else:
    with open(key_file, 'rb') as f:
        key = f.read()

# Initialiser Fernet avec la clé
cipher_suite = Fernet(key)

def encrypt_data(data):
    encrypted = cipher_suite.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted).decode()

def decrypt_data(token):
    encrypted = base64.urlsafe_b64decode(token.encode())
    return cipher_suite.decrypt(encrypted).decode()

