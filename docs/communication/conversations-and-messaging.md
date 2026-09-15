# Conversations, Messaging & Client Visibility Boundaries

## 1. Thread Management & Types

Conversations link team members, agents, and clients to domain entities:
- `PROJECT`: Linked to delivery projects, tasks, and milestone reviews.
- `CONTRACT`: Linked to commercial contract negotiation and terms.
- `PROPOSAL`: Linked to solution scoping and estimate discussions.
- `SUPPORT`: Linked to issue triage and client ticketing.
- `INTERNAL` / `DIRECT`: Internal team or 1-on-1 collaboration.

---

## 2. Client Visibility Boundary

A core security guardrail separates internal notes from client-visible messages:

```text
┌────────────────────────────────────────────────────────┐
│               CONVERSATION MESSAGE STREAM              │
├──────────────────────────┬─────────────────────────────┤
│  Message Visibility      │ Recipient Accessibility     │
├──────────────────────────┼─────────────────────────────┤
│  CLIENT_VISIBLE          │ Internal Team & Client      │
│  INTERNAL (Notes)        │ Internal Team Only (HIDDEN) │
│  RESTRICTED              │ Security & Tenant Admins    │
│  SYSTEM                  │ Automated Audit Logs        │
└──────────────────────────┴─────────────────────────────┘
```

### Security Enforcement
- Any query initiated by a client user or client portal API strictly strips `INTERNAL` and `RESTRICTED` records.
- Client users cannot author messages with `visibility = 'INTERNAL'`.
- All message edits retain immutable historical snapshots in `conversation_message_version_records` for audit compliance.
