# Saga Orchestration & Distributed Consistency

## Long-Running Sagas

Multi-step business processes (e.g. Contract Signing $\rightarrow$ Project Creation $\rightarrow$ Milestone Allocation $\rightarrow$ Workspace Provisioning) operate under a forward-recovery Saga orchestrator.

## Failure Containment Principles

1. **Deterministic Pause & Human Intervention**: Unlike simple web transactions, business operations with legal or financial side-effects (e.g., signing contracts, sending outbound emails, modifying baselines) must never execute automated rollbacks that undo legal realities.
2. **Crash Resilience**: State is committed durably to PostgreSQL at every step boundary. Worker crashes or server restarts simply resume execution at the current active step without duplicating prior succeeded actions.
3. **Poison Message Containment**: If a step encounters a fatal schema or business rule failure, the step is marked `FAILED`, the workflow enters `BLOCKED`, and a Dead Letter message is created for operator review.
