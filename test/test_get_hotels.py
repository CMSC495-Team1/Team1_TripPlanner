import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
def test_get_hotels():
    # Get the token from the environment variable (ensure you set this in your environment)
    token = os.getenv("GITHUB_TOKEN")  # Replace with the environment variable storing the token

    # Ensure the token is available
    if not token:
        raise ValueError("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")

    # Set headers with the token
    headers = {
        "Authorization": f"ghp_{token}"  # Use the token from the environment variable
    }

    # Make the GET request to the hotels endpoint
    response = requests.get("http://localhost:5000/hotels", headers=headers)

    # Check that the response status is OK
    assert response.status_code == 200, "Expected status code 200"

    # Check that the response data is non-empty
    data = response.json()
    assert len(data) > 0, "Expected non-empty response data"
