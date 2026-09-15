# Post-Delivery Support System Architecture — Phase 30

## 1. Executive Summary

Phase 30 establishes the **Post-Delivery Support, Maintenance, Warranty & Client Success System** for the Uzaii platform. It completes the operational lifecycle by ensuring that delivered projects receive deterministic issue classification, contractual warranty governance, SLA-bound incident response, scheduled preventative maintenance, and account expansion intelligence.

```
+-----------------------------------------------------------------------------------+
|                        CLIENT SUPPORT / INCIDENT SUBMISSION                       |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        SUPPORT CLASSIFIER & TRIAGE ENGINE                         |
|   (DEFECT vs SUPPORT vs MAINTENANCE vs INCIDENT vs CHANGE_REQUEST vs NEW_PROJECT) |
+-----------------------------------------------------------------------------------+
         |                        |                          |                   |
         v                        v                          v                   v
+------------------+     +------------------+     +------------------+    +------------------+
|  DEFECT TRIAGE   |     |    INCIDENTS     |     |   MAINTENANCE    |    |  SCOPE CHANGE    |
| - Warranty Check |     | - SEV-1 to SEV-4 |     | - Work Orders    |    | - Route Phase 28 |
| - Root Cause AI  |     | - Timelines      |     | - Scheduled Run  |    |   Change Mgmt    |
| - SLA Timers     |     | - Postmortem     |     | - CVE Audits     |    | - Opportunity    |
+------------------+     +------------------+     +------------------+    +------------------+
```

---

## 2. Core Operational Entities

1. **`SupportRequest`**: Client-submitted issues categorized deterministically into `DEFECT`, `SUPPORT`, `MAINTENANCE`, `CONFIGURATION`, `INCIDENT`, `CHANGE_REQUEST`, `NEW_PROJECT`, `QUESTION`, `TRAINING`, or `BILLING`.
2. **`SupportRequestVersion`**: Immutable version history for ticket updates.
3. **`SupportRequestEvent`**: Audit trail recording state transitions, SLA events, and AI advisories.
4. **`Incident` & `IncidentTimeline`**: Operational outage command tracking across SEV-1 through SEV-4 with milestone audit trails and postmortems.
5. **`Warranty`**: Authoritative contract baseline warranty coverage terms, start/end dates, and explicit exclusion conditions.
6. **`MaintenancePlan` & `MaintenanceWorkOrder`**: Preventative and scheduled maintenance plans with actionable work orders, checklists, and sign-offs.
7. **`KnowledgeArticle`**: Curated knowledge base articles, standard operating procedures, and runbooks.
8. **`ClientHealthSnapshot` & `SupportOpportunity`**: Telemetry and relationship health scoring with automated expansion opportunity generation.

---

## 3. Strict AI Guardrails & Permissions

The `SupportAgent` v1.0 operates under zero-trust safety constraints:
- **PROHIBITED ACTIONS**: `APPROVE_WARRANTY`, `CHANGE_CONTRACT`, `APPROVE_CHANGE`, `APPROVE_PAYMENT`, `ISSUE_REFUND`, `CLOSE_CRITICAL_INCIDENT`, `CHANGE_SLA`, `DELETE_SUPPORT_HISTORY`, `SEND_EXTERNAL_MESSAGE`, `MODIFY_CLIENT_BASELINE`.
- **Advisory Mode**: All AI classification, diagnostic troubleshooting, warranty assessments, and opportunity signals are strictly advisory drafts requiring human operations review.
