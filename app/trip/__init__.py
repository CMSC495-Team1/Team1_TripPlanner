from flask import Blueprint

trip = Blueprint('trip',
                 __name__,
                 template_folder='templates',
                 static_url_path='/trip/static',
                 static_folder='static')

from app.trip import routes
