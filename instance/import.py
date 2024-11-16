import json
from app import create_app, database
from app.models.models import Destination  # Adjust import based on your project structure

# Path to your JSON file
json_file_path = 'destination_data_with_images_corrected.json'

# Create Flask application context
app = create_app()

with app.app_context():
    # Load the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Insert data into the database
    for entry in data:
        destination = Destination(
            state=entry['state'],
            description=entry['description'],
            image_filename=entry['image_filename']
        )
        database.session.add(destination)

    # Commit the changes to the database
    database.session.commit()

    print("Data has been successfully imported!")
