from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Admin, showListing, Theaters, Bookings
import os
from . import db
import base64
from sqlalchemy import inspect

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    user = User.query.first()
    movies = showListing.query.all()
    return render_template('movies.html', user=current_user, movies=movies)


@views.route('/bookings', methods=['GET', 'POST'])
def booking():
    movie_id = request.args.get('movie_id')
    movies = showListing.query.filter_by(id=movie_id).first()
    if request.method=='POST':
        movie_id = request.args.get('movie_id')
        user_id = request.args.get("user_id")
        seats = request.form.get('seats')
        movies = showListing.query.filter_by(id=movie_id).first()
        new_booking = Bookings(show_listing_id=movie_id, user_id=user_id, number_of_seats=seats, total_amount=((int(seats)*movies.price)))
        theater = Theaters.query.filter_by(name=movies.theater_name).first()
        if theater.total_business:
            theater.total_business += (int(seats)*movies.price)
        else:
            theater.total_business = 0
            theater.total_business += (int(seats)*movies.price)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('booking.html', user=current_user, movies=movies)





