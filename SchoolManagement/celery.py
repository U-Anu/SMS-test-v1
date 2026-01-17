from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolManagement.settings')

app = Celery('SchoolManagement')

# Read config from Django settings with `CELERY_` namespace.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
app.conf.beat_schedule = {

    'Expiry-notification': {
        'task': 'sub_part.views.celery_call',
        'schedule': timedelta(seconds=30),
    },
}

app.conf.timezone = 'UTC'