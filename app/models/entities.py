from flask_sqlalchemy import SQLAlchemy
from app.extensions.db import db

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
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    destination = db.relationship('Destination', backref=db.backref('hotels', lazy=True))

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    destination = db.relationship('Destination', backref=db.backref('rentals', lazy=True))

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100), nullable=False)
    departure_destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    arrival_destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    departure_destination = db.relationship('Destination',
                                            foreign_keys=[departure_destination_id],
                                            backref=db.backref('departures', lazy=True))
    arrival_destination = db.relationship('Destination', foreign_keys=[arrival_destination_id],
                                          backref=db.backref('arrivals', lazy=True))

