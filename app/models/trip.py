from app import database
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey
from typing import Optional
from datetime import datetime


class Trip(database.Model):
    __tablename__ = 'trips'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trip_name: Mapped[str] = mapped_column(String(100), nullable=False)
    destination: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    options: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="trips")

    def __repr__(self) -> str:
        return f"<Trip('{self.trip_name}', '{self.destination}', '{self.start_date}', '{self.end_date}')>"
