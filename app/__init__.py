from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from app.data.initialize_database import initialize_database
from config import Config
from flask_bcrypt import Bcrypt

# Initialize extensions
database = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message_category = 'info'

    database.init_app(app)
    migrate.init_app(app, database)

    # Register routes (previously blueprints)
    from app.routes.index import index
    from app.routes.auth import auth
    from app.routes.flights import flights
    from app.routes.planner import planner

    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(flights, url_prefix='/flights')
    app.register_blueprint(planner, url_prefix='/planner')

    initialize_database(app, database)



    return app
