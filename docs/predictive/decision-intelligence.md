# Decision Intelligence & Human-in-the-Loop Operations

## The Decision Support Paradigm

Decision Intelligence connects raw statistical model outputs to structured human decisions. The platform enforces the principle:
$$\text{AI Recommends} \longrightarrow \text{You Decide}$$

### Decision Support Lifecycle

```text
PREDICTION GENERATED
        ↓
POLICY EVALUATION (Deterministic Rules Check)
        ↓
DECISION SUPPORT RECORD (PENDING_REVIEW)
        ↓
HUMAN OPERATOR REVIEW
  ├── ACCEPT: Implement recommended action
  ├── REJECT: Dismiss recommendation
  └── OVERRIDE: Execute alternate action + log feedback rationale
```

### Deterministic Safety Rules

Deterministic safety rules take precedence over AI predictions in all operational contexts:

| Domain | Rule Code | Condition | Action |
| :--- | :--- | :--- | :--- |
| **QA / Delivery** | `CRITICAL_DEFECT_RELEASE_BLOCK` | Open critical defects $> 0$ | Strictly block release approval |
| **Outreach** | `DNC_REGISTRY_BLOCK` | Contact on Do-Not-Contact list | Strictly block communication |
| **Project Execution** | `UNSIGNED_CONTRACT_BLOCK` | Missing client baseline signature | Block task initialization |

### Structured Human Override Feedback Loop

When an operator chooses `OVERRIDE`, the system requires:
1. `override_reason`: Explanation of domain knowledge, unmodeled external factors, or client-specific context.
2. `chosen_action`: The actual business action taken instead of the AI advice.

These records are preserved in `decision_overrides` for model calibration analysis and future policy refinement.
