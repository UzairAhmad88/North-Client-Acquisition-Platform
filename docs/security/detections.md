# Detection Rules Engine

## 1. Detection Rule Paradigms
- **Threshold Rules**: High volume of failed logins or mass file access within a sliding window.
- **Sequence Rules**: Step 1 (Failed Login) $\rightarrow$ Step 2 (Successful Login) $\rightarrow$ Step 3 (Privilege Elevation) $\rightarrow$ Step 4 (Data Export).
- **Behavioral & Anomaly Rules**: Statistical deviation from entity baseline.
- **Machine Learning & Graph Rules**: Abnormal link traversal in security topology.
