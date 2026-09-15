# Emergency Kill Switch & Circuit Breakers

## Overview

The Emergency Kill Switch is an autonomous safety circuit breaker designed to instantly deactivate AI components under emergency conditions (e.g. runaway hallucinations, rogue loops, security exploits, or billing anomalies).

## Multi-Level Circuit Breaker Hierarchy

```text
GLOBAL_AI_OFF
  ├── AGENT_OFF (e.g. discovery_agent, solution_agent)
  ├── MODEL_OFF (e.g. gpt-4o, claude-3-7-sonnet)
  ├── WORKFLOW_OFF (e.g. auto_proposal_generation)
  └── TOOL_OFF (e.g. crm_write_lead, email_dispatcher)
```

## Cutoff Mechanics

1. **In-Memory & Distributed Read-Through**: The `KillSwitchEngine` maintains synchronized state across application workers with low-latency lookups.
2. **Deterministic Fallbacks**: When a component is killed, downstream workflows do not crash; they cleanly drop to deterministic rule-based algorithms or queue for human operators.
3. **Strict Human Authorization**: Only authorized human administrators with `ACTIVATE_GLOBAL_KILL_SWITCH` permissions can trigger or deactivate the switch. AI agents are permanently prohibited from modifying kill switch states (`PROHIBITED_PERMISSIONS`).
4. **Mandatory Audit Logging**: Every activation, deactivation, and target alteration persists an immutable `AIKillSwitchEvent` with operator ID and mandatory justification reason.
