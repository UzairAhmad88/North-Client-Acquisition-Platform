# Service Recommendation System Architecture

## Overview

The **North's Service Recommendation Engine** is an explainable, evidence-based system designed to evaluate business profiles, digital presence, website audit findings, lead opportunity scores, and existing lead context against North's Service Catalog.

---

## Core Pipeline

```
                                +-------------------+
                                |    Lead Record    |
                                +---------+---------+
                                          |
        +------------------+--------------+--------------+------------------+
        |                  |                             |                  |
+-------v-------+  +-------v-------+             +-------v-------+  +-------v-------+
|  Business CRM |  |Research Engine|             | Website Audit |  |  Lead Scoring |
+-------+-------+  +-------+-------+             +-------+-------+  +-------+-------+
        |                  |                             |                  |
        +------------------+--------------+--------------+------------------+
                                          |
                                 +--------v--------+
                                 | Service Catalog |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  Signal Engine  |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |   Rule Engine   |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Relevance Score |
                                 |  & Band Mapper  |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Evidence, Limits|
                                 | & Confidence    |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Priority Mapper |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Human Decision  |
                                 | (Accept/Reject) |
                                 +-----------------+
```

---

## Architectural Principles

1. **Recommend from Evidence, Not Assumptions**: Recommendations trace back to observable data points from audit findings, research records, or business attributes.
2. **Relevance Fit ≠ Sales Commitment**: Scores reflect domain service relevance, NOT purchase probability or customer intent.
3. **Human Decision Authority**: Automated recalculations never overwrite human `ACCEPTED` or `REJECTED` decisions.
4. **Deterministic & Auditable**: Built on rule-based candidate selection without black-box ML or unvalidated inferences.
