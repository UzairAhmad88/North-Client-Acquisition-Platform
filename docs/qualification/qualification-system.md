# Qualification System Architecture & Data Model

## Overview
The Qualification System provides data persistence, REST APIs, background task execution, and human control mechanisms for lead qualification decisions in North's platform.

---

## Database Model (`lead_qualifications`)

The `lead_qualifications` table stores structured qualification records and historical human overrides:

```sql
CREATE TABLE lead_qualifications (
    id UUID PRIMARY KEY,
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    agent_run_id UUID REFERENCES agent_runs(id),
    decision VARCHAR(32) NOT NULL,
    confidence VARCHAR(16) NOT NULL,
    summary TEXT,
    factors JSONB NOT NULL DEFAULT '[]',
    reasons JSONB NOT NULL DEFAULT '[]',
    evidence JSONB NOT NULL DEFAULT '[]',
    risks JSONB NOT NULL DEFAULT '[]',
    missing_information JSONB NOT NULL DEFAULT '[]',
    limitations JSONB NOT NULL DEFAULT '[]',
    outreach_readiness VARCHAR(32) NOT NULL,
    recommended_internal_action VARCHAR(64),
    qualification_version VARCHAR(16) NOT NULL DEFAULT '1.0',
    is_stale BOOLEAN NOT NULL DEFAULT FALSE,
    human_override_decision VARCHAR(32),
    human_override_reason TEXT,
    overridden_by_user_id UUID REFERENCES users(id),
    overridden_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

---

## Key Features

1. **Deterministic Guardrails**:
   - **Do Not Contact (DNC) Check**: Overrides decision to `OUTREACH_BLOCKED`.
   - **Duplicate Context**: Unresolved duplicates mark status as `NEEDS_REVIEW`.
   - **Insufficient Data**: Missing basic business/research records marks status as `INSUFFICIENT_DATA`.

2. **Human Override Mechanism**:
   - Authorized operators can override any automated qualification decision.
   - Requires explicit text justification (`human_override_reason`).
   - Preserves original agent decision in historical audit fields (`decision`, `factors`, `reasons`) while setting `human_override_decision`, `overridden_by_user_id`, and `overridden_at`.

3. **REST API Endpoints**:
   - `POST /api/v1/leads/{id}/qualification`: Execute qualification task.
   - `GET /api/v1/leads/{id}/qualification`: Fetch current qualification record.
   - `POST /api/v1/leads/{id}/qualification/override`: Apply human override.
