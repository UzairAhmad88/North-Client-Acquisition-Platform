# Service Recommendation Testing Strategy

## Test Coverage Summary

- **Engine Unit Tests**: `tests/unit/backend/test_recommendations.py`
  - Candidate generation across active service catalog.
  - 6-component weighted relevance formula calculations.
  - Relevance score band mapping (`STRONG`, `GOOD`, `POSSIBLE`, `WEAK`).
  - Priority matrix evaluation based on score and confidence.
  - REST API endpoint verification (`/calculate`, `/list`, `/get`, `/accept`, `/reject`, unauthenticated checks).

- **Service Unit Tests**: `tests/unit/services/test_recommendation_service.py`
  - Context building and data loading.
  - Recommendation staleness invalidation (`mark_lead_recommendations_stale`).
  - `NotFoundError` exceptions on invalid lead/recommendation UUIDs.
  - `LeadService` sync on recommendation acceptance with provenance `HUMAN_ACCEPTED_RECOMMENDATION`.

## Verification Commands

```bash
# Backend pytest suite
python -m pytest

# Backend mypy static type checking
python -m mypy app
```
