from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.services.webhook_sender import send_webhook_task
from app.models import Webhook

router = APIRouter()


@router.get("/webhooks", response_model=List[schemas.WebhookOut])
def list_webhooks(db: Session = Depends(get_db)):
    return crud.list_webhooks(db)


@router.post("/webhooks", response_model=schemas.WebhookOut)
def create_webhook(webhook: schemas.WebhookCreate, db: Session = Depends(get_db)):
    return crud.create_webhook(db, webhook)


@router.put("/webhooks/{webhook_id}", response_model=schemas.WebhookOut)
def update_webhook(webhook_id: int, webhook: schemas.WebhookCreate, db: Session = Depends(get_db)):
    updated = crud.update_webhook(db, webhook_id, webhook.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return updated


@router.delete("/webhooks/{webhook_id}")
def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_webhook(db, webhook_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return {"ok": True}


@router.post("/webhooks/test/{webhook_id}")
def test_webhook(webhook_id: int, db: Session = Depends(get_db)):
    hook: Webhook | None = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not hook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    send_webhook_task.delay(hook.url, {"event": "test", "data": {"ok": True}})
    return {"ok": True}
