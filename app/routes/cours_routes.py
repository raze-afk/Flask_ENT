from flask import Blueprint, request, jsonify
from ..models import Cours
from .. import db

bp = Blueprint('cours_routes', __name__)

@bp.route('/api/show/cours', methods=['GET'])
def show_cours():
    cours_id = request.args.get('id')

    if cours_id:
        cours = Cours.query.get(cours_id)
        if cours:
            return jsonify({
                "id": cours.id,
                "name": cours.name,
                "creater_user": cours.creater_user,
                "user_concerner": cours.user_concerner,
                "devoir": cours.devoir
            }), 200
        return jsonify({"error": "Cours non trouvé"}), 404

    cours_list = Cours.query.all()
    cours_data = [
        {
            "id": c.id,
            "name": c.name,
            "creater_user": c.creater_user,
            "user_concerner": c.user_concerner,
            "devoir": c.devoir
        }
        for c in cours_list
    ]
    return jsonify(cours_data), 200

@bp.route('/api/create/cours', methods=['POST'])
def create_cours():
    try:
        data = request.json
        if not all(key in data for key in ['name', 'creater_user', 'user_concerner']):
            return jsonify({"error": "Données incomplètes"}), 400

        new_cours = Cours(
            name=data['name'],
            creater_user=data['creater_user'],
            user_concerner=data['user_concerner'],
            devoir=data.get('devoir', None)
        )

        db.session.add(new_cours)
        db.session.commit()
        return jsonify({"message": "Cours créé avec succès"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/update/cours', methods=['PUT'])
def update_cours():
    try:
        data = request.json
        cours_id = data.get('id')

        if not cours_id:
            return jsonify({"error": "ID requis"}), 400

        cours = Cours.query.get(cours_id)
        if not cours:
            return jsonify({"error": "Cours non trouvé"}), 404

        cours.name = data.get('name', cours.name)
        cours.creater_user = data.get('creater_user', cours.creater_user)
        cours.user_concerner = data.get('user_concerner', cours.user_concerner)
        cours.devoir = data.get('devoir', cours.devoir)

        db.session.commit()
        return jsonify({"message": "Cours mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/delete/cours', methods=['DELETE'])
def delete_cours():
    try:
        cours_id = request.args.get('id')

        if not cours_id:
            return jsonify({"error": "ID requis"}), 400

        cours = Cours.query.get(cours_id)
        if not cours:
            return jsonify({"error": "Cours non trouvé"}), 404

        db.session.delete(cours)
        db.session.commit()
        return jsonify({"message": f"Cours {cours_id} supprimé"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

