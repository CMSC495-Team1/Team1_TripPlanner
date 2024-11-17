from flask import abort, render_template
from jinja2 import TemplateNotFound
from app.trip import trip
from app.instance.models.models import Destination

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
                    'country': destination.country,
                    'state': destination.state,
                    'city': destination.city,
                    'description': destination.description,
                    'image_filename': destination.image_filename
                }
                for destination in all_destinations
            ]

            return render_template(f'trip/{page}.html', destinations=destinations_list)
        else:
            return render_template(f'trip/{page}.html')
    except TemplateNotFound:
        abort(404)

@trip.route('/view_trips/', defaults={'page': 'view_trips'})
@trip.route('/trip/<page>')
def view_trip(page):
    try:
        return render_template(f'trip/{page}.html')
    except TemplateNotFound:
        abort(404)
