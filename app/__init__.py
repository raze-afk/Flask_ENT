from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/database?collation=utf8mb4_general_ci'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .routes import user_routes, cours_routes, note_routes, auth_routes
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(cours_routes.bp)
        app.register_blueprint(note_routes.bp)
        app.register_blueprint(auth_routes.bp)
    return app

