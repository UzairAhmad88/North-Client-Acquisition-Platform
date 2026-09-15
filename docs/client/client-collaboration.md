# Client Collaboration & Communication Architecture

This document describes the client interaction layer and AI agent guardrails in **Uzaii Develop By North's Phase 27**.

---

## 1. Internal vs External Communication Policy

All client workspace discussions maintain strict visibility partitioning:
- **`INTERNAL_ONLY`**: Raw developer chat, cost discussions, internal labor margins, private engineering risks.
- **`CLIENT_VISIBLE`**: Sanitized, client-ready communication threads and deliverables.

Outbound external communications (Email, Slack, WhatsApp) must route through the server-side **Communication Guard** (Phase 19).

---

## 2. ClientCollaborationAgent v1.0 Guardrails

`ClientCollaborationAgent` executes four core tasks:
1. **CLASSIFY_REQUEST**: Categorizes incoming client requests (`IN_SCOPE`, `BUG`, `SUPPORT`, `CONTENT`, `POTENTIAL_SCOPE_CHANGE`).
2. **SUMMARIZE_FEEDBACK**: Aggregates deliverable comments into key takeaways and revision flags.
3. **EXTRACT_ACTIONS**: Pulls out required client inputs (API keys, brand assets).
4. **EVALUATE_SCOPE**: Detects scope expansion triggers in conversation text.

### Prohibited Actions Policy

The agent is strictly prohibited from autonomous side-effect actions:
- ❌ `APPROVE_DELIVERABLE`
- ❌ `APPROVE_SCOPE_CHANGE`
- ❌ `CHANGE_CONTRACT`
- ❌ `MODIFY_BASELINE`
- ❌ `SEND_EXTERNAL_MESSAGE`
- ❌ `CHANGE_PRICE`
- ❌ `PROMISE_DEADLINE`
