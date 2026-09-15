# AI Cost & Token Monitoring

## Overview

The AI Cost & Token Monitoring subsystem tracks, calculates, and enforces financial constraints across all LLM inference operations in real time.

## Pricing Models & Token Rates

Pricing is computed per model family using standard unit economics (per 1,000 tokens):

| Model Name | Prompt Rate ($/1k) | Completion Rate ($/1k) | Latency SLA (P95) |
| :--- | :--- | :--- | :--- |
| `gpt-4o` | $0.005 | $0.015 | < 3,000 ms |
| `gpt-4o-mini` | $0.00015 | $0.0006 | < 1,500 ms |
| `claude-3-7-sonnet` | $0.003 | $0.015 | < 3,500 ms |
| `claude-3-5-haiku` | $0.0008 | $0.004 | < 1,200 ms |
| `gemini-1.5-pro` | $0.0035 | $0.0105 | < 3,200 ms |

## Enforcement Policies & Actions

The `AIBudgetMonitor` evaluates per-day and per-month spending against `AIBudgetPolicy` thresholds:

1. **`BLOCK`**: When daily or monthly limit is breached, incoming AI requests are immediately aborted with an `AIBudgetExceededError`.
2. **`FALLBACK`**: Automatically reroutes expensive flagship model requests (e.g. `claude-3-7-sonnet`, `gpt-4o`) to lightweight, cost-effective models (e.g. `gpt-4o-mini`, `claude-3-5-haiku`).
3. **`REQUIRE_REVIEW`**: Routes the workflow to a human approval queue prior to making the model call.

## Multitenant Isolation & Granular Quotas

Budget policies can be assigned at three distinct scopes:
- **`GLOBAL`**: Platform-wide spending safeguards.
- **`AGENT`**: Per-agent allocations (e.g. max $20.00/day for Discovery Agent).
- **`WORKFLOW`**: Per-workflow or per-tenant allocations.
