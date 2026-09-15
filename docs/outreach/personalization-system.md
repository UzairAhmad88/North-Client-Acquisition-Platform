# Personalization System Architecture & Data Model

## Overview
The Personalization System handles evidence-backed personalization profile generation, channel-specific communication draft creation, draft versioning, claim validation, and human review boundaries.

---

## Database Model (`outreach_drafts`)

```sql
CREATE TABLE outreach_drafts (
    id UUID PRIMARY KEY,
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    agent_run_id UUID REFERENCES agent_runs(id),
    channel VARCHAR(32) NOT NULL DEFAULT 'EMAIL',
    tone VARCHAR(32) NOT NULL DEFAULT 'PROFESSIONAL',
    language VARCHAR(8) NOT NULL DEFAULT 'en',
    personalization_depth VARCHAR(32) NOT NULL DEFAULT 'STANDARD',
    objective VARCHAR(64) NOT NULL DEFAULT 'INTRODUCE_SERVICE',
    subject VARCHAR(255),
    body TEXT NOT NULL,
    primary_angle JSONB NOT NULL DEFAULT '{}',
    personalization_profile JSONB NOT NULL DEFAULT '{}',
    claims JSONB NOT NULL DEFAULT '[]',
    evidence JSONB NOT NULL DEFAULT '[]',
    risk_level VARCHAR(32) NOT NULL DEFAULT 'LOW',
    outreach_readiness VARCHAR(32) NOT NULL DEFAULT 'READY',
    approval_status VARCHAR(32) NOT NULL DEFAULT 'PENDING_APPROVAL',
    rejection_reason TEXT,
    version INTEGER NOT NULL DEFAULT 1,
    content_hash VARCHAR(64),
    is_stale BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
```

---

## Draft Versioning & Approval Invalidation Architecture

1. **Initial Draft**: When the Personalization Agent generates a draft, it starts at `version = 1` with `approval_status = PENDING_APPROVAL`.
2. **Human Modification**: If a user edits the subject or body of a draft, the system automatically:
   - Increments `version` ($v \rightarrow v+1$).
   - Resets `approval_status` to `PENDING_APPROVAL`.
3. **Approval Boundary**: The Personalization Agent cannot approve its own drafts or change status to `APPROVED`. Approval belongs strictly to human operator workflows.
