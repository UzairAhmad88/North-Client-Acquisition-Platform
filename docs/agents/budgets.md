# Agent Budget Controls & Cost Limits

## Default Execution Bounds

| Resource | Default Limit | Exception Triggered |
|---|---|---|
| Max Steps | 10 steps | `AgentBudgetExceededError` |
| Max Tool Calls | 8 tool calls | `AgentBudgetExceededError` |
| Max Runtime | 60 seconds | `AgentBudgetExceededError` |
| Max Tokens | 8,000 tokens | `AgentBudgetExceededError` |

---

## Budget Enforcement Pipeline

Budget limits are evaluated:
1. **Before Node Execution**: Increments step counter.
2. **Before Tool Execution**: Increments tool call counter.
3. **During AI Completion**: Increments token counter and calculates estimated cost.

Exceeding any bound immediately halts execution and transitions status to `FAILED` with `error_message = "Budget exceeded"`. Retries are prohibited on budget exhaustion.
