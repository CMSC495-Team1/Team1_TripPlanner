import requests

def test_get_hotels():
    headers = {
        "Authorization": "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"  # Replace with a valid token
    }
    response = requests.get("http://localhost:5000/hotels", headers=headers)
    assert response.status_code == 200  # Check that the response is OK
    assert len(response.json()) > 0  # Check that data is returned