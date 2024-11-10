import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
def test_get_locations():
    # Get the token from the environment variable (ensure you set this in your environment)
    token = os.getenv("GITHUB_TOKEN")  # Replace with the environment variable storing the token

    # Ensure the token is available
    if not token:
        raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")

    # Set headers with the token
    headers = {
        "Authorization": f"Bearer {token}"  # Use the token from the environment variable
    }

    # Make the GET request to the API
    response = requests.get("http://localhost:5000/locations", headers=headers)

    # Check status code
    assert response.status_code == 200, "Expected status code 200"

    # Check that the response is a non-empty JSON list
    data = response.json()
    assert len(data) > 0, "Expected non-empty response data"

    # Check that the first item contains the expected keys
    first_item = data[0]
    assert "location_id" in first_item, "Expected 'location_id' in response"
    assert "name" in first_item, "Expected 'name' in response"
