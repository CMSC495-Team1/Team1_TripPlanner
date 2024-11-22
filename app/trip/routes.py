from flask import abort, render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
from app.trip import trip
from app.instance.models.models import Destination
from app.instance.models.models import Trip
from datetime import datetime
from app import database
from flask import session, flash


@trip.route('/plan_trip/', methods=['GET', 'POST'])
def plan_trip():
    """
    Handles GET and POST requests for the Plan Trip page.
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
            # Check if the user is logged in
            user_id = session.get('user_id')
            if not user_id:
                flash("You must be logged in to plan a trip.", "error")
                return redirect(url_for('auth.login'))

            # Handle form submission for trip planning
            state = request.form.get('state')
            trip_name = request.form.get('trip_name')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')

            # Perform validation for missing fields
            if not state or not trip_name or not start_date or not end_date:
                error_message = "Please fill out all required fields."
                return render_template('trip/plan_trip.html', destinations=destinations_list, error=error_message)

            # Perform validation for invalid dates
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                if start_date_obj > end_date_obj:
                    error_message = "Start Date cannot be after the End Date."
                    return render_template('trip/plan_trip.html', destinations=destinations_list, error=error_message)

                # Save the trip to the database, linked to the user
                new_trip = Trip(
                    trip_name=trip_name,
                    state=state,
                    start_date=start_date_obj,
                    end_date=end_date_obj,
                    user_id=user_id  # Associate with the logged-in user
                )
                database.session.add(new_trip)
                database.session.commit()

                # Redirect to the view trips page after saving
                flash("Trip successfully created!", "success")
                return redirect(url_for('trip.view_trips'))

            except ValueError:
                error_message = "Invalid date format. Please use YYYY-MM-DD."
                return render_template('trip/plan_trip.html', destinations=destinations_list, error=error_message)

        # Handle GET request: Render the plan_trip page with destinations
        return render_template('trip/plan_trip.html', destinations=destinations_list)

    except TemplateNotFound:
        abort(404)


@trip.route('/view_trips/', methods=['GET'])
def view_trips():
    """
    Handles requests to view trips.
    """
    try:
        # Retrieve all trips from the database
        all_trips = Trip.query.all()  # Fetch trips from the database
        trips_list = [
            {
                'trip_name': trip.trip_name,
                'state': trip.state,
                'start_date': trip.start_date,
                'end_date': trip.end_date,
            }
            for trip in all_trips
        ] if all_trips else []

        # Pass trips_list to the template for rendering
        return render_template('trip/view_trips.html', trips=trips_list)
    except TemplateNotFound:
        abort(404)


@trip.route('/trip_details/', methods=['GET', 'POST'])
def trip_details():
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

        # Redirect to a summary or confirmation page
        return redirect(url_for('trip.view_trips'))

    # For a GET request, render the form with pre-filled data if available
    state = request.args.get('state', 'Default State')
    return render_template('trip/trip_details.html', state=state)


@trip.route('/search_hotel/', methods=['GET', 'POST'])
def search_hotel():
    error_message = None
    if request.method == 'POST':
        destination = request.form.get('destination')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Validation for missing fields
        if not destination or not start_date or not end_date:
            error_message = "All fields are required to search for hotels."
        else:
            # Add the hotel search logic here
            pass

    # Render the hotel_search.html template
    return render_template('trip/hotel_search.html', error=error_message)
