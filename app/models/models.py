from flask_sqlalchemy import SQLAlchemy
from app import database

class Customer(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    password = database.Column(database.String(80), nullable=False)

class Destination(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), unique=True, nullable=False)
    description = database.Column(database.String(500), nullable=False)
    image_url = database.Column(database.String(500), nullable=True)

class Hotel(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
    price_per_night = database.Column(database.Float, nullable=False)
    destination = database.relationship('Destination', backref=database.backref('hotels', lazy=True))

class Rental(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    company_name = database.Column(database.String(100), nullable=False)
    destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
    price_per_day = database.Column(database.Float, nullable=False)
    destination = database.relationship('Destination', backref=database.backref('rentals', lazy=True))

class Flight(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    airline = database.Column(database.String(100), nullable=False)
    departure_destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
    arrival_destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
    price = database.Column(database.Float, nullable=False)
    departure_destination = database.relationship('Destination',
                                            foreign_keys=[departure_destination_id],
                                            backref=database.backref('departures', lazy=True))
    arrival_destination = database.relationship('Destination', foreign_keys=[arrival_destination_id],
                                          backref=database.backref('arrivals', lazy=True))

