# Proposal & Solution Design Intelligence Architecture

## 1. System Overview

The **Proposal & Solution Design Intelligence System** transforms confirmed solution designs into client-facing technical and commercial proposals. It itemizes project scope, structures proposal sections, validates claim evidence traceability, computes content hashes, and integrates with the Phase 20 Risk & Quality Engine before requiring human operator approval.

```text
APPROVED SOLUTION DESIGN (Phase 23)
          ↓
   PROPOSAL AGENT (v1.0)
          ↓
  ┌───────────────────────┬────────────────────────┬──────────────────────┐
  │   PROPOSAL DRAFT      │   CLAIM VALIDATOR      │  CONTENT HASH (v1)   │
  └───────────────────────┴────────────────────────┴──────────────────────┘
          ↓
   RISK & QUALITY ENGINE (Phase 20) → PENDING_APPROVAL
          ↓
   HUMAN OPERATOR APPROVAL → APPROVED
```

---

## 2. Core Components

1. **ORM Data Layer** (`app/models/proposal.py`):
   - `Proposal`: Main proposal record.
   - `ProposalItem`: Itemized deliverable scope items.
   - `ProposalVersion`: Immutable historical snapshot versions with content hashes.

2. **Proposal Agent** (`agents/proposal/`):
   - **`ProposalComposer`**: Section composer (Cover, Executive Summary, Needs, Solution, Scope, Deliverables, Assumptions, Terms).
   - **`ProposalClaimValidator`**: Claim traceability and prohibited claim detection.
   - **`ProposalAgent`**: Production AI agent registered in `global_registry`.

3. **REST API & Service Layer** (`app/services/proposal.py`, `app/api/v1/proposals.py`):
   - `POST /api/v1/proposals`: Create draft proposal workspace.
   - `GET /api/v1/proposals/{id}`: Inspect proposal workspace.
   - `POST /api/v1/proposals/{id}/generate`: Trigger ProposalAgent composition and Risk Engine check.
   - `POST /api/v1/proposals/{id}/approve`: Human operator approval.

4. **Frontend UI** (`frontend/components/proposals/`, `frontend/app/(dashboard)/proposals/`):
   - Interactive Proposal Command Center workspace, pricing status display, and version history.

---

## 3. Commercial Safety & Guardrails

- **Pricing Safety**: Defaults `pricing_status` to `PRICING_REQUIRES_HUMAN_REVIEW` or `NOT_DEFINED`. Agents never autonomously invent binding prices.
- **Zero External Direct Dispatch**: Zero external sending permissions (`SEND_EMAIL`, `SEND_MESSAGE`). Approved proposals must pass through Phase 19 Communication Guard.
- **Immutable Versioning**: Any post-approval edits invalidate approval status and increment version (`v1` → `v2`).
