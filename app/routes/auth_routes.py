from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from ..models import User, Cours, Devoir, Note, Classe, Matiere, classe_eleve
from .. import db
from cryptography.fernet import Fernet
import os
from ..encryption_utils import *
import time

bp = Blueprint('auth_routes', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Déchiffrer tous les emails dans la base de données pour la comparaison
        users = User.query.all()
        for user in users:
            decrypted_email = decrypt_data(user.mail)
            if decrypted_email == email and user.check_password(password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                if user.status == 'admin':
                    return redirect(url_for('auth_routes.admin_home'))
                elif user.status == 'etudiant':
                    return redirect(url_for('auth_routes.student_home'))
                elif user.status == 'professeur':
                    return redirect(url_for('auth_routes.teacher_home'))

        flash('Invalid email or password', 'danger')
        time.sleep(3)
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_routes.login'))

@bp.route('/admin_home', methods=['GET'])
def admin_home():
    user_id = session.get('user_id')
    users = User.query.all()
    user = User.query.get(user_id)

    for use in users:
        use.decrypt_personal_info()

#    if user:
#        user 
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('auth_routes.login'))

    cours = Cours.query.all()
    devoirs = Devoir.query.all()
    notes = Note.query.all()
    classes = Classe.query.all()
    eleves = User.query.filter_by(status='etudiant').all()
    matieres = Matiere.query.all()

    # Déchiffrer les informations personnelles des élèves

    return render_template('admin.html', user=user, cours=cours, devoirs=devoirs, notes=notes, classes=classes, eleves=eleves, matieres=matieres, users=users)

@bp.route('/student_home', methods=['GET'])
def student_home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.decrypt_personal_info()  # Déchiffrer les informations personnelles de l'utilisateur
    else:
        flash('User not found', 'danger')
        return redirect(url_for('auth_routes.login'))

    cours = Cours.query.all()  # Vous pouvez filtrer les cours spécifiques à l'étudiant si nécessaire
    devoirs = Devoir.query.join(Classe).join(classe_eleve).filter(classe_eleve.c.user_id == user_id).all()
    notes = Note.query.filter_by(user_id=user_id).all()

    return render_template('student.html', user=user, cours=cours, devoirs=devoirs, notes=notes)

@bp.route('/teacher_home', methods=['GET'])
def teacher_home():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user:
        user.decrypt_personal_info()  # Déchiffrer les informations personnelles de l'utilisateur
    else:
        flash('User not found', 'danger')
        return redirect(url_for('auth_routes.login'))

    cours = Cours.query.filter_by(creater_user=user_id).all()
    devoirs = Devoir.query.all()
    notes = Note.query.all()
    classes = Classe.query.all()
    eleves = User.query.filter_by(status='etudiant').all()

    # Déchiffrer les informations personnelles des élèves
    for eleve in eleves:
        eleve.decrypt_personal_info()

    return render_template('teacher.html', user=user, cours=cours, devoirs=devoirs, notes=notes, classes=classes, eleves=eleves)

