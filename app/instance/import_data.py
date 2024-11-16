import json
import os

from instance.models.models import Destination

def import_data(database):
    # Path to your JSON file relative to import_data.py
    destination_data = os.path.join(os.path.dirname(__file__), 'destination_data.json')
    # Load the JSON data from the file
    with open(destination_data, 'r') as file:
        destinations = json.load(file)

    # Iterate over each destination in the JSON data
    for destination_data in destinations:
        # Check if the destination already exists in the database
        destination_found = Destination.query.filter_by(state=destination_data['state']).first()

        if not destination_found:
            # If the destination does not exist, create a new Destination object
            destination = Destination(
                state=destination_data['state'],
                description=destination_data['description'],
                image_filename=destination_data['image_filename']
            )
            # Add the new Destination object to the database session
            database.session.add(destination)
        else:
            # Update only if the description or image_filename has changed
          if destination_found.description != destination_data['description'] or \
             destination_found.image_filename != destination_data['image_filename']:
                destination_found.description = destination_data['description']
                destination_found.image_filename = destination_data['image_filename']

    # Commit the changes to the database to save all new and updated Destination objects
    database.session.commit()

    # Print a success message
    print("Data has been successfully imported!")
