# main.py
from __future__ import absolute_import
from Website import create_app
from Website.tasks import has_booked, export_theatre_details_to_csv
from Website.celery_config import make_celery
from celery.schedules import crontab


#celery -A main.celery worker -l info -P gevent --pool=solo   
#celery -A main.celery beat  --loglevel=info
# gevent
# wait.apply_async(countdown=4).wait()


app = create_app()
# app.config["CELERY_CONFIG"] = {"broker_url": "redis://127.0.0.1:6379", "result_backend": "redis://127.0.0.1:6379",}
celery = make_celery(app)

if __name__ == '__main__':
    with app.app_context():
        celery
        # Start the Celery beat scheduler
        celery.conf.beat_schedule = {
            "export_theatre_details_to_csv": {
                "task": "export_theatre_details_to_csv",
                "schedule": 10,  # Run every 24 hours
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
