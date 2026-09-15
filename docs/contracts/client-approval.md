# Client Approval & Acceptance Workflow

## Overview
The Client Approval Subsystem manages the audit trail, verification, and legal boundaries of client contract acceptance.

---

## Core Rules & Guardrails

> [!IMPORTANT]
> **Client Document Open $\neq$ Acceptance**
> Opening, viewing, downloading, or scrolling through a contract document is recorded for telemetry, but explicitly does **NOT** constitute legal acceptance or state transition.

> [!WARNING]
> **Explicit Client Action Required**
> Acceptance requires an explicit form submission by an authorized client representative containing:
> 1. Signer Full Name & Official Role / Title.
> 2. Signer Verified Email Address.
> 3. Explicit Acceptance Statement (e.g., *"I agree to the contract terms and scope commitments set forth above"*).
> 4. Client Machine Telemetry (IP Address & User-Agent).

---

## Acceptance Record Structure (`ContractClientAcceptance`)

| Attribute | Type | Purpose |
|---|---|---|
| `acceptance_id` | UUID | Primary key |
| `contract_id` | UUID | Target contract |
| `version_id` | UUID | Exact version accepted |
| `client_email` | String | Email of accepting party |
| `client_name` | String | Full name of accepting party |
| `client_title` | String | Role/title (e.g. CEO, CTO) |
| `acceptance_statement` | String | Exact assent text |
| `ip_address` | String | Client IPv4 / IPv6 address |
| `user_agent` | String | Client browser / device string |
| `accepted_at` | DateTime | Audit timestamp |

---

## Internal Approval vs. Client Acceptance

```mermaid
sequenceDiagram
    participant Agent as ContractAgent
    participant Operator as Internal Operator
    participant Client as Client Representative
    participant System as Contract System

    Agent->>System: Draft Contract Version (v1)
    System->>Operator: Submit for Internal Approval (IN_REVIEW)
    Operator->>System: Review & Internal Approve (INTERNAL_APPROVED)
    System->>Client: Send / Present Contract URL (SENT_TO_CLIENT)
    Client->>System: Open Document (Telemetry logged; state unchanged)
    Client->>System: Submit Explicit Acceptance Form
    System->>System: Log ContractClientAcceptance & Update State (CLIENT_ACCEPTED)
```
