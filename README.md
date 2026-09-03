# 🚀 ML-via-API

> Production-oriented REST API for ML inference for Machine Learning model inference built with **FastAPI**, following **Clean Architecture**, featuring asynchronous processing, authentication, monitoring, centralized logging, automated testing, and CI/CD.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Redis](https://img.shields.io/badge/Redis-Enabled-red?logo=redis)
![Celery](https://img.shields.io/badge/Celery-Async-37814A?logo=celery)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?logo=grafana)
![Loki](https://img.shields.io/badge/Loki-Logging-F2C811?logo=grafana)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions)

---

# 📖 Overview

ML-via-API is a backend application designed to expose Machine Learning models through a REST API while following production-oriented development practices.

Instead of focusing only on serving predictions, the project demonstrates the technologies commonly used in modern backend systems:

- REST API development
- Authentication with JWT
- PostgreSQL persistence
- Asynchronous task processing
- Monitoring and observability
- Centralized logging
- Dockerized deployment
- Automated testing
- Continuous Integration

The objective of this project is to showcase backend engineering skills rather than Machine Learning model development itself.

---

# ✨ Features

- RESTful API using FastAPI
- Clean Architecture
- JWT Authentication
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Migrations
- Redis Integration
- Celery Background Tasks
- Prometheus Metrics
- Grafana Dashboards
- Loki Centralized Logging
- Docker & Docker Compose
- Pytest Test Suite
- GitHub Actions CI Pipeline
- Environment Variables Configuration

---

# 🏗️ Architecture

The project follows the principles of Clean Architecture.

```
Client
   │
   ▼
FastAPI API
   │
   ▼
Application Layer
   │
   ▼
Domain Layer
   │
   ▼
Infrastructure
   ├── PostgreSQL
   ├── Redis
   ├── Celery
   └── ML Model
```

Each layer has a single responsibility, making the application easier to maintain, extend and test.

---

# 🛠 Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

## Database

- PostgreSQL

## Background Tasks

- Celery
- Redis

## Authentication

- JWT

## Observability

- Prometheus
- Grafana
- Loki

## DevOps

- Docker
- Docker Compose
- GitHub Actions

## Testing

- Pytest

---

# 📂 Project Structure

```
.
├── app/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── api/
│   └── core/
│
├── tests/
│
├── migrations/
│
├── docker/
│
├── prometheus/
│
├── grafana/
│
├── loki/
│
├── docker-compose.yml
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Getting Started

## Clone repository

```bash
git clone https://github.com/AndresPimentel-dev/ML-via-API.git

cd ML-via-API
```

---

## Environment variables

Create a `.env` file.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=ml_api

DATABASE_URL=postgresql://postgres:password@db:5432/ml_api

SECRET_KEY=your_secret_key

REDIS_URL=redis://redis:6379
```

---

## Run with Docker

```bash
docker compose up --build
```

---

## API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 📊 Monitoring

The application includes complete observability.

## Prometheus

Collects application metrics.

```
http://localhost:9090
```

---

## Grafana

Visualizes metrics and dashboards.

```
http://localhost:3000
```

---

## Loki

Centralized log aggregation.

---

# 🔐 Authentication

Protected endpoints use JWT authentication.

Workflow:

```
Login
      │
      ▼
Generate JWT
      │
      ▼
Authorization Header
      │
      ▼
Protected Endpoint
```

---

# ⚙ Background Processing

Long-running tasks are executed asynchronously using Celery workers connected to Redis.

```
Request
   │
   ▼
FastAPI
   │
   ▼
Redis Queue
   │
   ▼
Celery Worker
   │
   ▼
Result
```

---

# 🧪 Running Tests

```bash
pytest
```

or

```bash
pytest -v
```

---

# 🔄 Continuous Integration

GitHub Actions automatically executes:

- Code quality checks
- Unit tests
- Build validation

Every Pull Request is validated before merging.

---

# 📈 Why this project?

This project was developed to demonstrate practical backend engineering skills, including:

- Software Architecture
- REST API Design
- Authentication
- Database Design
- Background Processing
- Monitoring
- Logging
- Docker
- CI/CD
- Automated Testing

Rather than being a simple CRUD application, it aims to resemble the structure and tooling commonly found in production backend services.

---

# 📌 Future Improvements

- Request rate limiting
- API versioning
- Structured logging
- Health checks
- Kubernetes deployment
- Distributed tracing with OpenTelemetry
- Model version management
- Prediction caching
- Load testing

---

# 👨‍💻 Author

**Andrés Pimentel**

Backend Developer focused on Python and FastAPI.

GitHub:

https://github.com/AndresPimentel-dev

---

# ⭐ If you found this project interesting...

Give the repository a ⭐ to support the project.
