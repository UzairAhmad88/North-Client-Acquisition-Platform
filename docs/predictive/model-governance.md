# Model Governance, Lifecycle & Audit Trails

## Lifecycle States

All predictive models deployed within the platform transition through strictly audited lifecycle states:

```text
EXPERIMENTAL → VALIDATING → APPROVED → PRODUCTION → DEPRECATED → ARCHIVED
```

- **EXPERIMENTAL**: Newly initialized or retrained candidate models. Evaluated strictly in shadow or offline testing environments.
- **VALIDATING**: Models undergoing statistical validation (ROC-AUC, Calibration Error, Brier Score, MAE).
- **APPROVED**: Formally validated models awaiting authorized deployment approval.
- **PRODUCTION**: Currently active model serving live inference requests.
- **DEPRECATED**: Replaced by newer validated version; preserved for historical auditability.
- **ARCHIVED**: Fully retired models with permanent historical snapshot records.

## Audit & Compliance Controls

1. **Explicit Sign-off**: Every model version requires an explicit `approved_by` identity and timestamp before being promoted to `PRODUCTION`.
2. **Immutable Snapshot Logs**: All predictions are permanently recorded in `prediction_records` alongside the exact model version, feature vector checksum, and confidence bounds.
3. **Drift Monitoring**: Automated tasks calculate distribution drift on features and prediction distributions, raising `ModelDriftEvent` alerts if statistical divergence exceeds tolerances.
4. **No Automated Retraining Deployments**: Retraining workflows can produce candidate model artifacts, but automated live swapping is strictly forbidden.
