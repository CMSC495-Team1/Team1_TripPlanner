from flask import render_template
from app.trip import blueprint
from app.models.entities import Destination

@blueprint.route('/plan_trip/')
def destinations():
    # Query all destinations from the database
    all_destinations = Destination.query.all()

    # Convert each Destination instance to a dictionary
    destinations_list = [
        {
            'name': destination.name,
            'description': destination.description,
            'image_url': destination.image_url
        }
        for destination in all_destinations
    ]

    return render_template('plan_trip.html', destinations=destinations_list)