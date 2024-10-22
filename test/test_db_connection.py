from sqlalchemy import create_engine

#This script tests whether the connection to the trip_planner.db SQLite database can be successfully established.
#It uses SQLAlchemy to create a connection engine and attempts to connect to the database.

# Define the path to the SQLite database file.
DB_PATH = "sqlite:///../src/database/trip_planner.db"

# Create an engine to connect to the SQLite database.
engine = create_engine(DB_PATH)

# Test the connection to the database.
try:
    with engine.connect() as connection:
        print("Database connection was successful!")
except Exception as e:
    print("Failed to connect to the database.")
    print(f"Error: {e}")
