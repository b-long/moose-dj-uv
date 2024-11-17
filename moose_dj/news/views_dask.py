from uuid import uuid4
from django.http import JsonResponse
from dask.distributed import Client
import time

# Initialize Dask client
client = Client(n_workers=8, threads_per_worker=2)

NUM_FAKE_TASKS = 25

# Dictionary to store futures with task_id as key
task_futures = {}


def long_running_process(work_list):
    def task_function(task):
        time.sleep(2)
        return task

    futures = [client.submit(task_function, task) for task in work_list]
    return futures


async def start_task(request):
    work_list = []

    for t in range(NUM_FAKE_TASKS):
        task_id = str(uuid4())  # Generate a unique ID for the task
        work_list.append(
            {"address": f"foo--{t}@example.com", "message": f"Mail task: {task_id}"}
        )

    futures = long_running_process(work_list)
    dask_task_id = futures[0].key  # Use the key of the first future as the task ID

    # Store the futures in the dictionary with task_id as key
    task_futures[dask_task_id] = futures

    return JsonResponse({"task_id": dask_task_id})


async def get_task_status(request, task_id):
    futures = task_futures.get(task_id)

    if futures:
        if not all(future.done() for future in futures):
            progress = 0
            return JsonResponse({"status": "running", "progress": progress})
        else:
            results = client.gather(futures, asynchronous=False)
            progress = 100
            return JsonResponse(
                {
                    "task_id": task_id,
                    "status": "completed",
                    "progress": progress,
                    "results": results,
                }
            )
    else:
        return JsonResponse({"status": "error", "message": "Task not found"})
