# Effort & Time Tracking Engine

## Overview
Phase 24 established PERT three-point commercial effort estimates. Phase 26 tracks actual logged effort against tasks and computes schedule/effort variance metrics.

---

## Variance Calculations

### Effort Variance
$$\text{Effort Variance (Hours)} = \text{Total Actual Hours} - \text{Total Estimated Hours}$$

- Positive Variance ($> 0$): Project is exceeding estimated effort hours.
- Negative Variance ($< 0$): Project is completing ahead of effort estimate.

---

## Immutable Historical Estimate Rule
The original `ProjectEstimate` created in Phase 24 remains historically immutable. Actual effort entries (`EffortEntry`) are recorded separately to preserve baseline auditability.
