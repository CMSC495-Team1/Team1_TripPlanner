from flask import Blueprint

auth = Blueprint('auth',
                 __name__,
                 template_folder='templates',
                 static_url_path='/auth/static',
                 static_folder='static',)

from app.auth import routes
