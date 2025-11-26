# 📦 Acme Product Importer

A complete end-to-end solution for the **Acme CSV product import assignment**. 

---

## 🎯 What This App Does

✔ Upload large CSV files  
✔ Process import in background using Celery  
✔ Track real-time progress  
✔ Store products in PostgreSQL  
✔ Upsert by SKU (update if exists, insert if new)  
✔ View & filter products from UI  
✔ Delete all data with one click  
✔ Trigger webhook notification after import completes  

All components run together using **Docker Compose** — no manual Python setup required.

---

## 🚀 Features

| Feature | Status |
|--------|--------|
| CSV Upload | ✅ |
| Background Processing (Celery) | ✅ |
| Progress Polling | ✅ |
| PostgreSQL Storage | ✅ |
| SKU-Based Upsert | ✅ |
| Webhook Triggers | ✅ |
| UI Filtering/Search | ✅ |
| Bulk Delete Products | ✅ |

---

## 🏗️ System Architecture

| Component | Purpose |
|----------|---------|
| **FastAPI** | REST API + UI rendering |
| **PostgreSQL** | Product storage |
| **SQLAlchemy** | ORM & DB access |
| **Redis** | Celery broker |
| **Celery Worker** | Async CSV import + webhook |
| **Docker Compose** | Full environment automation |
| **Bootstrap + JS** | Frontend UI |

**Flow:**

> Upload CSV → Stored → Celery Processes → Upsert Products → Send Webhook → UI Shows Progress

---

## 📁 Project Structure

```txt
acme-product-importer/
│
├── app/
│   ├── main.py                 # FastAPI app entrypoint
│   ├── models.py               # SQLAlchemy models
│   ├── database.py             # DB connection/session
│   ├── crud.py                 # DB helpers
│   ├── celery_app.py           # Celery config
│   ├── schemas.py              # Pydantic schemas
│   ├── routers/
│   │   ├── upload.py           # CSV upload + progress API
│   │   ├── products.py         # Product list/filter/delete API
│   │   └── webhooks.py         # Webhook management API
│   └── services/
│       ├── csv_importer.py     # CSV parsing + SKU upsert logic
│       └── webhook_sender.py   # Sends webhook POST requests
│
├── static/
│   ├── index.html              # Upload UI + progress
│   ├── products.html           # Product table + SKU filter
│   └── webhooks.html           # Webhook registration UI
│
├── uploads/                    # Temp CSV storage
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation & Run

### 1️⃣ Prerequisites

- Docker Desktop (Windows/Mac)  
- OR Docker Engine (Linux)  

> No Python installation required.

---

### 2️⃣ Create Environment File

```sh
cp .env.example .env
```

---

### 3️⃣ Start the System

```sh
docker-compose up --build
```

After startup, open:

➡ http://localhost:8000

---

## 📌 How to Use

1. Go to **Upload Page**
2. Select a CSV and upload
3. Watch progress bar update live
4. Visit **Products Page** to view and filter data
5. (Optional) Add webhook URL for notifications
6. Use **Delete All** anytime to reset database

---

### 🏁 Done!

---

