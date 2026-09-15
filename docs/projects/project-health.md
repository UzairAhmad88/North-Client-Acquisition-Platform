# Deterministic Project Health Engine

## Overview
Project health in **Uzaii Develop By North's** is computed using a transparent, rules-based engine. AI agents may generate executive explanations, but cannot override deterministic health classifications.

---

## Health Classification Matrix

| Health Status | Trigger Conditions | Action Required |
|---|---|---|
| `HEALTHY` | All tasks, milestones, and client dependencies are on schedule; 0 severe blockers. | Normal execution. |
| `AT_RISK` | $\ge 2$ overdue tasks, $\ge 1$ blocked task, or effort variance $> 20.0$ hours. | PM review & task re-allocation. |
| `CRITICAL` | $\ge 3$ blocked tasks, $\ge 1$ missed milestone, or $\ge 2$ overdue client dependencies. | Urgent escalation & client alert. |
| `BLOCKED` | Project explicitly placed `ON_HOLD`. | Unblock dependency or resolve dispute. |
| `COMPLETED` | All tasks and deliverables completed ($100\%$). | Final sign-off. |

---

## Deterministic Rules Logic

```python
if blocked_task_count >= 3 or missed_milestone_count >= 1 or overdue_client_deps >= 2:
    health = "CRITICAL"
elif overdue_task_count >= 2 or blocked_task_count >= 1 or effort_variance > 20.0:
    health = "AT_RISK"
```
