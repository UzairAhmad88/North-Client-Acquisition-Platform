# Incident Management & Blameless Postmortems

## 1. Severity Levels

| Severity | Definition | Target Acknowledge | Target Resolve (RTO) |
|---|---|---|---|
| **SEV-1 (Critical)** | Core platform or business outage affecting multiple tenants or primary database down. | $< 5\text{ mins}$ | $< 1\text{ hour}$ |
| **SEV-2 (Major)** | Significant degraded functionality (e.g. AI provider outage, invoice generation blocked). | $< 15\text{ mins}$ | $< 4\text{ hours}$ |
| **SEV-3 (Moderate)** | Non-critical component degraded (e.g. background analytics or search index lag). | $< 1\text{ hour}$ | $< 24\text{ hours}$ |
| **SEV-4 (Minor)** | Cosmetic defect, minor UI anomaly, non-blocking administrative issue. | $< 4\text{ hours}$ | Next Sprint |

## 2. Incident Lifecycle State Machine

```
DETECTED ──> ACKNOWLEDGED ──> TRIAGED ──> INVESTIGATING ──> MITIGATING ──> RECOVERING ──> RESOLVED ──> VERIFIED ──> POST_INCIDENT_REVIEW ──> CLOSED
```

## 3. Human Authorization & Evidence
- Incidents cannot be closed without verified operational evidence and root-cause documentation.
- SEV-1 and SEV-2 incidents mandate a **Blameless 5-Whys Postmortem Report** detailing root cause, detection timeline, containment steps, recovery verification, and preventive action items.
