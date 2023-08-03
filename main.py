# main.py
from Website import create_app
from Website.tasks import has_booked, export_theatre_details_to_csv
from Website.celery_config import make_celery
from celery.schedules import crontab


#celery -A main.celery worker -l info -P gevent --pool=solo   
#celery -A app.celery beat  --loglevel=info
# gevent
# wait.apply_async(countdown=4).wait()


app = create_app()
celery = make_celery(app)

if __name__ == '__main__':
    with app.app_context():
        # Start the Celery beat scheduler
        celery.conf.beat_schedule = {
            "export_theatre_details_to_csv": {
                "task": "export_theatre_details_to_csv",
                "schedule": 60 * 60 * 24,  # Run every 24 hours
            },
            "has_booked": {
                "task": "has_booked",
                "schedule": 10,  # First day of the month at midnight
            },
        }
        celery.conf.timezone = "Asia/Kolkata"
        # celery.worker_main(argv=['worker'])
        app.run(debug=True)
        # Start the Celery worker (if needed)
        # celery.worker_main(argv=['worker', '--beat'])
