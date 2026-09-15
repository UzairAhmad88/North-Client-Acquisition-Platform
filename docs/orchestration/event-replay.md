# Event Replay & Time Travel Architecture

## 1. Overview

The Event Replay Engine (`backend/app/events/replay.py`) enables operators and developers to replay historical domain events through the platform without risking accidental external side-effects or corrupting active business baselines.

```text
HISTORICAL EVENTS (Database / Event Store)
               │
               ▼
       [ EventReplayEngine ]
       ├── Filter: Tenant, Subsystem, Event Types, Time Range
       └── Mode Assessment:
           ├── READ_ONLY: In-memory simulation only
           ├── DRY_RUN: Evaluates state changes without writes
           ├── REBUILD_PROJECTION: Recalculates analytical read-models
           └── CONTROLLED_REEXECUTION: Re-runs idempotent downstream tasks
               │
               ▼
    [ Side-Effect Guard Shield ]
    (Blocks: outreach.sent, contract.signed, proposal.accepted, etc.)
```

---

## 2. Replay Modes

| Mode | Purpose | Side Effects Allowed | Target State Modification |
| :--- | :--- | :--- | :--- |
| `READ_ONLY` | Auditing & debugging event progression | ❌ None | ❌ None |
| `DRY_RUN` | Verifying workflow rule execution & schema changes | ❌ None | ❌ None |
| `REBUILD_PROJECTION` | Rebuilding analytical data marts, views, or search indices | ❌ None (Internal DB only) | Read-model projections only |
| `CONTROLLED_REEXECUTION` | Recovering missed downstream tasks after bug fixes | Controlled & Idempotent only | Yes (with full audit trace) |

---

## 3. Side-Effect Shielding & Guardrails

To preserve platform safety and legal/commercial compliance, high-impact events are strictly shielded from re-execution during replay routines:

```python
SENSITIVE_REPLAY_BLOCKS = {
    "outreach.sent",          # Prevents duplicate emails/messages to prospects
    "contract.signed",        # Prevents unintended legal status transitions
    "proposal.accepted",      # Prevents duplicate commercial engagements
    "delivery.accepted",      # Prevents duplicate client signoffs
    "change.approved",        # Prevents unauthorized baseline modifications
    "commercial.payment_requested", # Prevents duplicate financial transactions
}
```

If an event matching these types is encountered during replay, the engine logs a `REPLAY_SHIELD_TRIGGERED` audit entry and skips external invocation while preserving event flow continuity.

---

## 4. Replay Execution Workflow

1. **Initiate Replay Session**: An authorized administrator submits a replay request specifying the filter criteria and execution mode.
2. **Snapshot Creation**: The engine creates an isolated replay context with unique `replay_session_id`.
3. **Stream & Deduplicate**: Events are streamed chronologically from `events` table ordered by `occurred_at ASC`.
4. **Guard Evaluation**: Each event is checked against sensitivity lists and target handler contracts.
5. **Execution & Telemetry**: Event handlers process the event, emitting metrics and audit records tagged with `replay_session_id`.
6. **Session Summary**: The engine produces a report of processed, skipped, failed, and shielded events.
