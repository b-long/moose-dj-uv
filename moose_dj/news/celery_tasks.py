# news/tasks.py

from time import sleep
import datetime
from celery import shared_task, group

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
