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
from config import Config

# Flask extensions

# Initialize sqlalchemy and migration extensions
database = SQLAlchemy()
migrate = flask_migrate.Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register app and database with the extensions
    database.init_app(app)
    migrate.init_app(app, database)

    # TODO: Do we need this?
    # os.makedirs(app.instance_path, exist_ok=True)

        #TODO: Do we need this?
        # # Export app, db, Customer, and Destination for use in the test file
        # __all__ = ['app', 'db', 'Customer', 'Destination', 'Hotel', 'Rental', 'Flight']

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

            # Import here to avoid circular import
            from app.instance.import_data import import_data
            # Call the import_data function to import the data from JSON data file
            import_data(database)

        except Exception as e:
            print(f"Migration error: {e}")

    return app
