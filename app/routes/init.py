from flask import Blueprint

bp = Blueprint('routes', __name__)

from . import user_routes, cours_routes, note_routes, auth_routes, devoirs_routes, classes_routes, matiere_routes

