from flask import Blueprint, request, jsonify
from ..models import Note, Cours
from .. import db

bp = Blueprint('note_routes', __name__)

@bp.route('/api/show/note', methods=['GET'])
def show_note():
    note_id = request.args.get('id')

    if note_id:
        note = Note.query.get(note_id)
        if note:
            return jsonify({
                "id": note.id,
                "user_id": note.user_id,
                "cours_id": note.cours_id,
                "nb_note": note.nb_note,
                "commentaire": note.commentaire
            }), 200
        return jsonify({"error": "Note non trouvée"}), 404

    notes = Note.query.all()
    note_list = [{"id": n.id, "user_id": n.user_id, "cours_id": n.cours_id, "nb_note": n.nb_note, "commentaire": n.commentaire} for n in notes]
    return jsonify(note_list), 200

@bp.route('/api/create/note', methods=['POST'])
def create_note():
    try:
        data = request.json
        if not all(key in data for key in ['user_id', 'cours_id', 'nb_note', 'commentaire']):
            return jsonify({"error": "Données incomplètes"}), 400

        cours = Cours.query.get(data['cours_id'])
        if not cours:
            return jsonify({"error": "Cours non trouvé"}), 404

        new_note = Note(
            user_id=data['user_id'],
            cours_id=data['cours_id'],
            nb_note=data['nb_note'],
            commentaire=data['commentaire'],
        )
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"message": "Note créée avec succès"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/update/note', methods=['PUT'])
def update_note():
    try:
        data = request.json
        note_id = data.get('id')

        if not note_id:
            return jsonify({"error": "ID requis"}), 400

        note = Note.query.get(note_id)
        if not note:
            return jsonify({"error": "Note non trouvée"}), 404

        note.user_id = data.get('user_id', note.user_id)
        note.cours_id = data.get('cours_id', note.cours_id)
        note.nb_note = data.get('nb_note', note.nb_note)
        note.commentaire = data.get('commentaire', note.commentaire)

        db.session.commit()
        return jsonify({"message": "Note mise à jour"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/api/delete/note', methods=['DELETE'])
def delete_note():
    try:
        data = request.json
        note_id = data.get('id')

        if not note_id:
            return jsonify({"error": "ID requis"}), 400

        note = Note.query.get(note_id)
        if not note:
            return jsonify({"error": "Note non trouvée"}), 404

        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": f"Note {note_id} supprimée"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

