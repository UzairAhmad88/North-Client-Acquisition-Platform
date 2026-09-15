# Phase 16 — Audit Agent Testing Suite

## 1. Test Coverage Overview

Unit and integration tests for the Audit Agent are located at `tests/unit/backend/test_audit_agent.py`.

### 1.1 Test Suite Matrix

| Test Case | Description | Status |
|---|---|---|
| `test_audit_agent_registration` | Verifies agent auto-registration in `global_registry` with permissions. | PASS |
| `test_audit_planner_target_selection` | Validates target URL selection hierarchy (Official > Researched > None). | PASS |
| `test_audit_planner_freshness_reuse` | Validates freshness policy enforcement ($\le 7$ day reuse). | PASS |
| `test_finding_collector_severity` | Verifies severity assignment (`HIGH`, `MEDIUM`, `LOW`, `INFO`). | PASS |
| `test_ssrf_security_guard` | Verifies `SecurityValidationError` on private/loopback/metadata URLs. | PASS |
| `test_prompt_injection_defense` | Validates `<UNTRUSTED_EXTERNAL_DATA>` tag wrapping for fetched web content. | PASS |
| `test_prohibited_communication_permission_failure` | Confirms system raises `AgentPermissionDeniedError` if `SEND_EMAIL` is requested. | PASS |
| `test_audit_agent_execution` | Tests full asynchronous execution workflow of `AuditAgent.run(ctx)`. | PASS |
| `test_audit_agent_api` | Tests REST endpoint `POST /api/v1/audits/jobs/{job_id}/run-agent` with auth headers. | PASS |

---

## 2. Command Execution
To run the test suite:
```bash
PYTHONPATH=backend python -m pytest tests/unit/backend/test_audit_agent.py
```
To run full backend unit tests:
```bash
PYTHONPATH=backend python -m pytest tests/unit/backend/
```
