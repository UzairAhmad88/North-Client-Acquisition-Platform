# Model Registry & ML Governance

## 1. Registry Architecture

Predictive models (such as lead conversion predictors, PERT variance models, and support demand forecasters) are cataloged in `model_registry` with immutable evaluation runs and predictions.

```text
model_id
tenant_id
model_key
name
purpose
version
model_type (deterministic_baseline, regression, classifier)
features
training_window
evaluation_metrics (MAE, RMSE, accuracy, F1)
status (EXPERIMENTAL, VALIDATING, APPROVED, PRODUCTION, DEPRECATED)
approved_by
approved_at
```

---

## 2. Governance Rules

1. **Deterministic Baseline First**: Complex machine learning models are not deployed when insufficient sample sizes exist ($<100$ records).
2. **Human Approval Required**: No model can enter `PRODUCTION` status without explicit human sign-off (`REQUIRE_HUMAN_MODEL_APPROVAL=true`).
3. **Drift Alerting**: When feature or prediction drift is detected during scheduled evaluation runs, the system emits an alert rather than automatically retraining or deploying (`ANALYTICS_AUTO_RETRAIN=false`).
