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
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
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
    with (app.app_context()):
        try:
            migrations_dir = pathlib.Path('migrations')
            db_file = pathlib.Path(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))

            # If no migrations folder exists, start fresh
            if not migrations_dir.exists():
                print("Initializing new migration repository...")
                flask_migrate.init()

                # Create initial database tables
                print("Creating initial database tables...")
                database.create_all()

                # Create and apply initial migration
                print("Creating initial migration...")
                flask_migrate.migrate()
                print("Applying initial migration...")
                try:
                    flask_migrate.upgrade()
                except Exception as upgrade_error:
                    if "Can't locate revision" in str(upgrade_error):
                        print("Stamping initial database state...")
                        flask_migrate.stamp()
                        flask_migrate.upgrade()
                    else:
                        raise upgrade_error

            # Import data only after successful migration
            print("Importing initial data...")
            from app.data.import_data import import_data
            import_data(database)

            print("Database initialization complete!")

        except Exception as e:
            print(f"Migration error: {str(e)}")
            print("Attempting to recover...")

            # Recovery procedure
            try:
                if migrations_dir.exists():
                    print("Removing existing migrations...")
                    import shutil
                    shutil.rmtree(migrations_dir)

                if db_file.exists():
                    print("Removing existing database...")
                    db_file.unlink()

                print("Creating fresh database...")
                database.create_all()

                print("Initializing fresh migrations...")
                flask_migrate.init()
                flask_migrate.migrate()
                flask_migrate.upgrade()

                print("Importing data...")
                from app.data.import_data import import_data
                import_data(database)

                print("Recovery complete!")
            except Exception as recovery_error:
                print(f"Recovery failed: {str(recovery_error)}")
                raise

    return app
