# Import necessary libraries and modules
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Set up the database URI for SQLAlchemy
# Here we're using SQLite as the database for simplicity.
# This database file will be named 'trip_planner.db' and will be stored in the same directory as the code.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/GaliaAdelshin/PycharmProjects/Team1_TripPlanner/src/instance/trip_planner.db'


# Track modifications of objects and emit signals - set to False for performance benefits.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Define the Customer model
# This table will store information about users who create accounts in our application.
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each customer
    username = db.Column(db.String(50), unique=True, nullable=False)  # Username must be unique and not null
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email must be unique and not null
    password = db.Column(db.String(80), nullable=False)  # Password field, storing hashed passwords in production is recommended

# Define the Location model
# This table will store information about the travel locations available to users.
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each location
    name = db.Column(db.String(100), unique=True, nullable=False)  # Name of the location
    description = db.Column(db.String(500), nullable=False)  # Description of the location

# Define the Hotel model
# This table will store information about hotels at various locations.
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each hotel
    name = db.Column(db.String(100), nullable=False)  # Name of the hotel
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)  # Foreign key referencing Location
    price_per_night = db.Column(db.Float, nullable=False)  # Price per night for the hotel

    # Relationship to establish connection back to Location
    location = db.relationship('Location', backref=db.backref('hotels', lazy=True))

# Define the Rental model
# This table will store information about car rental services available to users.
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each rental
    company_name = db.Column(db.String(100), nullable=False)  # Name of the rental company
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)  # Foreign key referencing Location
    price_per_day = db.Column(db.Float, nullable=False)  # Price per day for car rental

    # Relationship to establish connection back to Location
    location = db.relationship('Location', backref=db.backref('rentals', lazy=True))

# Define the Flight model
# This table will store information about flight options available to users.
class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key, unique identifier for each flight
    airline = db.Column(db.String(100), nullable=False)  # Name of the airline
    departure_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)  # Departure location foreign key
    arrival_location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)  # Arrival location foreign key
    price = db.Column(db.Float, nullable=False)  # Price of the flight

    # Relationships to establish connections back to Location
    departure_location = db.relationship('Location', foreign_keys=[departure_location_id], backref=db.backref('departures', lazy=True))
    arrival_location = db.relationship('Location', foreign_keys=[arrival_location_id], backref=db.backref('arrivals', lazy=True))

# Create all the tables in the database
# This line ensures that all tables defined above are created in the 'trip_planner.db' file.
with app.app_context():
    db.create_all()  # This ensures all tables are created within the context of the Flask app

# Route for the home page
# Displays the main options available in the Trip Planner Application
@app.route('/')
def home():
    return """
    <h1>Trip Planner Application</h1>
    <ul>
        <li><a href="/flights">Book a Flight</a></li>
        <li><a href="/rentals">Rent a Car</a></li>
        <li><a href="/hotels">Book a Hotel</a></li>
        <li><a href="/locations">Explore Locations</a></li>
    </ul>
    """

# Route for flights page
# Displays flight booking options
@app.route('/flights')
def flights():
    return "Flight booking options will be displayed here."

# Route for rentals page
# Displays car rental options
@app.route('/rentals')
def rentals():
    return "Car rental options will be displayed here."

# Route for hotels page
# Displays hotel booking options
@app.route('/hotels')
def hotels():
    return "Hotel booking options will be displayed here."

# Route for locations page
# Displays travel locations
@app.route('/locations')
def locations():
    # Query all locations from the Location table
    all_locations = Location.query.all()

    # Generate HTML content to display all locations
    location_list_html = "<h1>Explore Locations</h1><ul>"
    for loc in all_locations:
        location_list_html += f"<li>{loc.name}: {loc.description}</li>"
    location_list_html += "</ul>"

    return location_list_html


if __name__ == '__main__':
    # Run the Flask development server
    # Debug mode is enabled to provide detailed error messages during development
    app.run(debug=True)

# NOTES:
# 1. The above code connects the Trip Planner Application to an SQLite database, allowing you to store and retrieve data about customers, locations, hotels, rentals, and flights.
# 2. The `db.create_all()` method creates the necessary tables in the SQLite database.
# 3. Each table represents an entity in our Trip Planner Application: Customer, Location, Hotel, Rental, and Flight.
# 4. Relationships have been set between tables where necessary (e.g., hotels and rentals are linked to locations).
# 5. More tables can be added as needed, for example table for 'Reviews' to allow customers to leave reviews for hotels or locations.
# 6. The `Flight` table has two foreign keys to represent both departure and arrival locations, allowing better data modeling for flight routes.
