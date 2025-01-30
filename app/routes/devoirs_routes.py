from flask import Blueprint, request, jsonify
from ..models import Devoir, Classe
from .. import db

bp = Blueprint('devoirs_routes', __name__)

@bp.route('/api/create/devoir', methods=['POST'])
def create_devoir():
    try:
        data = request.json
        if not all(key in data for key in ['classe_id', 'text']):
            return jsonify({"error": "Données incomplètes"}), 400

        new_devoir = Devoir(
            classe_id=data['classe_id'],
            text=data['text']
        )

        db.session.add(new_devoir)
        db.session.commit()
        return jsonify({"message": "Devoir créé avec succès"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/update/devoir', methods=['PUT'])
def update_devoir():
    try:
        data = request.json
        devoir_id = data.get('id')

        if not devoir_id:
            return jsonify({"error": "ID requis"}), 400

        devoir = Devoir.query.get(devoir_id)
        if not devoir:
            return jsonify({"error": "Devoir non trouvé"}), 404

        devoir.classe_id = data.get('classe_id', devoir.classe_id)
        devoir.text = data.get('text', devoir.text)

        db.session.commit()
        return jsonify({"message": "Devoir mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/delete/devoir', methods=['DELETE'])
def delete_devoir():
    try:
        data = request.json
        devoir_id = data.get('id')

        if not devoir_id:
            return jsonify({"error": "ID requis"}), 400

        devoir = Devoir.query.get(devoir_id)
        if not devoir:
            return jsonify({"error": "Devoir non trouvé"}), 404

        db.session.delete(devoir)
        db.session.commit()
        return jsonify({"message": f"Devoir {devoir_id} supprimé"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
