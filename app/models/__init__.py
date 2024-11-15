from flask import Blueprint

blueprint = Blueprint('models', __name__)

from app.models import models