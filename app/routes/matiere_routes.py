from flask import Blueprint, request, jsonify
from ..models import Matiere, Classe, Cours, Devoir, db

bp = Blueprint('matiere_routes', __name__)


@bp.route('/api/create/matiere', methods=['POST'])
def create_matiere():
    try:
        data = request.json
        if not all(key in data for key in ['name']):
            return jsonify({"error": "Données incomplètes"}), 400

        new_matiere = Matiere(name=data['name'])

        db.session.add(new_matiere)
        db.session.commit()
        return jsonify({"message": "matiere créé avec succès"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/api/update/matiere', methods=['PUT'])
def update_matiere():
    try:
        data = request.json
        id = data.get('id')

        if not id:
            return jsonify({"error": "ID requis"}), 400

        matiere = Matiere.query.get(id)
        if not matiere:
            return jsonify({"error": "Devoir non trouvé"}), 404

        matiere.name = data.get('name', data)

        db.session.commit()
        return jsonify({"message": "Devoir mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/api/delete/matiere', methods=['DELETE'])
def delete_matiere():
    try:
        data = request.json
        matiere_id = data.get('id')

        if not matiere_id:
            return jsonify({"error": "ID requis"}), 400

        matiere_to_del= Matiere.query.get(matiere_id)
        if not matiere_to_del:
            return jsonify({"error": "matière non trouvé"}), 404

        db.session.delete(matiere_to_del)
        db.session.commit()
        return jsonify({"message": f"Matière {matiere_to_del} supprimé"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
