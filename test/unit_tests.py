import sys
import os
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Import the necessary modules from main_menu_updated.py
from src.main_menu_updated import app, db, Customer, Destination


# Setting up the test client
@pytest.fixture
def client():
    with app.test_client() as client:
        # Set up an app context, so db operations can be used
        with app.app_context():
            db.create_all()  # Create all tables for testing
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after the test


# --- TEST 1: Home Page ---
def test_home_page(client):
    """Test if the Home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Plan a Trip' in response.data  # Check if the "Plan a Trip" button is present


# --- TEST 2: Account Creation Page ---
def test_create_account_page(client):
    """Test if the Create Account page loads correctly."""
    response = client.get('/sign_up/')
    assert response.status_code == 200





