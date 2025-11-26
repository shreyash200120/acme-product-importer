from app.celery_app import celery
from app.database import SessionLocal
from app.models import Webhook
import requests
import time


@celery.task(bind=True)
def send_webhook_task(self, url: str, payload: dict):
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=5)
        duration = time.time() - start
        return {
            "status_code": resp.status_code,
            "duration": duration,
            "text": resp.text[:300],
        }
    except Exception as e:
        return {"error": str(e)}


@celery.task
def send_event_webhook(event_type: str, data: dict):
    db = SessionLocal()
    try:
        hooks = (
            db.query(Webhook)
            .filter(Webhook.event_type == event_type, Webhook.enabled == True)
            .all()
        )
        for h in hooks:
            send_webhook_task.delay(h.url, {"event": event_type, "data": data})
    finally:
        db.close()
