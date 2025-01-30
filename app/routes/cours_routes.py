from flask import Blueprint, request, jsonify
from ..models import Cours, Classe
from .. import db

bp = Blueprint('cours_routes', __name__)

@bp.route('/api/create/cours', methods=['POST'])
def create_cours():
    try:
        data = request.json
        if not all(key in data for key in ['name', 'creater_user', 'classe_id', 'jour', 'horaire']):
            return jsonify({"error": "Données incomplètes"}), 400

        new_cours = Cours(
            name=data['name'],
            creater_user=data['creater_user'],
            classe_id=data['classe_id'],
            jour=data['jour'],
            horaire=data['horaire'],
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
        cours.classe_id = data.get('classe_id', cours.classe_id)
        cours.jour = data.get('jour', cours.jour)
        cours.horaire = data.get('horaire', cours.horaire)
        cours.devoir = data.get('devoir', cours.devoir)

        db.session.commit()
        return jsonify({"message": "Cours mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/delete/cours', methods=['DELETE'])
def delete_cours():
    try:
        data = request.json
        cours_id = data.get('id')

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

