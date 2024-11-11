import requests  # Make sure this line is included

# Define the authorization headers with your GitHub Personal Access Token (PAT)
headers = {
    "Authorization": "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"  # Replace with your actual token
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