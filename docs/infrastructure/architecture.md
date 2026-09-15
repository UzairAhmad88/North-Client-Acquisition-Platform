# Infrastructure Architecture & Subsystems

The Cloud Operating System integrates 44 modular backend services and 18 specialized AI agents with database persistence across 29 ORM models.

```text
                                 [ Cloud Command Center ]
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
 [ Multi-Cloud Inventory ]         [ Kubernetes Platform ]             [ FinOps Engine ]
 - AWS / GCP / Azure               - Clusters & Node Pools             - Spend Attribution
 - Resource Graph Traversal        - Workload & Pod Health             - Anomaly Detection
 - Blast Radius Simulation         - HPA/VPA Autoscaling               - Savings Tracking
        │                                   │                                   │
        └───────────────────────────────────┼───────────────────────────────────┘
                                            ▼
                          [ Closed-Loop Agent Orchestration ]
                               18 Infrastructure Agents
```
