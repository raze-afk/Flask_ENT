from app import create_app, db
from app.models import User
from cryptography.fernet import Fernet
import os
import base64
from app.encryption_utils import *

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

