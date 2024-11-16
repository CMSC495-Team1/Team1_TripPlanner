from typing import Optional
from sqlalchemy import String as sqlString
import sqlalchemy.orm as orm
from app import database

class User(database.Model):
    """
    Mapped is a type hint provided by SQLAlchemy's ORM (Object Relational Mapper) to indicate that a class attribute
    is mapped to a database column. It is used to provide type information for the attribute, which helps with type
    checking and code completion in IDEs. For example, Mapped[int] indicates that the id attribute is mapped to a
    database column and is expected to be of type int. The orm.mapped_column function is used to define the specifics of
    the column, such as whether it is a primary key, its data type, and other constraints.
    """

    id: orm.Mapped[int] = orm.mapped_column(primary_key = True)

    username: orm.Mapped[str] = orm.mapped_column(sqlString(256),
                                                  index = True,
                                                  unique = True,
                                                  nullable = False)

    email: orm.Mapped[str] = orm.mapped_column(sqlString(256),
                                               index = True,
                                               unique = True,
                                               nullable = False)
    # Optional allows the column to be empty.
    password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sqlString(256))

    # __repr__ method tells Python how to print objects of this class, which is going to be useful for debugging.
    def __repr__(self):
        return f'<Use {self.username}>'

class Destination(database.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key = True)

    country: orm.Mapped[Optional[str]] = orm.mapped_column(sqlString(256),
                                                           index=True,
                                                           unique=True)

    state: orm.Mapped[Optional[str]] = orm.mapped_column(sqlString(256),
                                                         index=True,
                                                         unique=True)

    city: orm.Mapped[Optional[str]] = orm.mapped_column(sqlString(256), index= True)

    description: orm.Mapped[Optional[str]] = orm.mapped_column(sqlString(512))

    image_filename: orm.Mapped[Optional[str]] = orm.mapped_column(sqlString(256))

    def __repr__(self):
        return f'<Destination: {self.country}, {self.state}, {self.city}>'

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
