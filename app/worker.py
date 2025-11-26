# Small file so you can also run: celery -A app.worker.celery worker
from app.celery_app import celery

# No extra code needed; Celery uses this module entry.
