from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from ..models import User
from .. import db

bp = Blueprint('auth_routes', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(mail=email).first()
        if user and user.mdp == password:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('user_routes.home'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth_routes.login'))

