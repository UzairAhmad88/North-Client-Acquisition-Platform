# Human Task System & Approval Wait States

## First-Class Human Review Queues

When a workflow transitions into a `HUMAN_TASK` node (e.g. `APPROVE_OUTREACH`, `APPROVE_CONTRACT`, `APPROVE_RELEASE`), execution enters `WAITING` status and releases worker execution threads.

```text
AI Synthesis (Draft)
       │
       ▼
Risk Engine Verification
       │
       ▼
WAITING_FOR_HUMAN_APPROVAL ───▶ Human Task Queue (UI)
       │                              │
       │       ┌──────────────────────┴──────────────────────┐
       │       ▼                                             ▼
       │   APPROVE                                         REJECT
       │  (Captures Content Hash & Operator ID)    (Captures Reason & Cancels Workflow)
       │       │
       ▼       ▼
Workflow Resumes Execution
       │
       ▼
Guarded External Dispatch
```

## Content Hash Integrity Binding

When a human approves a draft payload, a SHA-256 hash of the approved text is bound to the `WorkflowApproval` record. If subsequent edits mutate the text prior to sending, the approval is instantly invalidated by `CommunicationGuard`.
