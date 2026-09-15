# Unified Workflow Orchestration & Event Control Plane Architecture

## System Overview

Phase 34 implements the central nervous system connecting all 33 previous phases of **Uzaii Develop By North's**.

```mermaid
graph TD
    Client[Domain Services / AI Agents / Webhooks] --> Outbox[Transactional Outbox Pattern]
    Outbox --> EventBus[Central Event Bus Provider Adapter]
    EventBus --> Inbox[Idempotent Consumer Inbox]
    Inbox --> WFEngine[Workflow Engine State Machine]
    WFEngine --> TaskDispatcher[Prioritized Task Dispatcher]
    TaskDispatcher --> AgentTask[AI Agent Runtime]
    TaskDispatcher --> HumanTask[Human Review & Approval Queue]
    TaskDispatcher --> SystemTask[Deterministic Safety Guards]
    HumanTask --> HumanDecision[Human Approval / Rejection / Revision]
    HumanDecision --> WFEngine
    SystemTask --> DB[(PostgreSQL Master Store)]
```

## Architectural Decoupling

The platform strictly isolates:
- **Events**: Immutable records of completed facts (`occurred_at`, `payload`, `correlation_id`).
- **Commands**: Requests for future actions that may fail or require authorization.
- **Workflows**: Declarative directed acyclic graphs (DAGs) coordinating business steps.
- **Agents**: Autonomous intelligence producing candidate drafts within bounded permissions.
- **Human Approvals**: Explicit human decision gates for sensitive actions.
- **Safety Guards**: Deterministic business rules (CommunicationGuard, RiskEngine, KillSwitch).
