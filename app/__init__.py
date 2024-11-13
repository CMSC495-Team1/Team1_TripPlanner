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
from config import Config
from app.extensions.db import db, migrate
from app.models.entities import Customer, Destination, Hotel, Rental, Flight

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    os.makedirs(app.instance_path, exist_ok=True)

    with app.app_context():
        db.create_all()  # Create all tables in the database

        # Export app, db, Customer, and Destination for use in the test file
        __all__ = ['app', 'db', 'Customer', 'Destination', 'Hotel', 'Rental', 'Flight']

    from app.main import blueprint as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.trip import blueprint as trip_blueprint
    app.register_blueprint(trip_blueprint)

    return app

if __name__ == '__main__':
    tripPlanner = create_app()
    tripPlanner.run(debug=True)