import os

from celery import Celery
from celery.schedules import crontab, timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')

app = Celery('project_manager')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "clean-old-logs": {
        "task": "logs.tasks.clean_logs",
        "schedule": crontab(hour=3, minute=0),  # каждый день в 03:00
    },
}