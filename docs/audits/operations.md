# Audit Operations & Troubleshooting Guide

## REST API Reference

```http
POST   /api/v1/audits/jobs
GET    /api/v1/audits/jobs
GET    /api/v1/audits/jobs/{id}
POST   /api/v1/audits/jobs/{id}/run?runner_type=MOCK|REAL
POST   /api/v1/audits/jobs/{id}/cancel

GET    /api/v1/audits/businesses/{business_id}
GET    /api/v1/audits/businesses/{business_id}/findings
GET    /api/v1/audits/businesses/{business_id}/history
GET    /api/v1/audits/{id}
```

## Operations & Background Workers

- Background task worker: `workers/tasks/audit.py` -> `execute_audit_task(db, job_id, runner_type)`.
- Errors are captured gracefully with job status `FAILED` and recorded error messages.
