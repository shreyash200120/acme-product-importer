import csv
import os
import redis

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.celery_app import celery
from app.database import SessionLocal
from app.models import Product
from app.services.webhook_sender import send_event_webhook

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.Redis.from_url(REDIS_URL)

CHUNK_SIZE = 5000


@celery.task(bind=True)
def process_csv_task(self, job_id: str, file_path: str):
    """
    Celery task: read CSV in chunks, upsert products by SKU, update progress in Redis.
    Redis key: progress:{job_id} = "<processed>/<total>" or "ERROR:..."
    """
    db: Session = SessionLocal()
    try:
        # First pass: count rows (for progress)
        total_rows = 0
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            # skip header row
            header = next(reader, None)
            for _ in reader:
                total_rows += 1

        if total_rows == 0:
            r.set(f"progress:{job_id}", "COMPLETED:0")
            return {"status": "empty"}

        processed = 0
        r.set(f"progress:{job_id}", f"0/{total_rows}")

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            batch = []

            for row in reader:
                raw_sku = (row.get("sku") or row.get("SKU") or "").strip()
                if not raw_sku:
                    continue
                sku = raw_sku.lower()

                product_data = {
                    "sku": sku,
                    "name": row.get("name") or row.get("Name") or None,
                    "description": row.get("description") or None,
                    "price": float(row["price"]) if row.get("price") else None,
                    "active": True,
                }
                batch.append(product_data)

                if len(batch) >= CHUNK_SIZE:
                    _flush_batch(db, batch)
                    processed += len(batch)
                    batch = []
                    r.set(f"progress:{job_id}", f"{processed}/{total_rows}")

            if batch:
                _flush_batch(db, batch)
                processed += len(batch)
                r.set(f"progress:{job_id}", f"{processed}/{total_rows}")

        r.set(f"progress:{job_id}", f"COMPLETED:{processed}")

        # Fire webhooks
        send_event_webhook.delay("import.completed", {"job_id": job_id, "rows": processed})

        return {"status": "ok", "processed": processed}

    except Exception as e:
        r.set(f"progress:{job_id}", f"ERROR:{str(e)}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
        try:
            os.remove(file_path)
        except OSError:
            pass


def _flush_batch(db: Session, batch: list[dict]):
    """Upsert a batch of rows, safely handling duplicate SKUs inside the batch."""
    if not batch:
        return

    # ✅ Deduplicate by SKU inside this batch
    # If the same SKU appears multiple times in this batch,
    # the LAST row wins (overwrite previous for that SKU).
    by_sku: dict[str, dict] = {}
    for item in batch:
        sku = item["sku"]
        by_sku[sku] = item

    values = list(by_sku.values())
    if not values:
        return

    stmt = insert(Product).values(values)

    # Update all columns except 'sku' on conflict
    update_dict = {k: getattr(stmt.excluded, k) for k in values[0].keys() if k != "sku"}

    stmt = stmt.on_conflict_do_update(
        index_elements=["sku"],  # conflict target: unique sku
        set_=update_dict,
    )

    db.execute(stmt)
    db.commit()

