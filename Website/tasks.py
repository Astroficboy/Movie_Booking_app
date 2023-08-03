from email.mime.multipart import MIMEMultipart
import smtplib
import subprocess
from Website.celery_config import celery
from flask import current_app as app
from .models import User, Admin, showListing, Theaters, Bookings
from apscheduler.schedulers.background import BackgroundScheduler
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from Website.models import Theaters, showListing, Bookings
import csv

@celery.task()
def export_theatre_details_to_csv(theatre_id):
    theater = Theaters.query.get(theatre_id)
    if not theater:
        return "Theater not found"

    filename = f"{theater.name}_details.csv"

    # Fetch required data from the database
    num_shows = showListing.query.filter_by(theater_name=theater.name).count()
    num_bookings = showListing.query.filter_by(theater_name=theater.name).count()
    # avg_rating = Rating.query.filter_by(id=theatre_id).average('rating')

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Theatre Name', 'Number of Shows', 'Number of Bookings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'Theatre Name': theater.name,
            'Number of Shows': num_shows,
            'Number of Bookings': num_bookings,
            # 'Average Rating': avg_rating,
        })

    return filename

@celery.task()
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
            user_scheduler = BackgroundScheduler(daemon=True)
            user_scheduler.add_job(s.send_message, trigger='cron', hour=17, minute=0, kwargs=({'msg':msg}))  # 5:00 PM
            user_scheduler.start()
            print("Scheduler started")
    else:
        print("Nothing to scedule")
    return("from celery task")



@celery.task()
def send_report(html_file_path):
    admin = Admin.query.all()
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "movie@booking.com"
    SENDER_PASSWORD = '123'
    RECEIVER_ADDRESS = "recipient@example.com"

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = RECEIVER_ADDRESS
    msg["Subject"] = "Monthly Entertainment Report"

    with open(html_file_path, 'r') as file:
        html_content = file.read()
        msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT) as server:
        for admin_email in admin:
            server.login(SENDER_ADDRESS, SENDER_PASSWORD)
            RECEIVER_ADDRESS = admin_email.email
            server.sendmail(SENDER_ADDRESS, RECEIVER_ADDRESS, msg.as_string())

# Schedule the function to run on the first day of each month at 12:00 AM
    admin_scheduler = BackgroundScheduler(daemon=True)
    admin_scheduler.add_job(send_report, trigger='cron', day='1', hour='0', minute='0', args=[r'Website\templates\report.html'])
    admin_scheduler.start()
    print("Admin report schedule has started.")

# Keep the script running


# Add this function to check the status and result of the task
def check_task_status(task_id):
    task = has_booked.AsyncResult(task_id)
    if task.state == "SUCCESS":
        print("Task completed successfully!")
        result = task.get()  # Get the result of the task
        print("Result:", result)
    elif task.state == "FAILURE":
        print("Task failed!")
        print("Exception:", task.result)  # The exception raised by the task (if any)
    else:
        print("Task is still running...")
