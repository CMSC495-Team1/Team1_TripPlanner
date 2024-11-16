from app import create_app, database
from flask_migrate import Migrate

app = create_app()
Migrate(app, database)

if __name__ == '__main__':
    app.run(debug=True)
    pass
