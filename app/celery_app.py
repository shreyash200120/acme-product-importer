from celery import Celery
import os

broker_url = os.getenv("BROKER_URL", os.getenv("REDIS_URL", "redis://redis:6379/0"))
backend_url = os.getenv("RESULT_BACKEND", broker_url)

celery = Celery(
    "acme_importer",
    broker=broker_url,
    backend=backend_url,
)

celery.conf.timezone = "UTC"
celery.conf.result_expires = 3600

# 🔴 IMPORTANT: tell Celery where to find tasks
# Option 1: autodiscover the app.services package
celery.autodiscover_tasks(["app.services"])

# Option 2 (extra safe): explicitly import modules so decorators run
from app.services import csv_importer, webhook_sender  # noqa: F401
