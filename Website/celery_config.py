# celery_config.py
from celery import Celery

celery = Celery("Application jobs")
CELERY_BROKER_URL = "redis://localhost:6380/1"
CELERY_RESULT_BACKEND = "redis://localhost:6380/2"


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    return celery
