from flask import abort, render_template
from jinja2 import TemplateNotFound
from app.trip import trip
from app.models.entities import Destination

@trip.route('/plan_trip/', defaults={'page': 'plan_trip'})
@trip.route('/trip/<page>')
def show(page):
    try:
        if page == 'plan_trip':
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

            return render_template(f'trips/{page}.html', destinations=destinations_list)
        else:
            return render_template(f'trips/{page}.html')
    except TemplateNotFound:
        abort(404)

@trip.route('/view_trips/', defaults={'page': 'view_trips'})
@trip.route('/trip/<page>')
def view_trips(page):
    try:
        return render_template(f'trips/{page}.html')
    except TemplateNotFound:
        abort(404)