from datetime import datetime

from flask import abort, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from app.trip import trip
from app.models.destination import Destination
from flask_login import login_required, current_user
from app import database
from app.models.trip import Trip

from app.models.trip import Trip
from app import database


@trip.route('/plan_trip/', methods=['GET', 'POST'])
@login_required
def plan_trip():
    """
    Handles GET and POST requests for the Plan Trip page.
    Requires user authentication.
    """
    try:
        # Fetch all destinations for the dropdown list
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
            # Get form data
            state = request.form.get('state')
            trip_name = request.form.get('trip_name')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            # Validate form fields
            if not all([state, trip_name, start_date, end_date]):
                print("Validation failed: Missing fields")
                return render_template('trip/plan_trip.html', destinations=destinations_list,
                                       error="All fields are required.")

            try:
                # Parse and validate dates
                from datetime import datetime
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError as e:
                print(f"Date validation error: {e}")
                return render_template('trip/plan_trip.html', destinations=destinations_list,
                                       error="Invalid date format.")

            # Create a new Trip object
            new_trip = Trip(
                trip_name=trip_name,
                destination=state,
                start_date=start_date,
                end_date=end_date,
                user_id=current_user.id  # Tie the trip to the logged-in user
            )
            database.session.add(new_trip)
            database.session.commit()

            print(f"New Trip to be added: {new_trip}")  # Debugging
            print(f"Current user: {current_user.id}, {current_user.username}")

            # Add the trip to the database
            print(f"Adding Trip: {new_trip}")
            database.session.add(new_trip)
            try:
                database.session.commit()
                print(f"Trip successfully saved: {new_trip}")
            except Exception as e:
                print(f"Error saving trip: {e}")
                database.session.rollback()

                return render_template('trip/plan_trip.html', destinations=destinations_list,
                                       error="Could not save trip.")

            # Redirect to the view trips page
            return redirect(url_for('trip.view_trips'))

        # Render the Plan Trip page for GET requests
        return render_template('trip/plan_trip.html', destinations=destinations_list)


    except TemplateNotFound:
        abort(404)


@trip.route('/view_trips/', methods=['GET'])
@login_required
def view_trips():
    """
    Displays all trips scheduled by the logged-in user.
    """
    try:
        print(f"Current user ID: {current_user.id}")  # Debugging: Print user ID
        user_trips = Trip.query.filter_by(user_id=current_user.id).all()
        print(f"Trips found: {user_trips}")  # Debugging: Print trips
        return render_template('trip/view_trips.html', trips=user_trips)
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
