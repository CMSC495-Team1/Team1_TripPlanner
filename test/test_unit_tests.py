import os
import sys
import pytest

# Add the directory containing the app module to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app  # Ensure this matches the structure of your project

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_start_planning_button(client):
    response = client.post('/plan_trip/', data={
        'state': 'New York',
        'trip_name': 'Vacation to New York',
        'start_date': '2024-12-01',
        'end_date': '2024-12-10'
    })
    assert response.status_code in [200, 302]  # Check for success or redirect

def test_user_registration(client):
    response = client.post('/register/', data={
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'testuser@example.com'
    })
    assert response.status_code == 200  # Check for successful registration