# news/tasks.py

from time import sleep
import datetime
from celery import shared_task, group
from celery.result import GroupResult

@shared_task()
def long_running_process(data: list):
    """Fake a long-running task."""
   
    job = group([process_item.s(item) for item in data])
    group_result = job.apply_async()
    return group_result.id

@shared_task()
def process_item(item):
    # Perform the actual work here
    sleep_time = 2
    sleep(sleep_time) # Simulate a long-running operation by sleeping for 13 seconds
    now_time = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")

    return {
        "item": item,
        "sleep_time": sleep_time,
        "now": now_time
    }

# from celery import shared_task, task
# @shared_task()
# def send_feedback_email_task(email_address, message):
#     """Fake a long-running task."""
#     sleep(20)  # Simulate expensive operation(s) that freeze Django
#     email = f"{email_address=}, {message=}"
#     print(f"Sending email {email}")

#     return email
