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
# Flask extensions

# Initialize sqlalchemy and migration extensions
database = SQLAlchemy()
migrate_database = flask_migrate.Migrate()
bcrypt = Bcrypt()
mail = Mail()
login = LoginManager()

def create_app(config_class=Config):
    # Imports in this scope aer to avoid circular dependencies
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)

    # Register app and database with the extensions
    database.init_app(app)
    migrate_database.init_app(app, database)

    # Register blueprints
    from app.main import main
    app.register_blueprint(main)

    from app.trip import trip
    app.register_blueprint(trip)

    from app.auth import auth
    app.register_blueprint(auth)

    # Run migration steps programmatically
    with app.app_context():
        try:
            # Step 2: Initialize migrations (only if the migrations folder doesn't exist)
            if not pathlib.Path('migrations').exists():
                flask_migrate.init()

            # Step 3: Generate a migration script
            flask_migrate.migrate()

            # Step 4: Apply the migration to the database
            flask_migrate.upgrade()

            from app.database.import_data import import_data
            # Call the import_data function to import the data from JSON data file
            import_data(database)

        except Exception as e:
            print(f"Migration error: {e}")

    return app
