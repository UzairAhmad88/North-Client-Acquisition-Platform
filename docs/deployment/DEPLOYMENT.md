# Deployment & Local Infrastructure Guide

## Architectural Overview
```text
Next.js (Port 3000)
   |
FastAPI (Port 8000)
   |
PostgreSQL (Port 5432) & Redis (Port 6379)
```

## Local Development Setup

### Environment Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Ensure `REAL_SEND=false` is set for local development safety.

### Running with Docker Compose
```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker compose up -d

# Check service status
docker compose ps

# View service logs
docker compose logs -f
```

### Manual Service Checks
- **Backend API Base**: `http://localhost:8000/api/v1`
- **Health Check**: `http://localhost:8000/health`
- **Liveness Check**: `http://localhost:8000/health/live`
- **Readiness Check**: `http://localhost:8000/health/ready`
- **Frontend App**: `http://localhost:3000`

### Running Backend Locally
```bash
cd backend
python -m venv .venv
# Activate venv (.venv\Scripts\activate on Windows or source .venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Running Backend Tests & Linter
```bash
cd backend
python -m pytest
python -m ruff check .
```

### Safety & Risk Control Boundary
In development, outbound email or message sending is disabled (`REAL_SEND=false`). Mock providers are used for all external integrations.
