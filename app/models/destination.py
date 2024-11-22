from app import database
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from typing import Optional

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
