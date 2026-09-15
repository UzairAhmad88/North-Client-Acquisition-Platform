# Phase 37 — Communication & Notification Architecture

## 1. Subsystem Architecture

The Phase 37 Unified Communication Platform serves as the central router and delivery layer for all internal and external events in **Uzaii Develop By North's**.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        SOURCE DOMAIN ENGINES                           │
│ (Sales, Research, Contracts, Projects, QA, Support, Security, AI Bus)   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                        Emits Operational Events
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      COMMUNICATION POLICY ENGINE                       │
│  - Policy matching by category & priority                              │
│  - Quiet Hours evaluation                                              │
│  - Mandatory Security Override check (CRITICAL_SECURITY bypass)        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     AUDIENCE RESOLUTION & SAFETY                       │
│  - Tenant isolation filtering                                          │
│  - Role / Project / Lead recipient expansion                          │
│  - Client visibility boundary protection                               │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  DEDUPLICATION & AGGREGATION ENGINE                    │
│  - Fingerprint generation & Idempotency key tracking                   │
│  - Time-window rate limiting                                           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     CHANNEL DISPATCH & DELIVERY                        │
│  ├── In-App (Unified Inbox Persistence & Badge Counters)               │
│  ├── Realtime WebSocket (Presence & Live Event Gateway)                │
│  ├── Email / SMS Adapters                                              │
│  └── Webhooks & Push Notifications                                     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  DELIVERY AUDIT & ERROR DLQ / RETRY                    │
│  - Provider message IDs and delivery timestamps                        │
│  - Retry counters & Exponential backoff                                │
│  - Dead-Letter Queue (DLQ) for failed dispatches                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Entities & Lifecycle

1. **`NotificationRecord`**: Immutable record of system-generated notifications.
2. **`InboxItemRecord`**: Recipient-specific inbox item with user state (`UNREAD`, `READ`, `SNOOZED`, `ARCHIVED`, `ACTION_REQUIRED`).
3. **`ConversationRecord`**: Multi-party or direct conversation threads scoped by tenant and linked to projects, contracts, or support tickets.
4. **`ConversationMessageRecord`**: Messages and internal notes with immutable version history snapshotting.
5. **`CommunicationDeliveryRecord`**: Channel-level delivery attempt telemetry, timestamps, provider IDs, and error payloads.
6. **`NotificationPreferenceRecord`**: Per-user channel preferences and quiet hours configuration.
