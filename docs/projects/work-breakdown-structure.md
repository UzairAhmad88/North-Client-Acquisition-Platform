# Work Breakdown Structure (WBS) & Task Management

## Overview
The Work Breakdown Structure (WBS) decomposes committed baseline deliverables into manageable engineering tasks, subtasks, dependencies, and delivery milestone targets.

---

## WBS Hierarchy & Data Flow

```text
ContractBaseline Deliverables
        ↓
Project Deliverables & Acceptance Criteria
        ↓
WBS Tasks (Parent Tasks)
        ↓
Subtasks (Granular Work Items)
```

---

## Task Model & Status Rules

### Task Statuses
- `TODO`: Initial state ($0\%$ progress).
- `READY`: Dependencies clear, ready for assignment.
- `IN_PROGRESS`: Active work ($1-99\%$ progress).
- `BLOCKED`: Work blocked by predecessor task or external issue.
- `IN_REVIEW`: Code review or QA verification.
- `COMPLETED`: Work verified ($100\%$ progress).

### Task Dependency & Graph Validation
- Supported dependency type: `FINISH_TO_START`.
- Circular dependency prevention: `check_circular_dependency` BFS algorithm rejects graphs containing cycles ($A \rightarrow B \rightarrow C \rightarrow A$).

### Subtask Progress Rollup
Parent task progress is calculated deterministically as the average progress of its child subtasks:
$$\text{Parent Progress} = \frac{\sum \text{Subtask Progress}_i}{N}$$
