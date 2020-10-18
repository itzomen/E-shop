import os
from celery import Celery

# Django default settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_shop.settings')
# initiating app instance
app = Celery('e_shop')
# Loading any custom configuration from e shop
app.config_from_object('django.conf:settings', namespace='CELERY')
# Setting Celery to auto discover asynchronous tasks for e shop
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')