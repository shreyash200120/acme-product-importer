from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app import models, schemas


# Upsert a single product using Postgres ON CONFLICT
def upsert_product(db: Session, data: Dict):
    stmt = insert(models.Product).values(**data)
    update_cols = {k: getattr(stmt.excluded, k) for k in data.keys() if k != "sku"}
    stmt = stmt.on_conflict_do_update(index_elements=["sku"], set_=update_cols)
    db.execute(stmt)


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    sku: Optional[str] = None,
    name: Optional[str] = None,
    active: Optional[bool] = None,
) -> List[models.Product]:
    q = db.query(models.Product)
    if sku:
        q = q.filter(models.Product.sku.ilike(f"%{sku.lower()}%"))
    if name:
        q = q.filter(models.Product.name.ilike(f"%{name}%"))
    if active is not None:
        q = q.filter(models.Product.active == active)
    return q.offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    data = product.dict()
    data["sku"] = data["sku"].lower().strip()
    obj = models.Product(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_product(db: Session, product_id: int, data: dict) -> Optional[models.Product]:
    obj = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not obj:
        return None
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_product(db: Session, product_id: int) -> bool:
    obj = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def delete_all_products(db: Session) -> None:
    db.query(models.Product).delete()
    db.commit()


# Webhooks CRUD
def list_webhooks(db: Session):
    return db.query(models.Webhook).all()


def create_webhook(db: Session, webhook: schemas.WebhookCreate) -> models.Webhook:
    obj = models.Webhook(**webhook.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_webhook(db: Session, webhook_id: int, data: dict):
    obj = db.query(models.Webhook).filter(models.Webhook.id == webhook_id).first()
    if not obj:
        return None
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_webhook(db: Session, webhook_id: int) -> bool:
    obj = db.query(models.Webhook).filter(models.Webhook.id == webhook_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
