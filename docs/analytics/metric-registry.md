# Centralized Metric Registry & Governance

## 1. Metric Integrity Rule

To eliminate conflicting formulas across dashboards and automated reports, every analytical metric is defined once in the central **Metrics Registry** (`analytics_metrics` table) and versioned through `analytics_metric_versions`.

```text
metric_id
tenant_id
metric_key
name
description
category
formula
source_tables
dimensions
time_window_default
version
owner
status
```

---

## 2. Standard Registered Metrics

| Metric Key | Category | Formula | Dimensions |
| :--- | :--- | :--- | :--- |
| `sales_funnel_conversion_rate` | SALES | `(Won Leads / Total Researched Leads) * 100` | Industry, Service, Channel |
| `pert_estimation_variance_pct` | ESTIMATION | `((Actual Hours - Estimated Hours) / Estimated Hours) * 100` | Service, Project |
| `requirements_change_frequency` | DELIVERY | `Count(Change Requests) / Count(Projects)` | Service, Client |
| `qa_escaped_defect_leakage_rate` | QUALITY | `(Escaped Defects / Total Recorded Defects) * 100` | Service, Release |
| `ai_invocation_cost_efficiency` | AI | `Sum(Actual Token Cost) / Count(Completed Workflows)` | Agent, Service |

---

## 3. Immutability & Lineage

1. Metric versions are strictly additive (`AnalyticsMetricVersion`).
2. Changes to metric formulas require author attribution, reason notes, and incremented version keys (`v1.1`, `v2.0`).
3. Historical snapshots retain the exact metric version used during computation.
