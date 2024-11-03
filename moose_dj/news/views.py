from uuid import uuid4
import threading
from time import sleep
from django.http import JsonResponse
from django.core.cache import cache


# This can be taken all the way down to 1, and our tests for
# an immediate response will still pass
NUM_FAKE_TASKS = 2

DEAMON_MODE = True

lock = threading.Lock()  # Lock for thread safety with cache access


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task_id, future):
        self.tasks[task_id] = future

    def get_task_status(self, task_id):
        if task_id in self.tasks:
            future = self.tasks[task_id]
            try:
                result = future.result()
                del self.tasks[task_id]  # Remove completed task
                return {'status': 'completed', 'result': result}
            except Exception as e:
                # Handle exceptions, e.g., TimeoutError
                return {'status': 'error', 'message': 'Task failed'}
        else:
            return {'status': 'error', 'message': 'Task not found'}


task_manager = TaskManager()


def run_task(task_id):
    # Simulate a long-running task
    progress = 0
    with lock:
        cache.set(task_id, {'progress': progress}, timeout=3600)
    for i in range(NUM_FAKE_TASKS):
        # Do some work
        progress = (i * (100 / NUM_FAKE_TASKS))
        with lock:
            cache.set(task_id, {'progress': progress}, timeout=3600)
        print(f"{progress=}", flush=True)
        sleep(1)

    with lock:
        cache.set(task_id, {'result': 'Task completed'}, timeout=3600)


def start_task(request):
    task_id = str(uuid4())  # Generate a unique ID for the task

    # Store initial task state in the cache
    with lock:
        cache.set(task_id, {'progress': 0}, timeout=3600)

    # Start the task in a separate thread
    future = threading.Thread(target=run_task, args=(task_id,), daemon=DEAMON_MODE)
    future.start()

    task_manager.add_task(task_id, future)

    return JsonResponse({'task_id': task_id})


def get_task_status(request, task_id):
    task_data = None
    with lock:
        task_data = cache.get(task_id)

    if task_data:
        if 'result' in task_data:
            return JsonResponse({'status': 'completed', 'result': task_data['result']})
        else:
            return JsonResponse({'status': 'running', 'progress': task_data['progress']})
    else:
        return JsonResponse({'status': 'error', 'message': 'Task not found'})