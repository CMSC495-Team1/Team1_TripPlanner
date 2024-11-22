import pytest
from flask import Flask, render_template, url_for
import sys
from pathlib import Path
from app import create_app

# Add the project root to the Python path to resolve module imports
sys.path.append(str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def app():
    # Set up the Flask app for testing
    app = create_app()
    app.config['TESTING'] = True

    # Use the same database path as the application
    REPO_ROOT = Path(__file__).resolve().parent.parent
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{REPO_ROOT / 'app' / 'instance' / 'app.db'}"

    yield app


@pytest.fixture
def client(app):
    return app.test_client()  # Flask test client to interact with the app


# Test for rendering the Plan Trip page with state options
def test_plan_trip_page(client):
    response = client.get('/plan_trip/')
    assert response.status_code == 200  # Ensure the page loads correctly

    # Check that the destination selection dropdown is present
    assert b'<select' in response.data
    assert b'Alabama' in response.data  # Example state in the dropdown


# Test that selecting a state updates the destination image and details
def test_select_state(client):
    response = client.get('/plan_trip/', query_string={'state': 'New York'})
    assert response.status_code == 200  # Ensure the page loads correctly

    # Verify the selected state's image and description
    assert b'New York' in response.data
    assert b'new_york.jpg' in response.data  # Adjust based on actual content


# Test the functionality of the buttons (e.g., starting the planning process)
def test_start_planning_button(client):
    response = client.post('/plan_trip/', data={
        'state': 'New York',
        'trip_name': 'Vacation to New York',
        'start_date': '2024-12-01',
        'end_date': '2024-12-10'
    })
    assert response.status_code in [200, 302]  # Check for success or redirect

    # Check that the form was submitted and redirected (adjust based on your app's behavior)
    assert response.status_code in [200, 302]  # Handle redirect status code if applicable


# Test if the trip details are populated and buttons work as expected
def test_trip_details(client):
    # Simulate selecting a state and submitting trip details
    response = client.post('/plan_trip/', data={
        'state': 'New York',
        'trip_name': 'Vacation',
        'start_date': '2024-11-20',
        'end_date': '2024-11-30'
    })

    # Check for redirect to trip details
    assert response.status_code == 302  # HTTP status for redirection
    assert '/view_trips/?page=view_trips' in response.headers['Location']


def test_plan_trip_missing_fields(client):
    response = client.post('/plan_trip/', data={
        'trip_name': '',
        'start_date': '',
        'end_date': ''
    })
    assert b"Please give the trip a name." in response.data
    assert response.status_code == 200


# Test for rendering the Sign-Up page
def test_sign_up_page(client):
    response = client.get('/sign_up/')
    assert response.status_code == 200  # Ensure the page loads correctly
    assert b'Sign Up' in response.data  # Check if the page contains "Sign Up"


# Test for rendering the Forgot Password page
def test_forgot_password_page(client):
    response = client.get('/forgot_password/')
    assert response.status_code == 200  # Ensure the page loads correctly
    assert b'Forgot Password' in response.data  # Check if the page contains "Forgot Password"


# Test for rendering the Account Settings page
def test_account_settings_page(client):
    response = client.get('/account_settings/')
    assert response.status_code == 200  # Ensure the page loads correctly
    assert b'Account Settings' in response.data  # Check if the page contains "Account Settings"


# Test for rendering the View Trips page
def test_view_trips_page(client):
    response = client.get('/view_trips/')
    assert response.status_code == 200  # Ensure the page loads correctly
    assert b'Upcoming Trips' in response.data  # Check if the page contains "Upcoming Trips"


# Test the Trip Details page with missing required fields
def test_hotel_booking_missing_fields(client):
    response = client.post('/search_hotel/', data={
        'destination': '',
        'start_date': '',
        'end_date': ''
    })
    print(response.data.decode())  # Debug output
    assert response.status_code == 200  # Ensure the form reloads with errors
    assert b"All fields are required to search for hotels." in response.data


# Test for invalid dates in trip planning
def test_trip_invalid_dates(client):
    response = client.post('/plan_trip/', data={
        'state': 'California',
        'trip_name': 'Test Trip',
        'start_date': '2024-12-31',
        'end_date': '2024-12-01'  # End date is before start date
    }, follow_redirects=True)

    assert response.status_code == 200  # Ensure the page reloads with errors
    assert b"Start Date cannot be after the End Date." in response.data


# Test for rendering the main index page
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200  # Ensure the page loads correctly
    assert b'Plan a Trip' in response.data  # Check for the "Plan a Trip" button


# Test for rendering the Trip Confirmation page after a complete booking flow
def test_booking_confirmation_page(client):
    # Simulate booking a trip
    client.post('/plan_trip/', data={
        'state': 'Florida',
        'trip_name': 'Vacation to Florida',
        'start_date': '2024-11-25',
        'end_date': '2024-12-05'
    })
    response = client.get('/view_trips/')
    assert response.status_code == 200  # Ensure the trips page loads correctly
    assert b'Upcoming Trips' in response.data


# Test for rendering static assets
def test_static_assets(client):
    response = client.get('/main/static/script.js')
    assert response.status_code == 200  # Ensure the JS file is served correctly

    response = client.get('/main/static/style.css')
    assert response.status_code == 200  # Ensure the CSS file is served correctly
