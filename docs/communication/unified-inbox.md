# Unified Inbox & State Model

## 1. Specification

The Unified Inbox provides users with a centralized, deduplicated stream of actionable alerts, conversation messages, task assignments, and system events.

### Inbox Item States
- `UNREAD`: Newly arrived item awaiting user interaction.
- `READ`: Marked as viewed by the user. Note: `READ` is purely informational and **never** authorizes an action or approves a contract.
- `SNOOZED`: Temporarily hidden until `snoozed_until` timestamp, after which it reappears in active views.
- `ARCHIVED`: Retained in historical records but hidden from active triage feeds.
- `ACTION_REQUIRED`: High-priority items awaiting a distinct decision (e.g. approval button click).
- `COMPLETED`: Associated task or action concluded.

---

## 2. Reading $\neq$ Approval Guardrail

A fundamental operational rule of **Uzaii Develop By North's**:

$$\text{Reading an Item} \neq \text{Approving a Workflow}$$
$$\text{Opening a Thread} \neq \text{Accepting Contract Terms}$$

All approvals require explicit cryptographic or role-authorized action endpoints (e.g. `/api/v1/contracts/{id}/approve` or `/api/v1/changes/{id}/sign-off`) and cannot be triggered by GET requests or read status updates.
