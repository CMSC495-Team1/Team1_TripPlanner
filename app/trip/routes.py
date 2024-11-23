from flask import abort, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from app.trip import trip
from app.models.destination import Destination
from flask_login import login_required, current_user


@trip.route('/plan_trip/', methods=['GET', 'POST'])
@login_required
def plan_trip():
    """
    Handles GET and POST requests for the Plan Trip page.
    Requires user authentication.
    """
    try:
        # Fetch all destinations for both GET and POST requests
        all_destinations = Destination.query.all()
        destinations_list = [
            {
                'country': destination.country,
                'state': destination.state,
                'city': destination.city,
                'description': destination.description,
                'image_filename': destination.image_filename
            }
            for destination in all_destinations
        ] if all_destinations else []

        if request.method == 'POST':
            # Handle form submission for trip planning
            state = request.form.get('state')
            trip_name = request.form.get('trip_name')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            # Perform validation for missing fields
            if not state or not trip_name or not start_date or not end_date:
                missing_fields = []
                if not state: missing_fields.append('state')
                if not trip_name: missing_fields.append('trip_name')
                if not start_date: missing_fields.append('start_date')
                if not end_date: missing_fields.append('end_date')

                print(f"Missing fields: {', '.join(missing_fields)}")  # For debugging
                return render_template('trip/plan_trip.html', destinations=destinations_list)

            return redirect(url_for('trip.view_trips', page='view_trips'))

        return render_template('trip/plan_trip.html', destinations=destinations_list)

    except TemplateNotFound:
        abort(404)


@trip.route('/view_trips/', methods=['GET'])
@login_required
def view_trips():
    """
    Handles requests to view trips.
    Requires user authentication.
    """
    try:
        return render_template('trip/view_trips.html')
    except TemplateNotFound:
        abort(404)


@trip.route('/trip_details/', methods=['GET', 'POST'])
@login_required
def trip_details():
    """
    Handles trip details page.
    Requires user authentication.
    """
    if request.method == 'POST':
        # Retrieve trip data submitted from the "Start Planning" step
        state = request.form.get('state')
        trip_name = request.form.get('trip_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Ensure all fields are provided
        if not all([state, trip_name, start_date, end_date]):
            error_message = "Please complete all required fields before submitting."
            return render_template('trip/trip_details.html', error=error_message)

        return redirect(url_for('trip.view_trips'))

    # For a GET request, render the form with pre-filled data if available
    state = request.args.get('state', 'Default State')
    return render_template('trip/trip_details.html', state=state)
