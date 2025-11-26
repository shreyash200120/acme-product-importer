from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import redis
from app.services.csv_importer import process_csv_task

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.Redis.from_url(REDIS_URL)

router = APIRouter()


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    job_id = str(uuid.uuid4())
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{job_id}.csv")

    try:
        with open(file_path, "wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    r.set(f"progress:{job_id}", "0/0")

    # enqueue background task
    process_csv_task.delay(job_id, file_path)

    return {"job_id": job_id}


@router.get("/progress/{job_id}")
def get_progress(job_id: str):
    val = r.get(f"progress:{job_id}")
    if not val:
        return {"status": "NOT_FOUND"}

    text = val.decode("utf-8")
    # Could be "X/Y" or "COMPLETED:Z" or "ERROR:..."
    return {"status": text}
