from .celery import app as celery_app

"""
Based on:

- https://realpython.com/asynchronous-tasks-with-django-and-celery/#handle-workloads-asynchronously-with-celery:~:text=To%20make%20sure%20that%20your%20Celery%20app%20is%20loaded%20when%20you%20start%20Django

To make sure that our Celery app is loaded when we start 
Django, we add it to __all__:

More info:
- https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
"""
__all__ = ("celery_app",)
