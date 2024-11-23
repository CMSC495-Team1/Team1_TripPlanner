"""
Trip Planner Application
-------------------------
This is a Flask web application for the Trip Planner project, developed for CMSC 495 7380.
The application allows users to explore travel destinations, book flights, rent cars,
and book hotels, providing an integrated travel planning experience.

## Team Members
- Galia Adelshin (Project Manager)
- Terence Boyce (Test Director)
- Jared Brick (Software Developer)
- Xavier Watson (Software Developer)
- Greg Chelchowski (Requirements Manager/UX/UI Designer)

Course: CMSC 495 7380
"""

import pathlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_migrate
from flask_mail import Mail
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.data.initialize_database import initialize_database
# Flask extensions

# Initialize sqlalchemy and migration extensions
database = SQLAlchemy()
migrate_database = flask_migrate.Migrate()
bcrypt = Bcrypt()
mail = Mail()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    login.login_view = 'auth.login'
    
    database.init_app(app)
    migrate_database.init_app(app, database)

    # Register blueprints
    from app.main import main
    app.register_blueprint(main)

    from app.trip import trip
    app.register_blueprint(trip)

    from app.auth import auth
    app.register_blueprint(auth)

    initialize_database(app, database)

    return app
