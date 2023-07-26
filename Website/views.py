from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Admin
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    user = User.query.filter_by().first()
    admin = Admin.query.filter_by().first()
    return render_template('movies.html', user=current_user)

@views.route('/bookings', methods=['GET'])
def booking():
    user = User.query.filter_by().first()
    showName = request.form.get('showName')
    rating = request.form.get('rating')
    director = request.form.get('director')
    price = request.form.get('price')
        
    return render_template('booking.html', user=current_user)





