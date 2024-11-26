from flask_login import UserMixin
from datetime import datetime, timezone
import secrets
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from typing import Optional
from sqlalchemy.orm import relationship
import app

from app import database, bcrypt

# 30 minutes in seconds
THIRTY_MINUTES = 1800

@app.login.user_loader
def load_user(user_id):
    return database.session.get(User,int(user_id))


class User(database.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    reset_token: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    reset_token_expiration: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, first_name: str, last_name: str, username: str, email: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
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

    def get_reset_token(self, expires_sec: int = THIRTY_MINUTES) -> str:
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
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token, max_age=THIRTY_MINUTES)['user_id']
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
