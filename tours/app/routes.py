from flask import render_template, redirect, url_for, request
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_required, login_user

from app import app, db
from .models import Tour, User, Booking


@app.route('/')
def index():
    tours = db.session.scalars(sa.select(Tour)).all()
    return render_template('index.html', tours=tours)


@app.route('/book', methods=['GET', 'POST'])
def book_tour():
    if request.method == 'POST':
        tour_id = request.form['tour_id']
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        booking_date = request.form['booking_date']
        num_people = request.form['num_people']

        new_booking = Booking(tour_id=tour_id, user_name=user_name, user_email=user_email, booking_date=booking_date,
                              num_people=num_people)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        tours = Tour.query.all()
        return render_template('book.html', tours=tours)


@app.route('/bookings')
def bookings():
    bookings = Booking.query.all()
    return render_template('bookings.html', bookings=bookings)


