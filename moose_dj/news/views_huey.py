from django.http import JsonResponse
import uuid
# from huey.contrib.djhuey import task, db_task

# from huey.contrib.djhuey import task, HUEY as huey
from django_huey import task, enqueue, get_queue

from time import sleep
from django.db import transaction
# import stamina

from moose_dj.news.models import TaskCollection

NUM_FAKE_TASKS = 3

# Configure Huey with SQLite backend
# from huey import SqliteHuey
# huey = SqliteHuey(filename="huey.db")

""""
Note: This is super broken.
"""

# @stamina.retry(on=TaskCollection.DoesNotExist, attempts=3)
@task()
def long_running_task(task_id):
    # Simulate a long-running task
    print(f"Task {task_id} STARTING:")

    sleep(1)

    with transaction.atomic():
        # Retrieve the TaskCollection instance
        task_collection = TaskCollection.objects.get(id=task_id)
        task_collection.increment_completed_tasks()
        task_collection.save()
        percentage_progress = task_collection.get_progress_percentage()

    print(f"Task {task_id} FINISHED: {percentage_progress=}")
    return "Task completed successfully"


def start_task(request):
    # print(huey)

    with transaction.atomic():
        task_id = str(uuid.uuid4())
        tc = TaskCollection.objects.create(
            id=task_id, total_tasks=NUM_FAKE_TASKS, completed_tasks=0
        )
        tc.save()


    all_iems = []
    for i in range(NUM_FAKE_TASKS):
        # Do some work here
        
        
        # long_running_task(task_id).get(blocking=False)
        # long_running_task(task_id).get(blocking=False, preserve=True)
        long_running_task(task_id)
        
        # x = c
        # all_iems.append(x.task)
        # enqueue(x.task)
        # enqueue(long_running_task(task_id).task)

        # scheduled_count : int = get_queue("first").scheduled_count()
        # scheduled : list = get_queue("first").scheduled()
        # pending : list = get_queue("first").pending()
        # all_results = get_queue("first").all_results()

        # Do work immediately
        # huey.execute(x.task)

        # Schedule work (background)
        # huey.add_schedule(x.task)
        # huey.enqueue(x.task)

    # Schedule work (background)

    f_scheduled_count : int = get_queue("first").scheduled_count()
    f_scheduled : list = get_queue("first").scheduled()
    f_pending : list = get_queue("first").pending()
    f_all_results = get_queue("first").all_results()


    # huey.schedule_items(all_iems)
    return JsonResponse({"task_id": task_id})


def get_task_status(request, task_id):
    with transaction.atomic():
        task_collection = TaskCollection.objects.get(id=task_id)

        if task_collection:
            percentage_progress = task_collection.get_progress_percentage()

            if percentage_progress == 100:
                result = "FIXME"
                return JsonResponse({"status": "completed", "result": result})
            else:
                # huey.signal()
                scheduled_count : int = get_queue("first").scheduled_count()
                scheduled : list = get_queue("first").scheduled()
                pending : list = get_queue("first").pending()
                all_results = get_queue("first").all_results()
                return JsonResponse(
                    {"status": "running", "progress": percentage_progress}
                )
        else:
            return JsonResponse({"status": "error", "message": "Task not found"})
