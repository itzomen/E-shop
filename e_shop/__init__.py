
# Load celery each time django starts
from .celery import app as celery_app

__all__ = ('celery_app',)
