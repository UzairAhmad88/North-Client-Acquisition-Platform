# Environment & Repository Setup Guide

## System Requirements
- Python 3.11+
- Node.js 20+ / npm
- Docker & Docker Compose
- PostgreSQL 16+ (or via Docker Compose)
- Redis 7+ (or via Docker Compose)

## Quick Start with Docker Compose
1. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```
2. Launch database and application containers:
   ```bash
   docker compose up -d
   ```
3. Check container status:
   ```bash
   docker compose ps
   ```

## Services & Ports
- Backend API: `http://localhost:8000` (Health checks: `/health`, `/health/live`, `/health/ready`)
- Frontend UI: `http://localhost:3000`
- PostgreSQL: `localhost:5432` (db: `uzaii`, user: `postgres`)
- Redis: `localhost:6379`

## Local Backend Development
```bash
cd backend
python -m venv .venv
# Activate venv (.venv\Scripts\activate on Windows)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Running Tests & Quality Checks
```bash
# Run pytest from backend directory
cd backend && python -m pytest

# Run linter
cd backend && ruff check .
```
