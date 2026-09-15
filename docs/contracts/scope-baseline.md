# Scope Commitment & Baseline Engine

## Overview
The Scope Baseline Engine guarantees that once a contract is executed, the agreed project scope, technical commitments, delivery milestones, SLA metrics, and financial pricing are locked into an immutable `ContractBaseline`.

---

## Why Baselines Matter
In client engagements, scope creep and mismatched expectations occur when client agreements deviate from delivery execution. The `ContractBaseline` resolves this by creating a fixed snapshot at execution time.

```text
Proposal (Phase 23/24)
        ↓
Contract Execution (Phase 25)
        ↓
[ ContractBaseline Locked ]  <-- Immutable Golden Master
        ↓
Project Management & Delivery Execution
```

---

## Baseline Structure (`ContractBaseline`)

| Attribute | Type | Purpose |
|---|---|---|
| `baseline_id` | UUID | Unique immutable baseline identifier |
| `contract_id` | UUID | Foreign key referencing executed contract |
| `version_number` | Integer | Version number of contract locked in baseline |
| `locked_scope_items` | JSON | List of committed scope deliverables, features, and non-functionals |
| `locked_deliverables` | JSON | Structured deliverable specs with acceptance criteria |
| `locked_milestones` | JSON | Target delivery dates and payment release triggers |
| `locked_total_amount` | Decimal | Total agreed contract valuation |
| `locked_currency` | String | Financial currency (e.g. `USD`, `PKR`) |
| `locked_sla_terms` | JSON | Agreed SLA parameters (e.g., support response times, uptime) |
| `baseline_hash` | String | SHA-256 hash of entire baseline object for anti-tamper auditing |
| `created_at` | DateTime | Timestamp when baseline was locked |

---

## Discrepancy Engine & Continuous Drift Monitoring
The `ContractDiscrepancy` system continuously monitors alignment between proposals, estimates, and contract text.

### Discrepancy Categories
1. `SCOPE_MISMATCH`: Items present in proposal/estimate missing from contract text (or vice versa).
2. `PRICE_MISMATCH`: Contract total amount deviates from Phase 24 Commercial Estimate total.
3. `TIMELINE_MISMATCH`: Milestone target dates contradict solution design phases.
4. `SLA_MISMATCH`: Support parameters differ from standard policy or approved estimate.
5. `MISSING_SECTION`: Key required contract section (e.g., Payment Terms, IP Rights, Confidentiality) is absent.

### Resolution Workflow
* Discrepancies are flagged during `ContractAgent` validation.
* Any `CRITICAL` discrepancy blocks internal operator approval.
* Operators can mark discrepancies `RESOLVED` with rationale or update contract text to match proposal baselines.
