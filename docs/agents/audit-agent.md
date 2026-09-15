# Phase 16 — Audit Agent Specification

## 1. Executive Summary
The **Audit Agent** transforms the **Phase 11 Audit System** into an intelligent, structured, evidence-aware agent workflow operating through the **Phase 14 Agent Core Runtime**.

The agent performs passive, read-only public digital assessments (website availability, HTTPS, mobile signals, SEO baselines, lead-capture CTAs, business information consistency) while enforcing strict security boundaries, evidence grounding, and human-in-the-loop decision boundaries.

---

## 2. Architecture & Design Principles

### 2.1 Runtime Integration
- **Agent Registry**: Registered under `audit_agent` v1.0 in `AgentRegistry`.
- **Context Awareness**: Receives `AgentContext` containing `business_profile`, `research_data`, `existing_audit`, and `metadata`.
- **State Management**: Execution steps tracked via Phase 14 `AgentRunRepository` (`PENDING`, `RUNNING`, `COMPLETED`, `PARTIAL`, `NO_WEBSITE`, `FAILED`).

### 2.2 Permissions Scoping
The agent operates under strict read-only permissions:
- **Granted Permissions**:
  - `READ_BUSINESS`: Read public business profile.
  - `READ_LEAD`: Access associated lead context.
  - `READ_RESEARCH`: Inspect existing research records.
  - `READ_AUDIT`: Read existing audit snapshots.
  - `FETCH_WEB`: Fetch public web pages (Read-only GET).
  - `RUN_AUDIT`: Execute deterministic Phase 11 audit runner.
  - `CREATE_AUDIT_RECORD`: Persist verified audit records.
- **Prohibited Permissions (Strictly Denied)**:
  - `SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT`, `MODIFY_EXTERNAL_RESOURCE`, `DELETE_DATA` (Zero autonomous side-effects or external modifications).

---

## 3. Target Selection & Freshness Policy

### 3.1 Target Selection Hierarchy
```
1. Explicitly requested target URL
2. Verified official website from Business Profile
3. Trusted website from Research records
4. User-provided website
5. NO_WEBSITE (Explicit audit outcome)
```

### 3.2 Audit Freshness Policy
- Existing audits $\le 7$ days old are reused to avoid redundant network crawling.
- Stale audits ($> 7$ days) trigger a fresh deterministic measurement run.

---

## 4. Finding Severity & Confidence Ratings

### 4.1 Severity Classification (Observable Impact)
- `HIGH`: Website down, no HTTPS.
- `MEDIUM`: Missing viewport tag, no contact CTA, contact phone discrepancy between research and website.
- `LOW`: Missing meta description, missing security header.
- `INFO`: Form detected, booking link detected.

### 4.2 Confidence Ratings
- `HIGH`: Direct website measurement, fresh ($\le 7$ days), no conflicts.
- `MEDIUM`: Research-derived signal or older direct observation.
- `LOW`: Weak inference without direct measurement.
