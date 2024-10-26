def test_get_locations():
    headers = {
        "Authorization": "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"  # Replace with a valid token if needed
    }
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