from flask_login import UserMixin
from datetime import datetime, timezone
import secrets
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from typing import Optional

from app import database, bcrypt

class User(database.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    reset_token: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    reset_token_expiration: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def set_password(self, password: str) -> None:
        """
        Generates a hash for the given password and stores it.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """
        Checks if the provided password matches the stored hashed password.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec: int = 1800) -> str:
        """
        Generates a timed JSON Web Signature for password resets.
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token: str) -> Optional['User']:
        """
        Verifies the provided reset token and returns the associated user.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except (ValueError, KeyError):
            return None
        return User.query.get(user_id)

    @staticmethod
    def create_reset_token() -> str:
        """
        Generates a random token to use for password reset.
        """
        return secrets.token_urlsafe(32)

    def __repr__(self) -> str:
        return f"<User('{self.username}', '{self.email}')>"

class Destination(database.Model):
    __tablename__ = 'destinations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    country: Mapped[Optional[str]] = mapped_column(String(256), index=True, unique=True, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(256), index=True, unique=True, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(256), index=True, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    image_filename: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    def __repr__(self) -> str:
        return f"<Destination: {self.country}, {self.state}, {self.city}>"

# class Hotel(database.Model):
#     id = database.Column(database.Integer, primary_key=True)
#     name = database.Column(database.String(100), nullable=False)
#     destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
#     price_per_night = database.Column(database.Float, nullable=False)
#     destination = database.relationship('Destination', backref=database.backref('hotels', lazy=True))
#
# class Rental(database.Model):
#     id = database.Column(database.Integer, primary_key=True)
#     company_name = database.Column(database.String(100), nullable=False)
#     destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
#     price_per_day = database.Column(database.Float, nullable=False)
#     destination = database.relationship('Destination', backref=database.backref('rentals', lazy=True))
#
# class Flight(database.Model):
#     id = database.Column(database.Integer, primary_key=True)
#     airline = database.Column(database.String(100), nullable=False)
#     departure_destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
#     arrival_destination_id = database.Column(database.Integer, database.ForeignKey('destination.id'), nullable=False)
#     price = database.Column(database.Float, nullable=False)
#     departure_destination = database.relationship('Destination',
#                                             foreign_keys=[departure_destination_id],
#                                             backref=database.backref('departures', lazy=True))
#     arrival_destination = database.relationship('Destination', foreign_keys=[arrival_destination_id],
#                                           backref=database.backref('arrivals', lazy=True))
