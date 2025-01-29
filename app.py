from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

# Configuration de la connexion à la base de données MySQL existante
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/database?collation=utf8mb4_general_ci'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#------------------------------------------------------------------------------
# Modèle de l'utilisateur (correspondant à ta base existante)
#------------------------------------------------------------------------------
class User(db.Model):
    __tablename__ = 'user'  # Assurez-vous que ce nom correspond à la table existante
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(150), unique=True, nullable=False)
    mdp = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

#------------------------------------------------------------------------------
# Route d'accueil
#------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return '<h1>API Utilisateurs</h1><p>Bienvenue sur l\'API Flask.</p>'

#------------------------------------------------------------------------------
# Afficher un utilisateur ou tous les utilisateurs
#------------------------------------------------------------------------------
@app.route('/api/show/user', methods=['GET'])
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

#------------------------------------------------------------------------------
# Créer un utilisateur
#------------------------------------------------------------------------------
@app.route('/api/create/user', methods=['POST'])
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

#------------------------------------------------------------------------------
# Mettre à jour un utilisateur
#------------------------------------------------------------------------------
@app.route('/api/update/user', methods=['PUT'])
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

#------------------------------------------------------------------------------
# Supprimer un utilisateur
#------------------------------------------------------------------------------
@app.route('/api/delete/user', methods=['DELETE'])
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

#------------------------------------------------------------------------------
# Exécuter l'application
#------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()

