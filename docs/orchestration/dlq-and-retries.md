# Retries & Dead Letter Queue (DLQ) Management

## Bounded Retry Strategy

Transient failures (e.g. network blips, AI provider 503s) are retried according to configurable exponential backoff with full jitter:

$$\text{delay} = \min\left(\text{max\_backoff}, \text{initial\_backoff} \times \text{multiplier}^{\text{attempt}-1}\right) \times \text{random}(0.5, 1.0)$$

## Dead Letter Queue (DLQ) Triage

When an event exceeds its maximum retry threshold or encounters a permanent unrecoverable failure (e.g. schema violation, poison message), it is captured into `dead_letter_messages`.

```text
Message in DLQ
      │
      ▼
Triage Statuses:
  ├── PENDING (Awaiting operator review)
  ├── INVESTIGATING (Under active analysis)
  ├── RETRY_SCHEDULED (Requeued for execution)
  ├── REPLAYED (Successfully reprocessed)
  ├── RESOLVED (Manually addressed)
  └── DISCARDED (Confirmed invalid)
```
