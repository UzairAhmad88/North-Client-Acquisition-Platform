# Evidence Validation & Coverage Subsystem

## Overview
Every factual claim embedded in an AI draft must be traceable to underlying research or audit data.

## Evidence Coverage Calculation

$$\text{Evidence Coverage} = \frac{\text{Supported Claims}}{\text{Total Factual Claims}}$$

### Claim Classifications
- `VERIFIED`: Linked directly to an observed audit finding or verified research record.
- `INFERRED`: Derived deterministically from verified business metrics.
- `GENERAL`: General consultative phrasing or proposal context (does not require evidence linking).
- `UNSUPPORTED`: Factual claim with no supporting evidence record.
- `CONTRADICTED`: Claim directly contradicted by observed audit data.

If `Evidence Coverage < 0.50`, rule `R-EVIDENCE-COVERAGE-LOW` triggers a `HIGH` severity finding (`REVIEW`).
