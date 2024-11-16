import pathlib
import os

project_dir = pathlib.Path(__file__).resolve().parent.parent

database_path = project_dir / 'app' / 'instance' / 'app.db'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')\
                              or f'sqlite:///{database_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
