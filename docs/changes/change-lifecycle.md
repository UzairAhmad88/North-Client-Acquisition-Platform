# Change Request Lifecycle & State Machine

This document details the state machine transitions and governance rules for Change Requests in **Uzaii Develop By North's Phase 28**.

---

## 1. Lifecycle State Diagram

```text
REQUESTED
   ↓
TRIAGED
   ↓
IMPACT_ANALYSIS
   ↓
ESTIMATION
   ↓
INTERNAL_REVIEW
   ↓
PENDING_CLIENT
   ↓
CLIENT_APPROVED
   ↓
APPROVED
   ↓
BASELINE_UPDATE
   ↓
IMPLEMENTATION
   ↓
COMPLETED
```

Alternative States: `REJECTED`, `CANCELLED`, `WITHDRAWN`, `EXPIRED`, `ON_HOLD`, `SUPERSEDED`.

---

## 2. State Transition Rules

- **`REQUESTED` $\rightarrow$ `TRIAGED`**:
  - `ChangeClassifier` evaluates incoming request text.
  - Determines classification (`IN_SCOPE`, `OUT_OF_SCOPE`, `DEFECT`, `CLARIFICATION`).
- **`TRIAGED` $\rightarrow$ `IMPACT_ANALYSIS`**:
  - Multi-dimensional impact analyzer identifies affected requirements, features, deliverables, tasks, schedule, and risks.
- **`IMPACT_ANALYSIS` $\rightarrow$ `ESTIMATION`**:
  - PERT three-point re-estimation calculates expected hours $(O + 4M + P)/6$.
- **`INTERNAL_REVIEW` $\rightarrow$ `PENDING_CLIENT`**:
  - Internal engineering and commercial operator grants internal sign-off.
- **`PENDING_CLIENT` $\rightarrow$ `CLIENT_APPROVED`**:
  - Authorized client signer submits explicit approval statement referencing canonical SHA-256 payload hash.
- **`APPROVED` $\rightarrow$ `BASELINE_UPDATE`**:
  - Server locks Baseline v2 and updates contract baseline lineage.
- **`BASELINE_UPDATE` $\rightarrow$ `IMPLEMENTATION`**:
  - Execution tasks mapped to the change request are created in `project_tasks`.
