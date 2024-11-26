import pytest
from app import create_app, db
from app.instance.models.models import Flight, Destination

@pytest.fixture
def client():
    """
    Sets up a test client for the application.
    """
    app = create_app('config.TestingConfig')  # Ensure your create_app function accepts 'TestingConfig'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables in the in-memory database
            populate_mock_data()  # Populate test data
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Cleanup the database


def populate_mock_data():
    """
    Populates the in-memory database with mock flight data for testing.
    """
    # Add destinations
    nyc = Destination(id=1, country='USA', state='NY', city='New York', description='City in NY', image_filename='nyc.jpg')
    la = Destination(id=2, country='USA', state='CA', city='Los Angeles', description='City in CA', image_filename='la.jpg')
    db.session.add_all([nyc, la])
    
    # Add flights
    flight1 = Flight(airline='Delta', departure_destination_id=1, arrival_destination_id=2, price=300)
    db.session.add(flight1)
    
    db.session.commit()


def test_one_way_flight_search(client):
    """
    Test a one-way flight search.
    """
    response = client.post('/search_flights/', json={
        'departure_city': 'New York',
        'arrival_city': 'Los Angeles',
        'date': '2024-12-01',
        'round_trip': False
    })
    
    assert response.status_code == 200, "Response status should be 200 for a valid search"
    data = response.get_json()
    assert 'flights' in data, "Response JSON should contain 'flights' key"
    assert len(data['flights']) > 0, "At least one flight should be returned"
    
    flight = data['flights'][0]
    assert flight['airline'] == 'Delta', "Expected airline is 'Delta'"
    assert flight['departure_city'] == 'New York', "Expected departure city is 'New York'"
    assert flight['arrival_city'] == 'Los Angeles', "Expected arrival city is 'Los Angeles'"
    assert flight['price'] == 300, "Expected flight price is 300"


def test_round_trip_flight_search(client):
    """
    Test a round-trip flight search.
    """
    response = client.post('/search_flights/', json={
        'departure_city': 'New York',
        'arrival_city': 'Los Angeles',
        'date': '2024-12-01',
        'return_date': '2024-12-10',
        'round_trip': True
    })
    
    assert response.status_code == 200, "Response status should be 200 for a valid search"
    data = response.get_json()
    assert 'flights' in data, "Response JSON should contain 'flights' key"
    assert len(data['flights']) > 0, "At least one flight should be returned"

    round_trip_flights = [flight for flight in data['flights'] if flight.get('type') == 'return']
    assert len(round_trip_flights) > 0, "At least one return flight should be included"

    for flight in round_trip_flights:
        assert flight['departure_city'] == 'Los Angeles', "Return flight departure city should be 'Los Angeles'"
        assert flight['arrival_city'] == 'New York', "Return flight arrival city should be 'New York'"