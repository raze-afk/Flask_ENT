from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Ajout de Flask-Migrate
import os

db = SQLAlchemy()
migrate = Migrate()  # Initialisation de Flask-Migrate

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/ENT?collation=utf8mb4_general_ci'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # Intégration de Flask-Migrate

    with app.app_context():
        from .routes import user_routes, cours_routes, note_routes, auth_routes, devoirs_routes, classes_routes, matiere_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(cours_routes.bp)
        app.register_blueprint(note_routes.bp)
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(devoirs_routes.bp)
        app.register_blueprint(classes_routes.bp)
        app.register_blueprint(matiere_routes.bp)

    return app

