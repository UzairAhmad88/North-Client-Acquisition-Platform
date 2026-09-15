# Phase 15 — Research Agent Testing Suite

## 1. Test Coverage Overview

Unit and integration tests for the Research Agent are located at `tests/unit/backend/test_research_agent.py`.

### 1.1 Test Suite Matrix

| Test Case | Description | Status |
|---|---|---|
| `test_research_agent_registration` | Verifies agent auto-registration in `global_registry` with permitted and denied permissions. | PASS |
| `test_research_planner_data_reuse` | Validates freshness policy enforcement ($\le 30$ day reuse). | PASS |
| `test_evidence_collector_trust_hierarchy` | Verifies source trust hierarchy (`OFFICIAL` > `HIGH_TRUST` > `MEDIUM_TRUST` > `LOW_TRUST`). | PASS |
| `test_confidence_calculator` | Verifies confidence assignment (`HIGH`, `MEDIUM`, `LOW`). | PASS |
| `test_prompt_injection_defense` | Validates `<UNTRUSTED_EXTERNAL_DATA>` tag wrapping for fetched web content. | PASS |
| `test_ssrf_security_guard` | Verifies `SecurityValidationError` exception on private/loopback/metadata URLs. | PASS |
| `test_prohibited_communication_permission_failure` | Confirms system raises `AgentPermissionDeniedError` if `SEND_EMAIL` is requested. | PASS |
| `test_research_agent_execution` | Tests full asynchronous execution workflow of `ResearchAgent.run(ctx)`. | PASS |
| `test_research_agent_api` | Tests REST endpoint `POST /api/v1/research/jobs/{job_id}/run-agent` with auth headers. | PASS |

---

## 2. Command Execution
To run the test suite:
```bash
PYTHONPATH=backend python -m pytest tests/unit/backend/test_research_agent.py
```
To run full backend unit tests:
```bash
PYTHONPATH=backend python -m pytest tests/unit/backend/
```
