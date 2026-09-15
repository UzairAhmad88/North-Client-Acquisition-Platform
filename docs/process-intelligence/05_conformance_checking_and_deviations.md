# Conformance Checking and Operational Deviations

## Conformance Metrics
- **Fitness / Conformance Rate**: Proportion of observed traces perfectly replayable against the formal model without missing tokens.
- **Precision**: How closely the model restricts behaviors to only those actually observed.
- **Generalization**: How well the model accounts for unseen valid traces.

## Deviation Classification
1. **Missing Step**: Mandatory control or verification omitted.
2. **Unexpected Step**: Unapproved ad-hoc activity inserted.
3. **Rework Loop**: Redundant reprocessing caused by downstream defects.
4. **Skipped Approval**: Bypassed authorization gate violating policy.
5. **Unauthorized Path**: Rogue transition between secure states.\n