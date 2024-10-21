from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Trip Planner Application</h1>
    <ul>
        <li><a href="/flights">Book a Flight</a></li>
        <li><a href="/rentals">Rent a Car</a></li>
        <li><a href="/hotels">Book a Hotel</a></li>
        <li><a href="/locations">Explore Locations</a></li>
    </ul>
    """

@app.route('/flights')
def flights():
    return "Flight booking options will be displayed here."

@app.route('/rentals')
def rentals():
    return "Car rental options will be displayed here."

@app.route('/hotels')
def hotels():
    return "Hotel booking options will be displayed here."

@app.route('/locations')
def locations():
    return "Location options will be displayed here."

if __name__ == '__main__':
    app.run(debug=True)