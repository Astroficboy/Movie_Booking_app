# celery_config.py
from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)
    celery.conf.enable_utc = False
    celery.conf.time_zone = "Asia/Kolkata"
    celery.conf.beat_schedule = {
    "has_booked": {
    "task": "has_booked",
    "schedule": crontab(minute="28",hour="15"),
     },
    "export_theatre_details_to_csv": {
    "task": "export_theatre_details_to_csv",
    "schedule": crontab(minute="28", hour="15"),
     },
    }



    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
# CELERY INITIALIZATION END
