from uuid import uuid4
from django.http import JsonResponse
from moose_dj.news.celery_tasks import long_running_process
from celery.result import AsyncResult

# NOTE: This can be taken all the way down to 1, and our tests for
# an immediate response will still pass
NUM_FAKE_TASKS = 25
# NOTE: Tests pass with 'DEAMON_MODE' set to True or False.
DEAMON_MODE = True


def start_task(request):
    """
    Calling .delay() is the quickest way to send a task message to Celery. This
    method is a shortcut to the more powerful .apply_async(), which additionally
    supports execution options for fine-tuning your task message.

    More info:
    - https://realpython.com/asynchronous-tasks-with-django-and-celery/#handle-workloads-asynchronously-with-celery:~:text=Calling%20.delay()%20is%20the%20quickest
    """
    work_list: list = []

    for t in range(NUM_FAKE_TASKS):
        task_id = str(uuid4())  # Generate a unique ID for the task

        work_list.append(
            {"address": f"foo--{t}@example.com", "message": f"Mail task: {task_id}"}
        )

    response = long_running_process.delay(work_list)
    celery_task_id = response.task_id
    return JsonResponse({"task_id": celery_task_id})


def get_task_status(request, task_id):
    # group_result = GroupResult(task_id)
    group_result = AsyncResult(task_id)

    if group_result:
        if group_result.status == "PENDING":
            progress = 0
            return JsonResponse({"status": "running", "progress": progress})
        else:
            result = group_result.children[0]
            # Calculate progress based on completed subtasks
            # measured_work = result.children[0].children

            total_subtasks = len(result.children)
            completed_subtasks = sum(1 for child in result.children if child.ready())
            progress = (completed_subtasks / total_subtasks) * 100

            print("Results")
            print(result.results)
            print(f"{progress=}")

            return JsonResponse(
                {
                    "task_id": task_id,
                    "status": "completed" if int(progress) == 100 else "running",
                    "progress": progress,
                }
            )
    else:
        return JsonResponse({"status": "error", "message": "Task not found"})
