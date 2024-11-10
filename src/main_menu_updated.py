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


# Route for the home page
@app.route('/')
def home():
    return """
    <h1>Trip Planner Application</h1>
    <ul>
        <li><a href="/flights">Book a Flight</a></li>
        <li><a href="/rentals">Rent a Car</a></li>
        <li><a href="/hotels">Book a Hotel</a></li>
        <li><a href="/destinations">Explore Destinations</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/create_account">Create Account</a></li>
    </ul>
    """


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        new_customer = Customer(username=username, email=email, password=hashed_password)

        db.session.add(new_customer)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('home'))

    return """
    <h1>Create Account</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <input type="submit" value="Create Account">
    </form>
    """


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        customer = Customer.query.filter_by(username=username).first()

        if customer and check_password_hash(customer.password, password):
            flash(f"Logged in as {username}", "success")
            return redirect(url_for('home'))
        else:
            flash("Login failed. Check your username and/or password.", "danger")
            return redirect(url_for('login'))

    return """
    <h1>Login</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    """


@app.route('/flights')
def flights():
    return render_template('flights.html')


@app.route('/rentals')
def rentals():
    return render_template('rentals.html')


@app.route('/hotels')
def hotels():
    return render_template('hotels.html')


@app.route('/destinations')
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


if __name__ == '__main__':
    app.run(debug=True)
