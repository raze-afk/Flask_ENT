from flask import Blueprint, request, jsonify
from ..models import Devoir
from .. import db

bp = Blueprint('devoirs_routes', __name__)

@bp.route('/api/show/devoir', methods=['GET'])
def show_devoirs():
    if 'id' in request.args: #query les devois d'un utilisateur
        user_id = request.args.get('user_id')

        devoirs = Devoir.query.get(user_id=user_id)
        if devoirs:
            return jsonify({
                "user_id": Devoir.user_id,
                "text": Devoir.text
            }), 200
        return jsonify({"error": "Aucun devoir trouvé"}), 404
    else: #query tous les devoirs
        devoirs = Devoir.query.all()
        devoirs_list = [{"id": d.id, "user_id": d.user_id, "text": d.text} for d in devoirs]
        return jsonify(devoirs_list), 200

@bp.route('/api/create/devoir', methods=['POST'])
def create_devoir():
    try:
        data = request.json # user_id, text
        text = data.get("text")
        if not text:
            return jsonify({"error": "Le champ 'text' est requis"}), 400
        new_devoir = Devoir(
            user_id=data['user_id'],
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
        data = request.json # id, text
        id = data.get("id")
        text = data.get("text")
        if not text:
                return jsonify({"error": "Le champ 'text' est requis"}), 400
        devoir = Devoir.query.get(id)
        devoir.text = text
        db.session.commit()
        return jsonify({"message": "Devoir mis à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@bp.route('/api/delete/devoir', methods=['DELETE'])
def delete_devoir():
    try:
            data = request.json # id
            id = data.get("id")
            devoir = Devoir.query.get(id)######### ajouter les if de securité
            db.session.delete(devoir)
            db.session.commit()
            return jsonify({"message": "Devoir supprimé"}), 200######### enlever la prim key de la db
    except Exception as e:
        return jsonify({"error": str(e)}), 500



