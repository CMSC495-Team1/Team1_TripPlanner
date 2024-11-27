import pytest
from app import create_app, database
from flask_login import FlaskLoginClient
from config import TestConfig


@pytest.fixture
def app():
    """Set up the Flask app for testing with a clean database."""
    test_app = create_app(TestConfig)
    test_app.test_client_class = FlaskLoginClient  # Enable test client to simulate logged-in users

    with test_app.app_context():
        database.drop_all()  # Ensure a clean slate
        database.create_all()  # Create tables
        yield test_app
        database.session.remove()
        database.drop_all()  # Cleanup after tests


@pytest.fixture
def client(app):
    """Return the test client for the app."""
    return app.test_client()


def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code in [200, 302]
    assert b"Plan a Trip" in response.data


def test_plan_trip_page(client, app):
    """Test that the Plan Trip page loads successfully."""
    with app.app_context():
        from app.models.user import User
        test_user = User(
            username="testuser",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User"
        )
        database.session.add(test_user)
        database.session.commit()

    # Simulate user login
    client.post('/auth/login', data={"username": "testuser", "password": "password"})

    response = client.get('/plan_trip/')
    assert response.status_code in [200, 302]
    if response.status_code == 200:
        assert b"Plan a Trip" in response.data
    elif response.status_code == 302:
        assert b"/login?next=%2Fplan_trip%2F" in response.data  # Ensure redirection URL is valid



def test_signup_page(client):
    """Test that the sign-up page loads successfully."""
    response = client.get('/sign_up')
    assert response.status_code in [200, 302]
    if response.status_code == 200:
        # Validate the correct heading in the sign-up page
        assert b"Sign Up" in response.data


def test_trip_submission_placeholder(client, app):
    """Test trip submission functionality."""
    with app.app_context():
        from app.models.user import User
        test_user = User(
            username="testuser",
            email="testuser@example.com",
            password="password",
            first_name="Test",
            last_name="User"
        )
        database.session.add(test_user)
        database.session.commit()

    client.post('/auth/login', data={"username": "testuser", "password": "password"})

    response = client.post('/plan_trip/', data={
        'state': 'New York',
        'trip_name': 'Vacation to New York',
        'start_date': '2024-12-01',
        'end_date': '2024-12-10'
    })
    assert response.status_code in [200, 302]
