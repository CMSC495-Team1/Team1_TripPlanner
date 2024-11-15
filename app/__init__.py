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

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
# from app.models.models import Customer, Destination, Hotel, Rental, Flight

# Flask extensions

# Global variables to be used in models.py
database = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database extensions
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

    return app

if __name__ == '__main__':
    tripPlanner = create_app()
    tripPlanner.run(debug=True)


