from Website import create_app, create_default_user
from Website.views import has_booked
from Website.workers import celery
from Website.tasks import hello, check_task_status
from Website.celery_config import celery, make_celery
# from flask import current_app as app

app, celery = create_app()
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/2"
celery = make_celery(app)

if  __name__ == '__main__':
    with app.app_context():
        has_booked()
        
        task = hello.apply_async()
        task_id = task.id

        # Check the status and result of the task using the task ID
        check_task_status(task_id)
        create_default_user()
    print("super user created")
    app.run(debug = True)

