from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(150), unique=True, nullable=False)
    mdp = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class Cours(db.Model):
    __tablename__ = 'cours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creater_user = db.Column(db.Integer, nullable=False)
    user_concerner = db.Column(db.Integer, nullable=False)
    devoir = db.Column(db.String(100), nullable=True)


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    cours_id = db.Column(db.String(100), nullable=False)
    nb_note = db.Column(db.String(150), unique=True, nullable=False)
    commentaire = db.Column(db.String(255), nullable=False)

class Devoir(db.Model):
    __tablename__ = 'devoir'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)
