# Data Quality & Contradiction Resolution

## The 7 Quality Dimensions

Data records are evaluated against 7 core dimensions:

1. **Completeness**: Ratio of mandatory domain attributes populated.
2. **Accuracy**: Conformance to schema regex, ranges, and validation constraints.
3. **Consistency**: Concordance across multi-source representations without contradiction.
4. **Freshness**: Record age relative to domain SLA freshness threshold ($T_{obs} \le T_{SLA}$).
5. **Validity**: Conformance to defined types and relational foreign keys.
6. **Uniqueness**: Absence of exact duplicate or near-duplicate entity instances.
7. **Provenance**: Traceability to source actors, agents, or authoritative upstream systems.

## Contradiction Detection

Contradictions are detected deterministically across differing sources:

```text
Source A (Hubspot):       employee_count = 50,  budget = $100,000
Source B (AI Discovery):  employee_count = 250, budget = $500,000
      ↓
Conflict Flagged: ["employee_count", "budget"]
Status: DETECTED / UNRESOLVED
```

Conflicts are stored in `data_conflicts` and can be resolved by selecting a winning source or recording human corrections without silent data loss.
