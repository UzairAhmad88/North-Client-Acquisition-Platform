# Notifications, Policies & Quiet Hours

## 1. Notification Policy Engine

The Communication Policy Engine determines whether a notification should be delivered immediately, queued, deferred for quiet hours, or escalated across multiple channels.

### Notification Categories
- `SYSTEM`: Infrastructure alerts, deployment status, database health.
- `OPERATIONAL`: Build completions, background jobs, sync tasks.
- `SECURITY`: Anomalous logins, credential updates, permission escalations.
- `APPROVAL`: Contract sign-offs, change request approvals, budget overrides.
- `WORKFLOW`: Step progression in multi-agent or human orchestration pipelines.
- `SALES` / `CLIENT` / `SUPPORT` / `BILLING` / `AI`: Domain-specific communications.

---

## 2. Quiet Hours & Mandatory Security Bypass

Users can configure custom quiet-hour windows (e.g. 22:00 to 07:00 in their local timezone).

### Policy Rules
1. **Normal & Low Priority**: External channels (Email, SMS, Push) are suppressed or queued until quiet hours conclude. In-App notifications remain accessible.
2. **Critical Security Override**:
   - Notifications categorized under `SECURITY` or prioritized as `CRITICAL` **strictly bypass** quiet hours.
   - Core delivery channels cannot be disabled in user preferences.
   - Guaranteed multi-channel delivery ensures safety and compliance.
