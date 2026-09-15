# Task Dispatcher & Priority Queues

## Priority Queues

The `TaskDispatcher` schedules and dispatches executable work items across five distinct priority levels:

| Priority Tier | Queue Name | SLA Target | Use Cases |
| :--- | :--- | :--- | :--- |
| `CRITICAL` | `critical` | < 1,000 ms | Security alerts, Emergency kill switches |
| `HIGH` | `high` | < 5,000 ms | Client webhook responses, Human approval resumptions |
| `NORMAL` | `default` | < 30,000 ms | Discovery, Research, Audit, Solution workflows |
| `LOW` | `low` | < 120,000 ms | Daily metric rollups, Forecast recalibrations |
| `BACKGROUND` | `background`| Best Effort | Event replays, Historical benchmark suites |

## Concurrency Control & Distributed Locks

The `DistributedLockManager` enforces atomic execution on sensitive shared aggregates (`WorkflowTaskLock`), preventing race conditions when multiple worker nodes process concurrent events for the same lead, project, or contract.
