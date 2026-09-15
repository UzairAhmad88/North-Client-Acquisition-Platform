# Transactional Outbox & Deduplicated Inbox Patterns

## Transactional Outbox Pattern

To eliminate dual-write inconsistencies (updating DB but failing to publish event), domain changes and event records are committed in the same database transaction.

```text
┌────────────────────────────────────────────────────────┐
│               PostgreSQL Single Transaction             │
│                                                        │
│   1. INSERT INTO leads (id, status, ...)               │
│   2. INSERT INTO event_outbox (event_id, event_type...)│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
               Outbox Background Worker
                            │
                            ▼
                     Central Event Bus
```

## Deduplicated Consumer Inbox

Consumers protect against duplicate event delivery by verifying incoming `event_id` against the `event_inbox` table.

```python
if await InboxConsumer.is_duplicate(db, event.event_id, consumer_name):
    # Safely skip processing; idempotent ignore
    return {"status": "DUPLICATE_IGNORED"}
```

## Idempotency Keys

Every workflow action compute deterministic SHA-256 keys based on:
$$\text{key} = \text{SHA256}(\text{workflow\_id} : \text{step\_key} : \text{attempt\_group})$$
Preventing duplicate external executions during worker crash recoveries or transient network retries.
