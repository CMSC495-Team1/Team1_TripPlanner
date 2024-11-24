from flask import Blueprint

index = Blueprint('index',__name__)

from app.routes.index import routes
