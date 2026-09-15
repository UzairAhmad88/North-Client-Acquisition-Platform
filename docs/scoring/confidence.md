# Confidence Rating & Missing Data Policy

## Confidence Levels

- `HIGH`: Business profile complete, Audit completed and available, Research records verified.
- `MEDIUM`: Business profile complete and Audit or Research data available.
- `LOW`: Minimal inputs available (e.g., Business CRM record only, Audit missing or failed).

## Missing Data Handling

Missing data does not automatically set a score component to 0 or negative without factual basis.
- `UNKNOWN`: Input data not yet collected; component assigns baseline default and lowers overall score confidence.
- `ZERO`: Confirmed observation that feature/signal is completely absent.
- `NOT_APPLICABLE`: Dimension does not apply to this business model.
