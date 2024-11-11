import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moose_dj.settings")
app = Celery("moose_dj")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()