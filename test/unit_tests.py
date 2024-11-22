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
