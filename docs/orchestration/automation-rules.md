# Automation Rules Engine

## Overview

The Automation Rules Engine enables declarative cross-system triggers linking domain events to automated workflows.

```text
WHEN [Event Trigger]
IF   [Condition Rules]
THEN [Allowed Action / Launch Workflow]
```

## Security Guardrails: No Autonomous Communication

- **Rule**: Triggering an automation rule does **not** grant authorization to bypass human approval or communication safety guards.
- **Action Restriction**: Automation rules can create drafts or launch workflows, but external communication actions must still pass through `RiskEngine`, `HumanApproval`, and `CommunicationGuard`.
- **Audit Logging**: Every automation rule execution creates an immutable `AutomationRuleRun` record logging the triggering event ID, execution status, and outcome summary.
