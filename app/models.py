from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import os
from . import db
from app.encryption_utils import *

# Table d'association pour la relation plusieurs-à-plusieurs entre Classe et User
classe_eleve = db.Table('classe_eleve',
    db.Column('classe_id', db.Integer, db.ForeignKey('classe.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), unique=True, nullable=False)
    mdp = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    cours_crees = db.relationship('Cours', foreign_keys='Cours.creater_user', backref='creator', lazy=True)
    notes = db.relationship('Note', backref='student', lazy=True)
    classes = db.relationship('Classe', secondary=classe_eleve, backref=db.backref('eleves', lazy='dynamic'))
    matieres = db.relationship('Matiere', backref='professor', lazy=True)

    def set_password(self, password):
        """Hash the password and set it to the `mdp` attribute."""
        self.mdp = generate_password_hash(password)

    def check_password(self, password):
        """Check the hashed password against the provided password."""
        return check_password_hash(self.mdp, password)

    def encrypt_field(self, field):           
        """Encrypt a field and return the encrypted value."""
        return cipher_suite.encrypt(field.encode())

    def decrypt_field(self, field):
        """Decrypt a field and return the decrypted value."""
        return cipher_suite.decrypt(field).decode()

    def encrypt_personal_info(self):
        """Encrypt personal information fields."""
        self.nom = self.encrypt_field(self.nom)
        self.prenom = self.encrypt_field(self.prenom)
        self.mail = self.encrypt_field(self.mail)

    def decrypt_personal_info(self):
        """Decrypt personal information fields."""
        self.nom = self.decrypt_field(self.nom)
        self.prenom = self.decrypt_field(self.prenom)
        self.mail = self.decrypt_field(self.mail)

class Cours(db.Model):
    __tablename__ = 'cours'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    creater_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)
    devoir = db.Column(db.String(100), nullable=True)
    jour = db.Column(db.String(50), nullable=True)
    horaire = db.Column(db.String(50), nullable=True)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)  # Corrected line   
    classe = db.relationship('Classe', backref=db.backref('cours_list', lazy=True))
    matiere = db.relationship('Matiere', backref=db.backref('cours_list', lazy=True))

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    nb_note = db.Column(db.String(150), nullable=False)
    commentaire = db.Column(db.String(255), nullable=False)
    cours = db.relationship('Cours', backref=db.backref('notes_list', lazy=True))
    user = db.relationship('User', backref=db.backref('student_notes_list', lazy=True))

class Devoir(db.Model):
    __tablename__ = 'devoir'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    classe = db.relationship('Classe', backref=db.backref('devoirs_list', lazy=True))

class Classe(db.Model):
    __tablename__ = 'classe'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class Matiere(db.Model):
    __tablename__ = 'matiere'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    prof_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    cours = db.relationship('Cours', backref=db.backref('matiere_cours', lazy=True))  

    

