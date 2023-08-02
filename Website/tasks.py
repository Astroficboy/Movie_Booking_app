from Website.celery_config import celery
from flask import current_app as app

@celery.task()
def hello():
    print("inside task")
    return "Task completed successfully"

# Add this function to check the status and result of the task
def check_task_status(task_id):
    task = hello.AsyncResult(task_id)
    if task.state == "SUCCESS":
        print("Task completed successfully!")
        result = task.get()  # Get the result of the task
        print("Result:", result)
    elif task.state == "FAILURE":
        print("Task failed!")
        print("Exception:", task.result)  # The exception raised by the task (if any)
    else:
        print("Task is still running...")
