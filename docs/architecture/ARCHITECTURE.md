# Architecture Baseline

## Layer Overview
```text
Presentation (Next.js)
   |
API Layer (FastAPI /api/v1)
   |
Business Services Layer (app.services)
   |
Repositories & Data Access (app.repositories & app.core.database)
```

## Backend Core Scaffolding

### Application Structure
```text
backend/app/
├── main.py                FastAPI application entry, middleware, exception handlers, lifecycle
├── api/
│   ├── deps.py            FastAPI dependencies (db session generator, request ID extractor)
│   └── v1/                API v1 router definitions
├── core/
│   ├── config.py          Pydantic Settings & environment validation
│   ├── database.py        SQLAlchemy engine, session factory, and Base model
│   ├── exceptions.py      Structured AppError hierarchy
│   ├── logging.py         Logging configuration
│   └── middleware.py      Request ID & Request Logging middlewares
├── models/                SQLAlchemy ORM domain models
├── schemas/
│   └── common.py          Generic DataResponse, PaginatedResponse, ErrorResponse schemas
├── repositories/          Database data access objects
├── services/              Domain business logic services
└── utils/                 Shared utility helpers
```

### API Contract Standard
- **Base Route**: `/api/v1`
- **Single Item**: `{"data": {...}}`
- **Collection**: `{"data": [...], "pagination": {"page": 1, "page_size": 25, "total": 100}}`
- **Error Response**: `{"error": {"code": "...", "message": "...", "request_id": "..."}}`
- **Response Headers**: `X-Request-ID` attached to all HTTP responses.

### Database & Migrations
- **ORM**: SQLAlchemy 2.0 with DeclarativeBase
- **Migrations**: Alembic (`alembic.ini` and `migrations/env.py`) configured to `settings.database_url`
