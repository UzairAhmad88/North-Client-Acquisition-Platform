# Agent Runtime Testing Strategy

## Test Coverage Summary

- **Backend Agent Core Suite**: `tests/unit/backend/test_agent_core.py`
  - Agent registration & metadata validation.
  - Prohibited permission deny-by-default (`SEND_EMAIL` exception trigger).
  - Tool sandbox execution & input/output schema validation.
  - Prompt-injection defense sanitization (`<UNTRUSTED_EXTERNAL_DATA>` wrapper & injection text replacement).
  - Budget control limits (step limit & tool call limit triggers).
  - State transition graph validation.
  - Workflow graph execution & human approval boundary (`WAITING_FOR_APPROVAL`).
  - AIRouter & `MockAIProvider` completion execution.
  - REST API endpoint authorization & list/cancel endpoints.

## Verification Commands

```bash
# Backend pytest suite
python -m pytest

# Backend mypy static type checking
python -m mypy app
```
