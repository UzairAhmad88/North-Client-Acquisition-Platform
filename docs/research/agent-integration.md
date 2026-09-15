# Phase 15 — Research Agent Integration Guide

## 1. Integration Flow

The Research Agent is integrated across the backend API, worker tasks, and Next.js frontend workspace:

```text
[Frontend / React Component]
         │
         ▼ (POST /api/v1/research/jobs/{job_id}/run-agent)
[REST API Router (app/api/v1/research.py)]
         │
         ▼
[Background Worker Task (workers/tasks/research.py)]
         │
         ▼
[AgentRuntimeService (Phase 14)]
         │
         ▼
[ResearchAgent (agents/research/agent.py)]
         │
         ├── ReadBusinessTool / FetchWebTool (agents/research/tools.py)
         ├── ResearchEvidenceCollector & ConfidenceCalculator
         └── ResearchOutputValidator
```

---

## 2. API Endpoints

### 2.1 Trigger Agent Execution
`POST /api/v1/research/jobs/{job_id}/run-agent`
- **Auth**: Required (`ADMIN` or `MEMBER` role)
- **Response**:
```json
{
  "status": "SUCCESS",
  "message": "Research Agent executed successfully.",
  "data": {
    "id": "job-uuid",
    "status": "COMPLETED",
    "records_found": 4,
    "records_validated": 4
  }
}
```

---

## 3. Worker Integration

The worker task `execute_research_task(db, job_id)` in `workers/tasks/research.py`:
1. Fetches `ResearchJob` by ID.
2. Triggers `AgentRun` tracking record in `AgentRunRepository`.
3. Instantiates `ResearchAgent` via `global_registry.get("research_agent")`.
4. Executes `agent.run(context)` within context boundaries.
5. Updates `AgentRun` status (`COMPLETED`, `PARTIAL`, `FAILED`) and records execution events.
