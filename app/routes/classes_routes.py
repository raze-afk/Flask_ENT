from flask import Blueprint, request, jsonify
from ..models import Classe, User, db

bp = Blueprint('classe_routes', __name__)

# Create a new classe
@bp.route('/api/create/classe', methods=['POST'])
def create_classe():
    try:
        data = request.json
        if not all(key in data for key in ['name']):
            return jsonify({"error": "Données incomplètes"}), 400

        new_classe = Classe(name=data['name'])
        db.session.add(new_classe)
        db.session.commit()
        return jsonify({"message": "Classe créée avec succès", "id": new_classe.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Read a classe
@bp.route('/api/show/classe', methods=['GET'])
def show_classe():
    classe_id = request.args.get('id')

    if classe_id:
        classe = Classe.query.get(classe_id)
        if classe:
            eleves = [{"id": user.id, "nom": user.nom, "prenom": user.prenom} for user in classe.eleves]
            return jsonify({
                "id": classe.id,
                "name": classe.name,
                "eleves": eleves
            }), 200
        return jsonify({"error": "Classe non trouvée"}), 404

    classes = Classe.query.all()
    classe_list = [{
        "id": c.id,
        "name": c.name
    } for c in classes]

    return jsonify(classe_list), 200

# Update a classe
@bp.route('/api/update/classe', methods=['PUT'])
def update_classe():
    try:
        data = request.json
        classe_id = data.get('id')

        if not classe_id:
            return jsonify({"error": "ID requis"}), 400

        classe = Classe.query.get(classe_id)
        if not classe:
            return jsonify({"error": "Classe non trouvée"}), 404

        classe.name = data.get('name', classe.name)

        db.session.commit()
        return jsonify({"message": "Classe mise à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a classe
@bp.route('/api/delete/classe', methods=['DELETE'])
def delete_classe():
    try:
        data = request.json
        classe_id = data.get('id')

        if not classe_id:
            return jsonify({"error": "ID requis"}), 400

        classe = Classe.query.get(classe_id)
        if not classe:
            return jsonify({"error": "Classe non trouvée"}), 404

        db.session.delete(classe)
        db.session.commit()
        return jsonify({"message": f"Classe {classe_id} supprimée"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add students to a classe
@bp.route('/api/add/eleves', methods=['POST'])
def add_eleves_to_classe():
    try:
        data = request.json
        classe_id = data.get('classe_id')
        user_ids = data.get('user_ids')

        if not classe_id or not user_ids:
            return jsonify({"error": "ID de classe et IDs des utilisateurs requis"}), 400

        classe = Classe.query.get(classe_id)
        if not classe:
            return jsonify({"error": "Classe non trouvée"}), 404

        for user_id in user_ids:
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": f"Utilisateur avec ID {user_id} non trouvé"}), 404
            if user not in classe.eleves:
                classe.eleves.append(user)

        db.session.commit()
        return jsonify({"message": "Élèves ajoutés à la classe avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
