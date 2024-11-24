from flask import Blueprint

planner = Blueprint('planner', __name__, url_prefix='/planner')

from app.routes.planner import routes
