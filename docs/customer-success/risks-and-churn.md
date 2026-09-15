# Proactive Risk Matrix & Churn Detection

## 1. Risk Categories

* **`RELATIONSHIP`**: Sponsor departure, executive disengagement, contact turnover.
* **`FINANCIAL`**: Unpaid invoices, billing disputes, budget freeze.
* **`DELIVERY`**: Milestone slippage, unresolved blockers, scope creep.
* **`SUPPORT`**: Unresolved critical incidents, repeated SLA breaches.
* **`SATISFACTION`**: Negative communication sentiment, low CSAT responses.
* **`CONTRACT`**: Approaching expiration without renewal activity.

## 2. Risk Detection Rule Engine

The `CustomerSuccessRiskDetector` scans operational telemetry:
* Health score $< 50.00$ $\rightarrow$ High Churn Risk.
* Unpaid overdue invoices $\ge 1$ $\rightarrow$ Financial Payment Risk.
* Inactivity $> 30$ days $\rightarrow$ Stakeholder Relationship Inactivity.
* Negative sentiment ratio $\ge 40\%$ $\rightarrow$ Satisfaction Degradation.
* Renewal window $\le 60$ days with health $< 70.00$ $\rightarrow$ Contract Renewal at Risk.
