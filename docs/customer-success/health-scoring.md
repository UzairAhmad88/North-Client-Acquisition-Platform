# Multi-Factor Client Health Scoring Engine

## 1. Mathematical Formulation & Weighting

The `HealthScoringEngine` computes a deterministic composite score between `0.00` and `100.00` using configurable dimension weights:

| Dimension | Default Weight | Data Sources |
|---|---|---|
| **Engagement** | 15% | Interaction frequency, meeting attendance, response recency |
| **Project Health** | 20% | Milestone completions, blocked tasks, deliverable acceptance |
| **Support Health** | 10% | Ticket resolution SLAs, escalation frequency, backlog age |
| **Financial Operations** | 15% | Payment punctuality, overdue invoices, dispute rates |
| **Satisfaction** | 20% | CSAT survey averages, NPS rating, communication sentiment |
| **Relationship** | 10% | Sponsor stability, decision-maker presence, multi-threading |
| **Goal Progress** | 10% | Strategic objective completion percentage |

## 2. Missing Factor Re-Normalization

When telemetry is missing for certain factors, the engine automatically re-normalizes the weights across available dimensions:

$$NormalizedWeight_i = \frac{Weight_i}{\sum_{j \in Valid} Weight_j}$$

$$CompositeScore = \sum_{i \in Valid} (Score_i \times NormalizedWeight_i)$$

## 3. Insufficient Data Protection

If fewer than 2 active factors have recorded data, the engine assigns `HealthBand.INSUFFICIENT_DATA` with `confidence = "LOW"`, preventing premature or misleading health labels.

## 4. Trend Velocity Evaluation

The engine compares recent historical snapshots:
* $\Delta > +2.00$ points/period $\rightarrow$ **`IMPROVING`**
* $\Delta < -2.00$ points/period $\rightarrow$ **`DECLINING`**
* Else $\rightarrow$ **`STABLE`**
