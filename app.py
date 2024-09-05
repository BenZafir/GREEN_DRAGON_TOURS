from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migarte = Migrate(app, db)
IMAGE_FOLDER = os.path.join('static', 'images')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = False, nullable = False)
    start_date = db.Column(db.String(80), unique = False, nullable = False)
    end_date = db.Column(db.String(80), unique = False, nullable = False)
    destination_name = db.Column(db.String(80), unique = False, nullable = False)

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/destination/<destination_name>')
def trips(destination_name):
    bookings = Booking.query.filter_by(destination_name=destination_name).all()
    return render_template("destination.html", destination_name=destination_name, bookings=bookings)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    destination_name = request.form['destination_name']

    new_booking = Booking(name=name, start_date=start_date, end_date=end_date, destination_name=destination_name)

    db.session.add(new_booking)
    db.session.commit()

    return render_template("booking_success.html", destination_name=destination_name, name=name, start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    app.run(debug=True, port=5000)