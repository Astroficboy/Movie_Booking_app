from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Admin, showListing
import os
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    user = User.query.filter_by().first()
    admin = Admin.query.filter_by().first()
    movies = showListing.query.filter_by().first()
    return render_template('movies.html', user=current_user, movies=movies)

@views.route('/add_movies', methods=['GET', 'POST'])
def add_movies():
    admin = Admin.query.filter_by().first()
    if admin.is_authenticated:
        admin = Admin.query.filter_by(id=admin.id).first()
    else:
        return redirect(url_for('admin_auth.admin_login'))
    if request.method == 'POST':
        show_name = request.form.get('show_name')
        tags = request.form.get('tags')
        director = request.form.get('director')
        price = request.form.get('price')
        screen_no = request.form.get('screen_no')
        theater_name = request.form.get('theater_name')
        image = request.files['image']
        image = image.read()
        new_movie = showListing(show_name=show_name, tags=tags, director=director, theater_name=theater_name,
                                image=image, price=price, screen_no=screen_no)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()
    return render_template('add_movies.html', admin=admin)

@views.route('/bookings', methods=['GET'])
def booking():
    user = User.query.filter_by().first()
    showName = request.form.get('showName')
    rating = request.form.get('rating')
    director = request.form.get('director')
    price = request.form.get('price')
        
    return render_template('booking.html', user=current_user)





