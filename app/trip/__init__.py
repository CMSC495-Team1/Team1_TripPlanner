from flask import Blueprint

blueprint = Blueprint('trip', __name__)

from app.trip import routes