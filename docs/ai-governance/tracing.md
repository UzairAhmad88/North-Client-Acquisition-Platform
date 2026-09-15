# Distributed AI Tracing & Zero CoT Policy

## Architecture & Lifecycle

Every AI invocation initializes a distributed `AITrace` span hierarchy. A trace links workflows, projects, leads, agent versions, prompt versions, and model versions.

```text
AITrace [trace_id, tenant_id, workflow_id, agent_key, version]
  ├── AITraceEvent [span_type: AGENT_START]
  ├── AITraceEvent [span_type: TOOL_CALL, tool_name: crm_search]
  ├── AITraceEvent [span_type: MODEL_CALL, provider: anthropic/claude-3-7-sonnet]
  ├── AITraceEvent [span_type: RISK_CHECK, policy: prompt_injection_defense]
  ├── AITraceEvent [span_type: VALIDATION, schema: ProposalPayloadSchema]
  └── AITraceEvent [span_type: AGENT_COMPLETE]
```

## Zero Private Chain-of-Thought (CoT) Storage

### Policy Statement
Deep internal reasoning, hidden scratchpads, and unscrubbed model monologues represent intellectual property and privacy exposure vectors, and must never be persisted to disks or queryable tables.

### Sanitization Implementation
`AITracerEngine.sanitize_event_payload()` scrubs the following keys recursively from all trace metadata:
- `thought`
- `reasoning`
- `chain_of_thought`
- `internal_monologue`
- `hidden_scratchpad`

### Retained Observability Metadata
Traces retain rich, verifiable telemetry:
1. Sanitized structured inputs and final outputs
2. Prompt token counts, completion tokens, and dollar cost
3. Tool arguments, returned schemas, and execution latency
4. Policy violation checks, validation errors, and retry attempts
5. Human evaluation ratings and revision Levenshtein distances
