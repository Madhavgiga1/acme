# Acme Inc. Product Importer System

A scalable, production-ready backend application built to handle the asynchronous import of large product catalogs (up to 500,000 records) from CSV files. The solution is fully containerized using Docker and utilizes a multi-service architecture for stability and performance.

## 🏗️ Architecture Overview

This is a **multi-container Dockerized setup** with individual services for:
- **Django** (Web Application)
- **Celery** (Background Task Processing)
- **PostgreSQL** (Database)
- **Redis** (Message Broker)

This architecture allows for cleaner scaling, easier development, and superior fault isolation.
![over](https://github.com/user-attachments/assets/f332061c-6650-400f-8e25-5b9063adb5bb)
![overview](https://github.com/user-attachments/assets/f71b64a1-cf44-4f36-8b22-15143aa89e59)

```
┌─────────────┐      ┌─────────────┐
│   Django    │◄────►│    Redis    │
│  Web App    │      │   (Broker)  │
└──────┬──────┘      └─────────────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐
│ PostgreSQL  │◄────►│   Celery    │
│  Database   │      │   Worker    │
└─────────────┘      └─────────────┘
```

## 🎯 Key Technical Achievements

### ✅ Clean Codebase Structure
Organized the project into three focused apps: **core**, **app**, and **products**. This makes the code easier to navigate, extend, and maintain.

### ✅ Dockerized Architecture
Multi-container environment with separate services for Django, Celery, PostgreSQL, and Redis, ensuring cleaner scaling and superior fault isolation.

### ✅ Stable Service Startup
Implemented a custom `wait_for_db` management command and used Docker's `service_healthy` conditions so the App and Celery containers only start after Postgres is ready, preventing random startup failures during deployments.

### ✅ Scalable Background Processing
Used **Celery** with **Redis** as the message broker to process large CSV imports (500,000+ rows) without blocking the web server. Optimized DB operations using:
- Chunked file reading
- Bulk upserts/updates
- Transaction management

### ✅ Secure Deployment Setup
- Deployed with **Gunicorn** and **Whitenoise** for production stability
- Used server-side `.env` files for sensitive configuration
- `SECRET_KEY` and database credentials are segregated from the codebase
- Environment-based configuration for seamless local-to-production transitions

### ✅ Data Integrity & User Experience
- Case-insensitive SKU overwrites (upsert logic)
- Real-time progress bar updates via polling
- Comprehensive Product Management CRUD operations
- Advanced filtering capabilities

## 🚀 Features Implementation

| Feature | Status | Description |
|---------|--------|-------------|
| **Async CSV Import** | ✅ | Upload large CSV files with real-time progress tracking via polling. Handles case-insensitive SKU upserts. |
| **Product Management** | ✅ | Full CRUD operations with pagination and filtering by SKU, name, and active status. |
| **Bulk Operations** | ✅ | Delete All Products functionality executed asynchronously via Celery. |
| **Webhook Integration** | ✅ | Webhook endpoints triggered upon successful import completion. |



### Upload via Web Interface

1. Navigate to `http://localhost:80/products/import/`
2. Select your CSV file
3. Click "Import Products"
4. Watch the real-time progress bar
5. View imported products at `http://localhost:80/products/`

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/` | GET | List all products with pagination |
| `/products/create/` | POST | Create a new product |
| `/products/<id>/edit/` | POST | Update existing product |
| `/products/<id>/delete/` | POST | Delete a product |
| `/products/import/` | POST | Upload CSV for async import |
| `/products/import/progress/<task_id>/` | GET | Get import progress |
| `/products/delete-all/` | POST | Bulk delete all products |



## 📚 Technology Stack

- **Backend Framework:** Django 4.2+
- **Task Queue:** Celery 5.3+
- **Message Broker:** Redis 7+
- **Database:** PostgreSQL 15+
- **WSGI Server:** Gunicorn
- **Static Files:** Whitenoise
- **Containerization:** Docker & Docker Compose



