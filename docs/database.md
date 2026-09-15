# Database Foundation Guide

## Architecture Overview
- **Database Engine**: PostgreSQL 16 (via Docker Compose or local server)
- **ORM**: SQLAlchemy 2.0 with DeclarativeBase
- **Migrations**: Alembic
- **Primary Keys**: UUIDv4 (`uuid.uuid4`)
- **Timestamps**: Timezone-aware UTC (`created_at`, `updated_at`)

## Database Configuration & Environment
Configure database connectivity using environment variables (`.env`):
```ini
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/uzaii
POSTGRES_DB=uzaii
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Model Conventions (`app.models.base`)

### Naming Conventions
All tables enforce deterministic SQL constraint names:
- **Primary Keys**: `pk_<table>`
- **Foreign Keys**: `fk_<table>_<column>_<referred_table>`
- **Unique Constraints**: `uq_<table>_<column>`
- **Check Constraints**: `ck_<table>_<constraint>`
- **Indexes**: `ix_<table>_<column>`

### Shared Base Model (`BaseModel`)
All entities inherit from `BaseModel`:
```python
from app.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class ExampleEntity(BaseModel):
    __tablename__ = "example_entities"
    name: Mapped[str]
```
`BaseModel` automatically provides `id` (UUID PK), `created_at` (UTC timestamp), and `updated_at` (UTC timestamp auto-updated).

## Alembic Migration Workflow

### Common Commands
```bash
# Apply all pending migrations to latest schema
alembic upgrade head

# Roll back 1 migration
alembic downgrade -1

# Show current migration revision
alembic current

# Show migration history log
alembic history

# Autogenerate migration script after model changes
alembic revision --autogenerate -m "Add example table"
```

## Development Seed Framework
Populate initial test data safely in non-production environments:
```bash
python scripts/seed.py
```
> **Security Safeguard**: The seed framework aborts execution if `APP_ENV=production`.

## Reset Strategy (Development Only)
```bash
# Stop and remove postgres container volume
docker compose down -v

# Re-launch database container
docker compose up -d postgres

# Apply migrations and seed development data
alembic upgrade head
python scripts/seed.py
```

## Database Health & Security
- **Health Check**: Lightweight `SELECT 1` query executed at `/health/ready`.
- **Injection Protection**: All queries use SQLAlchemy parameterization. Raw string formatting is strictly prohibited.
- **Credential Protection**: Connection credentials are read strictly from environment variables.
