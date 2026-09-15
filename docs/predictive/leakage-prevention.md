# Point-in-Time Data Leakage Defense

## The Risk of Data Leakage

Data leakage occurs when information from after the point of prediction (post-hoc outcomes, final invoices, completed milestone logs) contaminates the training dataset or live feature extraction. This creates falsely optimistic model metrics during validation that fail catastrophically in production.

## Leakage Defense Architecture

The platform enforces a three-tier leakage defense mechanism:

### 1. Temporal Cutoff Constraint
Every feature query is strictly parameterized with an authoritative point-in-time timestamp ($T_{\text{inference}}$ or $T_{\text{as\_of}}$):
$$\forall f \in \text{Features}, \quad \text{Timestamp}(f) \le T_{\text{inference}}$$

### 2. Prohibited Post-Event Variable Filtering
The feature store engine maintains a denylist of outcome variables that cannot be included in predictive feature sets:
- `final_invoice_amount`
- `client_signature_timestamp`
- `actual_completion_date`
- `post_delivery_defect_count`
- `realized_margin`
- `churn_confirmed_date`
- `settled_contract_value`

### 3. Immutable Snapshot Checksums
When a prediction is generated, the feature vector is frozen into a JSON snapshot, hashed with SHA-256, and saved alongside the prediction record.
