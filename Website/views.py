from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Admin, showListing, Theaters, Bookings, Super
import os
from . import db
import base64
from sqlalchemy import inspect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from Website import tasks

views = Blueprint('views', __name__)

def get_role():
   try: 
        if current_user:
            if current_user.role == 'admin':
                return 'admin'
        else:
            return redirect(url_for('admin_auth.login'))
        if current_user:
            if current_user.role == 'normal':
                return 'normal'
        else:
            return redirect(url_for('auth.login'))
        if current_user:
            if current_user.role == 'super':
                return 'admin'
        else:
            return redirect(url_for('super_auth.super_login'))
   except AttributeError:
       return redirect(url_for('auth.sign_up'))

@views.route('/', methods=['GET', 'POST'])
def home():
    user=None
    admin=None
    super=None
    query = request.form.get("search")
    print("q", query)
    movies = showListing.query.all()
    if query:
        movies = showListing.query.filter((showListing.show_name.like(query + '%'))).all()
    if current_user:
        if get_role() == 'normal':
            user = User.query.filter_by(id=current_user.id).first()
        if get_role() == 'admin':
            admin = Admin.query.filter_by(id=current_user.id).first()
        if get_role() == 'super':
            super = Super.query.first()
    else:   
        return redirect(url_for('auth.sign_up'))
    movies = showListing.query.all()
    if query:
        return redirect(url_for('views.search', query=query))
    return render_template('movies.html', user=user, movies=movies, admin=admin, super=super, query=query)


@views.route('/bookings', methods=['GET', 'POST'])
def booking():
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "movie@booking.com"
    SENDER_PASSWORD = ''
    
    movie_id = request.args.get('movie_id')
    admin = Admin.query.first()
    movies = showListing.query.filter_by(id=movie_id).first()
    if request.method=='POST':
        movie_id = request.args.get('movie_id')
        user_id = request.args.get("user_id")
        user_email = User.query.filter_by(id=user_id).first()
        seats = request.form.get('seats')
        movies = showListing.query.filter_by(id=movie_id).first()
        new_booking = Bookings(show_listing_id=movie_id, user_id=user_id, number_of_seats=seats, total_amount=((int(seats)*movies.price)))
        theater = Theaters.query.filter_by(name=movies.theater_name).first()
        
        msg = MIMEMultipart()
        msg["FROM"]=SENDER_ADDRESS
        msg["To"]=user_email.email
        msg["Subject"]= "Your booking for " + movies.show_name + " at " + movies.theater_name + " is confirmed. The amount of booking for " + str(seats) + " seats " + " is " + str(int(seats)*movies.price) +"."
        s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
        s.login(SENDER_ADDRESS, SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        
        if theater.total_business:
            theater.total_business += (int(seats)*movies.price)
        else:
            theater.total_business = 0
            theater.total_business += (int(seats)*movies.price)
        if movies.no_seats:
            if seats < movies.no_seats:
                movies.number_of_bookings += seats
                db.session.add(new_booking)
                db.session.commit()
            flash('No Seats available.', category='error')
        else:
            movies.no_seats = 100
            movies.no_seats -= seats
        return redirect(url_for('views.home'))
    return render_template('booking.html', user=current_user, movies=movies, admin=admin)


@views.route('/search', methods=['GET', 'POST'])
def search():
    user=None
    admin=None
    super=None
    query = request.args.get("query")
    print("q", query)
    movies = showListing.query.all()
    theater = Theaters.query.all()
    if query:
        movies = showListing.query.filter((showListing.show_name.like(query + '%'))).all()
        theater = Theaters.query.filter((Theaters.address.like(query + '%'))).all()
    print(movies)
    if request.method=='POST':
        if current_user:
            if get_role() == 'normal':
                user = User.query.filter_by(id=current_user.id).first()
            if get_role() == 'admin':
                admin = Admin.query.filter_by(id=current_user.id).first()
            if get_role() == 'super':
                super = Super.query.first()
        else:
            return redirect(url_for('auth.sign_up'))
    return render_template('search.html', user=user, admin=admin, super=super, movies=movies, query=query, theaters=theater)


@views.route('/movie', methods=['GET', 'POST'])
def movie():
    user=None
    admin=None
    super=None
    movie_name = request.args.get("movie_name")
    movie = showListing.query.filter_by(show_name = movie_name).all()
    if current_user:
        if get_role() == 'normal':
            user = User.query.filter_by(id=current_user.id).first()
        if get_role() == 'admin':
            admin = Admin.query.filter_by(id=current_user.id).first()
        if get_role() == 'super':
            super = Super.query.first()
    else:   
        return redirect(url_for('auth.sign_up'))
    return render_template('movie.html', movie=movie)


def has_booked():
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "movie@booking.com"
    SENDER_PASSWORD = '123'
    mailhog_path = r'F:\Pranav project\from scratch\MailHog_windows_amd64.exe'
    smtp_server = [ mailhog_path ]
    subprocess.Popen(smtp_server)
    bookings = Bookings.query.all()
    booking_user_ids = []
    users = User.query.all()
    msg = MIMEMultipart()
    msg["FROM"]=SENDER_ADDRESS
    msg["To"]= []
    msg["Subject"]= "You worked hard for the past few days, may be now it's time for some entertainment. Visit http://127.0.0.1:5000/"
    s=smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    
    
    
    for booking in bookings:
        booking_user_ids.append(booking.user_id)
    for user in users:
        if user.id not in booking_user_ids:
            msg["To"].append(user.email)
            
    print(msg["To"])
    if len(msg["To"])>0:
        for mail in msg["To"]:
            msg["To"] = mail
            scheduler = BackgroundScheduler(daemon=True)
            scheduler.add_job(s.send_message, trigger='cron', hour=17, minute=0, kwargs=({'msg':msg}))  # 5:00 PM
            scheduler.start()
            print("Scheduler started")
            
@views.route("/hello", methods=['GET', 'POST'])
def hello():
    job = tasks.hello.delay()
    return str(job), 200