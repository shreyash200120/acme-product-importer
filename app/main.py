from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError
import time

from app.database import Base, engine
from app.routers import upload, products, webhooks


app = FastAPI(title="Acme Product Importer")


# ✅ Wait for DB and then create tables
@app.on_event("startup")
def startup_event():
    retries = 10  # try for ~20 seconds total
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ DB ready, tables created")
            break
        except OperationalError as e:
            print("⏳ DB not ready yet, retrying...", e)
            retries -= 1
            time.sleep(2)


# API routers
app.include_router(upload.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")

# Serve static HTML UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}
