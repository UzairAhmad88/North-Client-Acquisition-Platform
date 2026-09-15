# Security, Isolation & Authorization in Search and Commands

## 1. Multi-Tenant Boundary Enforcement

Multi-tenancy is enforced at the earliest possible stage in every pipeline:

```text
Request (AuthContext: tenant_id="t-1", role="client")
   │
   ▼
[Authorization Layer] ──► Inject mandatory `tenant_id = 't-1'` into Search Index filter
   │
   ▼
[Storage / Vector Layer] ──► Scoped strictly to partition `t-1`
   │
   ▼
[Post-Retrieval Filter] ──► Verification that entity belongs to `t-1`
```

No search query, autocomplete suggestion, command parsing, or assistant retrieval can query outside the caller's verified `tenant_id`.

---

## 2. Client Visibility Boundaries

Users with the role `CLIENT` have strict data isolation boundaries:

- **Prohibited Entities**: Client accounts are blocked from searching or querying internal developer items, cost sheets, supplier bids, or raw AI governance traces.
- **Field Masking**: Sensitive fields such as internal developer notes, gross margins, risk severity calculation weights, and raw system prompts are automatically redacted from search snippets and assistant context.
- **Client Visibility Filter**: Searches by client users automatically append `client_visible = True` to all query plans.

---

## 3. Command Security & Approval Gates

1. **Default-Deny Model**: If a command is not explicitly registered and authorized for the caller's role, execution is immediately rejected (`403 Forbidden` / `STATUS: FORBIDDEN`).
2. **Action Confirmation**: State-modifying operations require `has_confirmation=True`.
3. **Approval Gating**: Critical financial, contractual, and communication actions (`action.send_proposal`, `action.approve_contract`) require explicit approval tokens and audit tracking.
4. **Immutable Audit Trail**: Every command parsed, validated, rejected, pending, or executed generates an audit record in `command_audit_events`.

---

## 4. Prompt Injection Defense

All platform assistant context synthesis adheres to the following defenses:

1. **No System Prompt Leakage**: Explicit model guidelines against echoing internal system prompts.
2. **Context Escaping**: Records are encapsulated in `<UNTRUSTED_RETRIEVED_DATA>` XML-style blocks.
3. **Delimiter Stripping**: Token patterns matching delimiter injection exploits are stripped during context construction.
4. **Grounded Synthesis**: The assistant declines to answer or hallucinate when supporting citations are absent in the retrieved tenant data.
