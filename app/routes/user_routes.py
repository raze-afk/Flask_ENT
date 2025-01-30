from flask import Blueprint, request, jsonify
from ..models import User
from .. import db

bp = Blueprint('user_routes', __name__)

@bp.route('/', methods=['GET'])
def home():
    return '<h1>API Utilisateurs</h1><p>Bienvenue sur l\'API Flask.</p>'

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(mail=data['mail']).first()
    if user and check_password_hash(user.mdp, data['mdp']):
        return jsonify({'message': 'Login successful!', 'status': user.status})
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

@bp.route('/api/show/user', methods=['GET'])
def show_user():
    user_id = request.args.get('id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                "id": user.id,
                "nom": user.nom,
                "prenom": user.prenom,
                "mail": user.mail,
                "status": user.status
            }), 200
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    users = User.query.all()
    user_list = [{"id": u.id, "nom": u.nom, "prenom": u.prenom, "mail": u.mail, "status": u.status} for u in users]
    return jsonify(user_list), 200

@bp.route('/api/create/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        if not all(key in data for key in ['nom', 'prenom', 'mail', 'password', 'status']):
            return jsonify({"error": "Données incomplètes"}), 400

        if data['status'] not in ['admin', 'etudiant', 'professeur']:
            return jsonify({"error": "Statut invalide"}), 400

        new_user = User(
            nom=data['nom'],
            prenom=data['prenom'],
            mail=data['mail'],
            mdp=data['password'],
            status=data['status']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Utilisateur créé avec succès"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/update/user', methods=['PUT'])
def update_user():
    try:
        data = request.json
        user_id = data.get('id')

        if not user_id:
            return jsonify({"error": "ID requis"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        user.nom = data.get('nom', user.nom)
        user.prenom = data.get('prenom', user.prenom)
        user.mail = data.get('mail', user.mail)
        user.mdp = data.get('password', user.mdp)
        user.status = data.get('status', user.status)

        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/delete/user', methods=['DELETE'])
def delete_user():
    try:
        user_id = request.args.get('id')

        if not user_id:
            return jsonify({"error": "ID requis"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Utilisateur {user_id} supprimé"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

