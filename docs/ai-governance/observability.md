# AI Observability & Performance Monitoring

## Overview

The AI Observability subsystem continuously tracks operational health, throughput, latency percentiles, error rates, and human revision acceptance across all AI agents and predictive models in production.

## Key Performance Indicators (KPIs)

| Metric | Target SLA | Critical Breach Threshold | Telemetry Source |
| :--- | :--- | :--- | :--- |
| **P95 Latency** | < 3,500 ms | > 8,000 ms | `AITrace.total_duration_ms` |
| **Execution Success Rate** | > 98.5% | < 90.0% | `AITrace.status == COMPLETED` |
| **Human Acceptance Rate** | > 85.0% | < 70.0% | `HumanRevisionRecord.edit_magnitude` |
| **Token Budget Utilization** | < 80.0% of limit | >= 100.0% | `AIBudgetPolicy` / `ModelUsageRecord` |
| **Schema Validation Pass Rate** | 100.0% | < 99.0% | `AITraceEvent` (span_type=VALIDATION) |
| **Hallucination / Evidence Score** | >= 4.0 / 5.0 | < 3.0 / 5.0 | `HumanEvaluation` & Automated Graders |

## Health Snapshots & Auto-Degradation

The `AIHealthSnapshot` engine aggregates metrics hourly per agent:
- `HEALTHY`: Success rate >= 95%, P95 < 5s, Human acceptance >= 80%.
- `WARNING`: Success rate 90-95%, P95 5s-8s, or Daily cost > 80% quota.
- `DEGRADED`: Success rate 80-90% or Human rejection > 30%. Alerts operator channel.
- `FAILED`: Success rate < 80% or continuous schema validation failures. Triggers auto-isolation.
- `DISABLED`: Manually deactivated via Kill Switch.
