from app import create_app, db
from app.models import User
from cryptography.fernet import Fernet
import os
import base64

# Chemin vers le fichier de clé
key_file = 'secret.key'

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

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Vérifiez si un utilisateur administrateur existe déjà
        admin_user = User.query.filter_by(status='admin').first()
        if not admin_user:
            # Créez un nouvel utilisateur administrateur avec les données chiffrées
            new_admin = User(
                nom=encrypt_data('Admin'),
                prenom=encrypt_data('Admin'),
                mail=encrypt_data('admin@example.com'),
                status='admin'
            )
            new_admin.set_password('adminpassword')  # Définissez un mot de passe pour l'administrateur
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin_user()

