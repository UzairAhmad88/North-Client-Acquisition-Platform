# Incident Management & Severity Governance — Phase 30

## 1. Severity Definitions

| Severity | Definition | Target Response | Target Containment | Lead Commander |
| :--- | :--- | :--- | :--- | :--- |
| **SEV-1 (Critical Outage)** | Complete service unavailability, severe data loss, or active security breach. | 15 Minutes | 2 Hours | Lead DevOps / CTO |
| **SEV-2 (Major Impact)** | Primary business capability degraded, core payment/auth failure for subset of users. | 30 Minutes | 4 Hours | Senior Support Lead |
| **SEV-3 (Moderate Degradation)** | Non-critical functionality glitch, UI distortion, background sync delay. | 2 Hours | 24 Hours | Support Engineer |
| **SEV-4 (Minor)** | Minor cosmetic issue or documentation inconsistency without operational block. | 8 Hours | 72 Hours | On-call Engineer |

---

## 2. Incident Command Lifecycle

```
[DETECTED] ---> [ACKNOWLEDGED] ---> [MITIGATING / CONTAINMENT] ---> [RESOLVED] ---> [CLOSED / POSTMORTEM]
```

1. **Detection & Declaration**: Automated monitoring telemetry or manual escalation. Initial timeline event recorded.
2. **Containment**: Rapid isolation, rollback, or capacity scale-up to halt blast radius.
3. **Remedy & Verification**: Hotfix deployment or configuration repair verified against monitoring signals.
4. **Postmortem (RCA)**: Mandatory root-cause analysis, timeline breakdown, and corrective action items before incident closure.
