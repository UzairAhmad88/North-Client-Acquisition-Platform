# Qualification Agent Architecture & Operations

## Overview
The **Qualification Agent** (`qualification_agent` v1.0) is North's internal evaluation agent built on top of the Phase 14 Agent Core Runtime. It synthesizes all available context about a Lead—including Business profile, Lead CRM state, Research profile, Website Audit findings, Lead Opportunity Score, and Service Recommendations—to determine if a Lead is worth pursuing, why, with what confidence level, and what information remains missing.

> **CRITICAL BOUNDARY**: The Qualification Agent is strictly an internal assessment tool. It operates under a zero-autonomous-communication policy and is forbidden from contacting leads or executing external side-effects.

---

## Agent Permissions & Scope

| Permission Name | Granted | Purpose |
|-----------------|---------|---------|
| `READ_BUSINESS` | Yes | Read business profile metadata |
| `READ_LEAD` | Yes | Read lead lifecycle status & contact preferences |
| `READ_RESEARCH` | Yes | Read research profile data |
| `READ_AUDIT` | Yes | Read website audit findings |
| `READ_SCORE` | Yes | Read lead opportunity score |
| `READ_SERVICES` | Yes | Read service recommendations |
| `READ_CRM_CONTEXT` | Yes | Read internal CRM notes & tags |
| `CREATE_QUALIFICATION_RESULT` | Yes | Save qualification result record |
| `SEND_EMAIL` | **NO** | Prohibited |
| `SEND_MESSAGE` | **NO** | Prohibited |
| `SEND_WHATSAPP` | **NO** | Prohibited |
| `MAKE_PAYMENT` | **NO** | Prohibited |

---

## Qualification Decision Matrix

The Qualification Agent evaluates multiple factors to arrive at one of five decisions:

1. **`QUALIFIED`**: High score, clear service fit, contactable, clean DNC status. Recommended for outreach.
2. **`POTENTIALLY_QUALIFIED`**: Moderate score or minor missing information, but strong signal.
3. **`NEEDS_REVIEW`**: Contradictory evidence, unresolved duplicate flags, or manual review needed.
4. **`NOT_QUALIFIED`**: Explicitly poor fit, out-of-scope business type, or zero contact channels.
5. **`INSUFFICIENT_DATA`**: Essential research or business metadata missing.

---

## Outreach Readiness Statuses

- **`READY`**: Lead passed qualification and clean DNC check.
- **`NEEDS_MANUAL_REVIEW`**: Requires human oversight before scheduling outreach.
- **`NOT_RECOMMENDED`**: Low opportunity score or weak service fit.
- **`OUTREACH_BLOCKED`**: DNC list match or explicit opt-out.

---

## Evidence Provenance & Audit Trail

All qualification factor evaluations contain explicit evidence references tracing back to specific research items, audit findings, or CRM properties. Opportunity Scores and Service Recommendation rankings are strictly preserved and never altered.
