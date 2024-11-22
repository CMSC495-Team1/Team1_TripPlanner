import pathlib
import flask_migrate

def initialize_database(app, database):
    with app.app_context():
        try:
            migrations_dir = pathlib.Path('migrations')
            db_file = pathlib.Path(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))

            if not migrations_dir.exists():
                print("Initializing new migration repository...")
                flask_migrate.init()

                print("Creating initial database tables...")
                database.create_all()

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

            print("Importing initial data...")
            from app.data.import_data import import_data
            import_data(database)

            print("Database initialization complete!")

        except Exception as e:
            print(f"Migration error: {str(e)}")
            print("Attempting to recover...")

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
