# API Contract
Base path: `/api/v1`.

Single response: `{"data": {...}}`
Collection response: `{"data": [], "pagination": {"page": 1, "page_size": 25, "total": 0}}`
Error: `{"error": {"code": "...", "message": "...", "request_id": "..."}}`

Async operations use task/workflow identifiers. Important errors include AUTH_REQUIRED, FORBIDDEN, VALIDATION_ERROR, RESOURCE_NOT_FOUND, APPROVAL_REQUIRED, OUTREACH_BLOCKED, DO_NOT_CONTACT, RATE_LIMITED and INTERNAL_ERROR.
