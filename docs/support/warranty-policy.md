# Contractual Warranty Governance & Defect Policy — Phase 30

## 1. Warranty Eligibility Grounding

Warranty coverage is strictly bounded by the delivered contract baseline deliverables from Phase 25/26/29:
- **Eligible Defect Categories**: Functional regressions, baseline code defects, broken integration points approved in UAT.
- **Warranty Window**: Standard 30, 60, or 90 days from Handover Sign-off date.

## 2. Mandatory Warranty Exclusions

The following conditions are contractually excluded from free defect warranty and require billable support or Phase 28 Change Management:
1. **Third-Party Outages**: AWS/GCP/Azure downtime, external SaaS API rate limits, third-party payment gateway disruptions.
2. **Unauthorized Modifications**: Client alterations to application source code, infrastructure, database schemas, or configurations without North's consent.
3. **Out-of-Scope Scope Creep**: New features or workflow alterations not documented in the signed specification baseline.
4. **Environment Misuse**: Operating software outside documented hardware/software runtime requirements.

## 3. Human-in-the-Loop Decision Enforcement

AI engines draft warranty eligibility evaluations based on the text of the issue and baseline deliverables. However:
- **No AI Autonomous Approval**: An authorized Human Supervisor (`HUMAN_OPERATIONS_LEAD`) must sign off on any warranty coverage decision.
- All decisions are permanently recorded in the immutable `SupportRequestEvent` audit trail.
