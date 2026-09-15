# Personalization Agent Architecture & Operations

## Overview
The **Personalization Agent** (`personalization_agent` v1.0) is North's internal context and draft preparation engine built on top of the Phase 14 Agent Core Runtime. It synthesizes all available context about a Lead—including Business CRM, Lead CRM, Research Profile, Website Audit findings, Opportunity Score, Service Recommendations, and Qualification Assessment—to produce an evidence-backed personalization profile and channel-specific communication draft.

> **CRITICAL BOUNDARY**: The Personalization Agent strictly operates under a zero-autonomous-communication policy. It prepares internal context and drafts in `PENDING_APPROVAL` status only. It cannot send communications, approve its own drafts, make financial commitments, or modify external resources.

---

## Agent Permissions & Scope

| Permission Name | Granted | Purpose |
|-----------------|---------|---------|
| `READ_BUSINESS` | Yes | Read business profile metadata |
| `READ_LEAD` | Yes | Read lead lifecycle status & contact info |
| `READ_RESEARCH` | Yes | Read research profile records |
| `READ_AUDIT` | Yes | Read website audit findings |
| `READ_SCORE` | Yes | Read lead opportunity score |
| `READ_SERVICES` | Yes | Read service recommendations |
| `READ_QUALIFICATION` | Yes | Read qualification assessment |
| `READ_CRM_CONTEXT` | Yes | Read CRM notes and history |
| `CREATE_OUTREACH_DRAFT` | Yes | Save outreach draft record |
| `SEND_EMAIL` | **NO** | Prohibited |
| `SEND_MESSAGE` | **NO** | Prohibited |
| `SEND_WHATSAPP` | **NO** | Prohibited |
| `SEND_SMS` | **NO** | Prohibited |
| `MAKE_PAYMENT` | **NO** | Prohibited |

---

## Qualification Gate & Do-Not-Contact (DNC) Rules

1. **Do-Not-Contact (DNC)**: Leads marked as DNC are automatically assigned `outreach_readiness = OUTREACH_BLOCKED`. No sendable draft is generated.
2. **`NOT_QUALIFIED` / `INSUFFICIENT_DATA`**: Prevents sendable draft generation (`outreach_readiness = NOT_RECOMMENDED`).
3. **`NEEDS_REVIEW`**: Permits internal draft creation with `outreach_readiness = NEEDS_MANUAL_REVIEW`.
4. **`QUALIFIED` / `POTENTIALLY_QUALIFIED`**: Permits normal evidence-backed personalization with `outreach_readiness = READY`.

---

## Fabricated Claims & Safety Defense

All claims in generated drafts must map to verified evidence. The `ClaimValidator` automatically flags or blocks:
- **Hype & Guarantees**: Guaranteed rankings, guaranteed 50% revenue growth, 100% conversion promises.
- **False Urgency**: "Competitors are taking your customers", "act today or lose out".
- **Fabricated Social Proof**: Fake testimonials, unverified portfolio references, or invented contact details.

---

## Communication Channels & Tone Support

- **Channels**: `EMAIL`, `WHATSAPP`, `SMS`, `LINKEDIN`.
- **Tones**: `PROFESSIONAL`, `FRIENDLY`, `CONCISE`, `CONSULTATIVE`, `LOCAL_BUSINESS`.
- **Depths**: `LIGHT`, `STANDARD`, `DEEP`.
