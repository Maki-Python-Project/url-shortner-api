import os

from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

app = Celery('base')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'get_joke_3s': {
#         'task': 'api.tasks.get_joke',
#         'schedule': 3.0
#     }
# }


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
