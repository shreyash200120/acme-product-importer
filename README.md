# Acme Product Importer

This project is a complete solution for the Acme CSV product import assignment.

It allows users to:

- Upload large CSV files containing product data
- Process the import asynchronously (no UI blocking)
- Track import progress live
- View & filter imported products
- Delete all products when needed
- Trigger webhook notifications once an import completes

The entire system runs using **Docker Compose**, so no local setup is required besides Docker.

---

## 🚀 Features

| Feature | Implemented |
|--------|:-----------:|
| CSV Upload | ✅ |
| Asynchronous Processing (Celery) | ✅ |
| Progress Polling UI | ✅ |
| PostgreSQL Storage | ✅ |
| SKU-Based Upsert | ✅ |
| Webhooks (Event Triggered on Completion) | ✅ |
| Product Listing + Search | ✅ |
| Bulk Delete Products | ✅ |

---

## 🏗️ System Architecture

The application uses the following stack:

- **FastAPI** → Serves API and frontend pages
- **PostgreSQL** → Stores product data
- **SQLAlchemy ORM** → Models, queries, migrations-ready
- **Redis + Celery** → Background task processing (CSV import + webhooks)
- **Docker Compose** → One command environment setup
- **Bootstrap + Vanilla JavaScript** → Frontend UI

Workflow overview:

User Uploads CSV → Saved → Celery Worker Processes → DB Upserts → Webhooks Fired → UI Shows Progress

---

### 📁 Project Structure

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
├── uploads/                    # Temp storage for uploaded CSVs
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Installation & Running

### 1️⃣ Prerequisites

- Docker Desktop or Docker Engine

No Python installation needed.

---

### 2️⃣ Setup Environment

Inside the project folder, run:

cp .env.example .env

### 3️⃣ Start Application
docker-compose up --build

Once running, visit:

👉 http://localhost:8000

## 📌 How to Use

1. Open your browser and go to:

   👉 http://localhost:8000

2. Click **"Upload CSV"** and select a CSV file.

3. The progress bar will show real-time import status.

4. Once complete, navigate to the **Products** page to view and filter imported items.

5. (Optional) Register a webhook on the **Webhooks** page to be notified when future imports finish.

6. You may delete all data anytime using the **Delete All** button on the Products page.
