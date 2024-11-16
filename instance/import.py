import json
from app import create_app, database
from app.models.models import Destination  # Adjust import based on your project structure



def import_data(app):
    # Path to your JSON file relative to import.py
    destinations_data = 'destination_data.json'

    with app.app_context():
        # Load the JSON data
        with open(destinations_data, 'r') as file:
            destinations = json.load(file)

        # Insert data into the database
        for destination in destinations:
            destination = Destination(
                state=destination['state'],
                description=destination['description'],
                image_filename=destination['image_filename']
            )
            database.session.add(destination)

        # Commit the changes to the database
        database.session.commit()

        print("Data has been successfully imported!")
