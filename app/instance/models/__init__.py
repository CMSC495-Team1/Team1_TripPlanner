from flask import Blueprint

blueprint = Blueprint('models', __name__)

from instance.models import models
