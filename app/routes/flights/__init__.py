from flask import Blueprint

flights = Blueprint('flights',__name__)

from app.routes.flights import routes
