from flask import Blueprint

trip = Blueprint('trips',
                 __name__,
                 template_folder='templates',
                 static_url_path='/trips/static',
                 static_folder='static')

from app.trip import routes