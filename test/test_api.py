import os
from dotenv import load_dotenv
import requests  # Make sure this line is included


# Load environment variables from the .env file
load_dotenv()
# Define the authorization headers with your GitHub Personal Access Token (PAT)
# Get the token from an environment variable
token = os.getenv("GITHUB_TOKEN")  # Make sure you set this in your environment

headers = {
    "Authorization": f"Bearer {token}"  # Fetch the token from the environment
}

# Make the GET request to your API
response = requests.get("http://localhost:5000/locations", headers=headers)

# Print the response status and body for debugging
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")

# Check that the status code is 200 (OK)
assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

# Check that the response is not empty
assert response.json() is not None, "Expected JSON response but got None"