"""
Trip Planner Application
-------------------------
This is a Flask web application for the Trip Planner project, developed for CMSC 495 7380.
The application allows users to explore travel destinations, book flights, rent cars,
and book hotels, providing an integrated travel planning experience.

## Team Members
- Galia Adelshin (Project Manager)
- Terence Boyce (Test Director)
- Jared Brick (Software Developer)
- Xavier Watson (Software Developer)
- Greg Chelchowski (Requirements Manager/UX/UI Designer)

Course: CMSC 495 7380
"""

# Import necessary libraries and modules
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_migrate import Migrate
from flask import jsonify

# Initialize Flask app
app = Flask(__name__, template_folder='../templates')

app.secret_key = 'your_secret_key'  # Required for flashing messages

# Set up the database URI for SQLAlchemy
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'trip_planner.db')

# Ensure the instance folder exists (useful if it's not created in the repo)
os.makedirs(app.instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'),
                               nullable=False)  # Change location_id to destination_id
    price_per_night = db.Column(db.Float, nullable=False)

    # Relationship to connect back to the Destination
    destination = db.relationship('Destination',
                                  backref=db.backref('hotels', lazy=True))  # Relationship with Destination


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'),
                               nullable=False)  # Change location_id to destination_id
    price_per_day = db.Column(db.Float, nullable=False)
    destination = db.relationship('Destination',
                                  backref=db.backref('rentals', lazy=True))  # Relationship with Destination


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    departure_destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'),
                                         nullable=False)  # Reference to Departure Destination
    arrival_destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'),
                                       nullable=False)  # Reference to Arrival Destination
    price = db.Column(db.Float, nullable=False)
    departure_destination = db.relationship('Destination', foreign_keys=[departure_destination_id],
                                            backref=db.backref('departures',
                                                               lazy=True))  # Relationship with Departure Destination
    arrival_destination = db.relationship('Destination', foreign_keys=[arrival_destination_id],
                                          backref=db.backref('arrivals',
                                                             lazy=True))  # Relationship with Arrival Destination


with app.app_context():
    db.create_all()  # Create all tables in the database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan_trip/')
def destinations():
    # Query all destinations from the database
    all_destinations = Destination.query.all()

    # Convert each Destination instance to a dictionary
    destinations_list = [
        {
            'name': destination.name,
            'description': destination.description,
            'image_url': destination.image_url
        }
        for destination in all_destinations
    ]

    return render_template('plan_trip.html', destinations=destinations_list)

@app.route('/sign_up/')
def sign_up():
    return render_template('sign_up.html')

@app.route('/forgot_password/')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/view_trips/')
def view_trips():
    return render_template('view_trips.html')

@app.route('/account_settings/')
def account_settings():
    return render_template('account_settings.html')







if __name__ == '__main__':
    app.run(debug=True)
