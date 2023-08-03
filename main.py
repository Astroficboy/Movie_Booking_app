from Website import create_app, create_default_user
from Website.workers import celery
from Website.tasks import has_booked, check_task_status, send_report
from Website.celery_config import celery, make_celery
import redis

app, celery = create_app()
app.config['CELERY_BROKER_URL'] = "redis://localhost:6380"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6380"
celery = make_celery(app)

if  __name__ == '__main__':
    with app.app_context():
        r = redis.StrictRedis(host='localhost', port=6380, db=0)
        r.ping()
        has_booked()
        send_report("Website/templates/report.html")
        create_default_user()
        print("super user created")
    app.run(debug = True)

