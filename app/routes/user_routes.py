from flask import Blueprint, request, jsonify
from ..models import User, Cours, Note, Devoir, Classe, db, classe_eleve

bp = Blueprint('user_routes', __name__)

@bp.route('/api/show/user', methods=['GET'])
def show_user():
    user_id = request.args.get('id')

    if user_id:
        user = User.query.get(user_id)
        if user:
            user.decrypt_personal_info()
            return jsonify({
                "id": user.id,
                "nom": user.nom,
                "prenom": user.prenom,
                "mail": user.mail,
                "status": user.status,
                "cours": [{"id": c.id, "name": c.name} for c in user.cours],
                "devoirs": [{"id": d.id, "text": d.text} for d in user.devoirs],
                "notes": [{"id": n.id, "nb_note": n.nb_note, "commentaire": n.commentaire} for n in user.notes],
                "classes": [{"id": cl.id, "name": cl.name} for cl in user.classes]
            }), 200
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    users = User.query.all()
    user_list = []
    for u in users:
        u.decrypt_personal_info()
        user_list.append({
            "id": u.id,
            "nom": u.nom,
            "prenom": u.prenom,
            "mail": u.mail,
            "status": u.status,
            "classes": [{"id": cl.id, "name": cl.name} for cl in u.classes]
        })

    return jsonify(user_list), 200

@bp.route('/api/create/user', methods=['POST'])
def create_user():
    try:
        data = request.json
        required_fields = ['nom', 'prenom', 'mail', 'password', 'status', 'classe_id']
        if not all(key in data for key in required_fields):
            return jsonify({"error": "Données incomplètes"}), 400

        if data['status'] not in ['admin', 'etudiant', 'professeur']:
            return jsonify({"error": "Statut invalide"}), 400

        existing_user = User.query.filter_by(mail=data['mail']).first()
        if existing_user:
            return jsonify({"error": "Email déjà utilisé"}), 400

        new_user = User(
            nom=data['nom'],
            prenom=data['prenom'],
            mail=data['mail'],
            status=data['status']
        )
        new_user.set_password(data['password'])  # Hash the password
        new_user.encrypt_personal_info()  # Encrypt personal information
        db.session.add(new_user)
        db.session.commit()

        # Ajouter l'utilisateur à la classe
        new_classe_eleve = classe_eleve.insert().values(
            classe_id=data['classe_id'],
            user_id=new_user.id
        )
        db.session.execute(new_classe_eleve)
        db.session.commit()

        return jsonify({"message": "Utilisateur créé avec succès", "id": new_user.id}), 201

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

        if 'mail' in data and data['mail'] != user.mail:
            existing_user = User.query.filter_by(mail=data['mail']).first()
            if existing_user:
                return jsonify({"error": "Email déjà utilisé"}), 400

        user.nom = data.get('nom', user.nom)
        user.prenom = data.get('prenom', user.prenom)
        user.mail = data.get('mail', user.mail)
        if 'password' in data:
            user.set_password(data['password'])  # Hash the new password
        user.status = data.get('status', user.status)

        user.encrypt_personal_info()  # Encrypt personal information
        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/delete/user', methods=['DELETE'])
def delete_user():
    try:
        data = request.get_json()
        user_id = data.get('id')

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

