# Phase 16 — Audit Agent Integration Guide

## 1. System Integration Flow

```text
[Frontend / React Component (AuditAgentCard)]
         │
         ▼ (POST /api/v1/audits/jobs/{job_id}/run-agent)
[REST API Router (app/api/v1/audits.py)]
         │
         ▼
[Background Worker Task (workers/tasks/audit.py)]
         │
         ▼
[AgentRuntimeService (Phase 14)]
         │
         ▼
[AuditAgent (agents/audit/agent.py)]
         │
         ├── Target Selection (AuditPlanner)
         ├── Deterministic Audit Engine (Phase 11 runner)
         ├── Finding Classifier & Severity (AuditFindingCollector)
         └── Output Validation (AuditOutputValidator)
```

---

## 2. API Endpoints

### 2.1 Trigger Audit Agent Run
`POST /api/v1/audits/jobs/{job_id}/run-agent`
- **Auth**: Required (`ADMIN` or `MEMBER` role)
- **Response**:
```json
{
  "status": "SUCCESS",
  "message": "Audit Agent executed successfully.",
  "data": {
    "id": "job-uuid",
    "status": "COMPLETED",
    "findings_count": 5
  }
}
```

---

## 3. Worker Integration

The worker task `execute_audit_task(db, job_id)` in `workers/tasks/audit.py`:
1. Fetches `AuditJob` by ID.
2. Triggers `AgentRun` tracking record in `AgentRunRepository`.
3. Instantiates `AuditAgent` via `global_registry.get("audit_agent")`.
4. Executes `agent.run(context)` within context boundaries.
5. Runs Phase 11 audit runner for persistence compatibility.
6. Updates `AgentRun` status (`COMPLETED`, `PARTIAL`, `NO_WEBSITE`, `FAILED`) and records execution events.
