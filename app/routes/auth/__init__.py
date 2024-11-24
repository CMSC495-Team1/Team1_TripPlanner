from flask import Blueprint

auth = Blueprint('auth',__name__)

from app.routes.auth import routes
