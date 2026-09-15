# Phase 34 — Unified Workflow Orchestration, Event Bus & Automation Control Plane

## Executive Summary

Phase 34 delivers the central orchestration, transactional event bus, and automation control plane for the **Uzaii Develop By North's** platform.

It bridges all 33 previous phases into an event-driven, durable, observable, versioned, idempotent, failure-tolerant, human-controlled, and tenant-isolated operational system.

## Fundamental Architectural Principle

> **Automate coordination, not authority.**
> Events describe what happened $\neq$ Commands request what should happen $\neq$ Workflows determine what happens next $\neq$ Agents provide intelligence $\neq$ Humans approve sensitive decisions $\neq$ Guards enforce safety.

```text
Event ≠ Command ≠ Decision ≠ Approval ≠ Execution
```

## Document Index

1. [Architecture Overview](architecture.md) — System topology, event flows, and control plane layers.
2. [Event Bus & Registry](event-bus.md) — Event specifications, versioning, schemas, and provider adapter.
3. [Transactional Outbox & Inbox](outbox-inbox.md) — Atomic persistence, consumer deduplication, and idempotency keys.
4. [Workflow Engine](workflow-engine.md) — Declarative graph templates, state machine, and durable execution.
5. [Saga Orchestration & Consistency](sagas-and-compensation.md) — Multi-step distributed transactions and failure containment.
6. [Human Task System](human-tasks.md) — Review queues, approval wait states, content hashing, and audit trails.
7. [Automation Rules Engine](automation-rules.md) — WHEN/IF/THEN rule builder, triggers, and safety guardrails.
8. [Task Dispatcher & Priority Queues](task-dispatcher.md) — Routing, concurrency limits, and distributed locks.
9. [Retries & Dead Letter Queue (DLQ)](dlq-and-retries.md) — Exponential backoff, jitter, and poisoned message triage.
10. [Controlled Event Replay](event-replay.md) — Replay modes, dry-run verification, and side-effect blocking.
11. [Observability & Tracing](observability-and-tracing.md) — Correlation IDs, causation trees, and execution metrics.
