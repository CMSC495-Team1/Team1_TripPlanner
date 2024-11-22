import pathlib
import os

# Locate the project directory dynamically
project_dir = pathlib.Path(__file__).resolve().parent

# Correctly define the database path
database_path = project_dir / 'app' / 'instance' / 'app.db'
print(f"Database path: {database_path}")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or f'sqlite:///{project_dir / "app" / "instance" / "app.db"}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Warn if the path or instance folder is missing
    if not database_path.parent.exists():
        print(f"Warning: Instance folder {database_path.parent} does not exist.")
    elif not database_path.exists():
        print(f"Warning: Database file not found at {database_path}. Ensure it's created or migrated.")
