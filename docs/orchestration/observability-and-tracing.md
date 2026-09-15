# Orchestration Observability, Correlation & Tracing

## 1. Overview

The orchestration platform implements end-to-end distributed observability across all events, workflows, tasks, and worker executions. Every interaction carries a strict correlation envelope ensuring total traceability from root business trigger to final outcome.

```text
[ USER ACTION / TRIGGER ]
           │ correlation_id: trace-abc-123, causation_id: null
           ▼
     [ DOMAIN EVENT ]
           │ correlation_id: trace-abc-123, causation_id: event-001
           ▼
 [ WORKFLOW STATE MACHINE ]
           │ correlation_id: trace-abc-123, causation_id: step-001
           ▼
    [ TASK DISPATCHER ]
           │ correlation_id: trace-abc-123, causation_id: task-001
           ▼
[ AGENT / WORKER EXECUTION ]
```

---

## 2. Distributed Tracing Envelope

Every `DomainEvent`, `WorkflowInstance`, `WorkflowStepInstance`, and `TaskExecution` stores the following metadata attributes:

* **`correlation_id`**: The root identifier spanning the entire business journey (e.g., initial lead intake, full proposal lifecycle, client handover). It is preserved immutably across all child events, steps, and background tasks.
* **`causation_id`**: The immediate parent identifier (event ID, step ID, or task ID) that directly triggered the current operation.
* **`trace_id` / `span_id`**: OpenTelemetry-compatible tracing identifiers for linking with APM platforms.
* **`tenant_id`**: Partitioning identifier for multi-tenant isolation.
* **`actor_type` & `actor_id`**: Identifies whether the operation was initiated by a human (`HUMAN`), an automated agent (`AI_AGENT`), or a system timer (`SYSTEM`).

---

## 3. Telemetry & Metrics

The orchestration engine tracks key operational metrics:

1. **Workflow Health**:
   - `workflow_execution_duration_seconds`: Histogram of total workflow turnaround time.
   - `workflow_step_duration_seconds`: Duration per step and subsystem.
   - `workflow_state_transitions_total`: Counter for state transitions by type and status.
   - `workflow_compensation_events_total`: Rate of saga compensations triggered.

2. **Event Bus Performance**:
   - `event_outbox_lag_seconds`: Delay between event insertion into `event_outbox` and actual dispatch.
   - `event_inbox_deduplication_ratio`: Percentage of duplicate incoming events filtered.
   - `event_bus_publish_throughput`: Rate of published events per subsystem.

3. **Human Task SLA & Governance**:
   - `human_task_queue_depth`: Number of pending approvals and reviews.
   - `human_task_wait_time_hours`: Time spent in `WAITING_FOR_HUMAN_APPROVAL` before operator action.
   - `human_task_approval_rate`: Ratio of approved vs. rejected tasks.

4. **Reliability & Dead Letters**:
   - `dead_letter_queue_depth`: Total active un-triaged DLQ items.
   - `retry_attempt_distribution`: Distribution of retry attempts (1st, 2nd, 3rd, max).

---

## 4. Audit Log Integrity

All state transitions, rule evaluations, task completions, and human decisions produce immutable entries in `workflow_audit_logs`. Audit logs cannot be updated or deleted, providing complete compliance assurance for enterprise clients.
