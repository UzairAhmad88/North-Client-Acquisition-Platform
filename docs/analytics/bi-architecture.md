# Business Intelligence & Portfolio Analytics Architecture

## 1. Overview & Core Principle

Phase 31 transforms the historical operational data across the full platform lifecycle (Discovery $\to$ Lead Gen $\to$ Research $\to$ Audit $\to$ Qualification $\to$ Outreach $\to$ Conversation $\to$ Requirements $\to$ Solution $\to$ Estimation $\to$ Proposal $\to$ Contract $\to$ Project $\to$ Change Management $\to$ QA $\to$ UAT $\to$ Delivery $\to$ Support $\to$ Warranty $\to$ Maintenance $\to$ Client Success) into a **measurable, evidence-backed organizational learning system**.

### The Non-Negotiable Core Principle:
> **The platform learns from historical outcomes, but historical correlation must NEVER automatically become business truth or modify production policies.**

```text
RAW OPERATIONAL DATA
        ↓
DATA NORMALIZATION & REGISTRY
        ↓
METRICS & ANALYTICS
        ↓
PATTERN DETECTION
        ↓
INSIGHTS (Evidence Grounded)
        ↓
RECOMMENDATIONS
        ↓
HUMAN DECISION (Review Gate)
        ↓
CONTINUOUS EXPERIMENT (Trial Testing)
        ↓
MEASURED OUTCOME & ORGANIZATIONAL LEARNING
```

---

## 2. Four Intelligence Layers

1. **Descriptive Intelligence (What happened?)**:
   - Researched lead volumes, proposal send rates, active delivery counts, SLA adherence, and authoritative realized revenues.
2. **Diagnostic Intelligence (Why did it happen?)**:
   - PERT effort variance $(Actual - Estimated) / Estimated$, scope change root cause attribution (e.g., incomplete initial requirements), and escaped defect leakage rates.
3. **Predictive Intelligence (What may happen?)**:
   - Probabilistic lead conversion scoring bands, project schedule overrun likelihoods, and support demand forecasting with confidence intervals.
4. **Prescriptive Intelligence (What might we do?)**:
   - Empirical recommendations with articulated expected benefits, potential downsides, affected workflows, and required human sign-off gates.

---

## 3. Security & Boundary Guardrails

- **Zero Autonomous Policy Changes**: System and AI agents cannot unilaterally modify pricing, scoring weights, SLA policies, hourly rates, or agent permissions (`ANALYTICS_AUTO_POLICY_CHANGE=false`).
- **Semantic Layer vs Arbitrary SQL**: Natural language analytics requests are mapped strictly through approved parameterized metric models. Raw SQL generation and execution by AI is prohibited (`EXECUTE_ARBITRARY_SQL` is forbidden).
- **Financial Segregation**: Strict separation between `ACTUAL` realized revenue, `FORECAST` pipeline, and unaccepted `ESTIMATE` proposal values.
