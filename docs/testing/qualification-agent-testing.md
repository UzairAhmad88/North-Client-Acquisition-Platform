# Qualification Agent Testing & Verification

## Overview
Comprehensive test suites verify that the Qualification Agent adheres to all permissions, security boundaries, deterministic guardrails, and human override behaviors.

---

## Test Cases Executed (`tests/unit/backend/test_qualification_agent.py`)

1. **`test_qualification_agent_registration`**: Verifies agent is registered in `AgentRegistry` with correct permissions (`READ_BUSINESS`, `READ_LEAD`, `READ_RESEARCH`, `READ_AUDIT`, `READ_SCORE`, `READ_SERVICES`, `READ_CRM_CONTEXT`, `CREATE_QUALIFICATION_RESULT`).
2. **`test_permission_enforcement`**: Verifies prohibited permissions (`SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT`) raise `PermissionDeniedException`.
3. **`test_dnc_guardrail`**: Verifies Do Not Contact status enforces `outreach_readiness = OUTREACH_BLOCKED`.
4. **`test_duplicate_context_guardrail`**: Verifies unresolved duplicate flag forces decision to `NEEDS_REVIEW`.
5. **`test_insufficient_data_handling`**: Verifies sparse inputs result in `INSUFFICIENT_DATA`.
6. **`test_score_non_alteration`**: Verifies lead opportunity scores and recommendation rankings are preserved without modification.
7. **`test_untrusted_data_isolation`**: Verifies external web research excerpts are wrapped in `<UNTRUSTED_EXTERNAL_DATA>` tags.
8. **`test_qualification_confidence_calculator`**: Verifies confidence score calculation based on data completeness and freshness.
9. **`test_qualification_engine_evaluation`**: Verifies hybrid engine decision output structure.
10. **`test_human_override_flow`**: Verifies human override records justification, timestamp, user ID, and updates active decision.

---

## Running Verification Commands

```powershell
# Run qualification agent unit tests
$env:PYTHONPATH="backend"; python -m pytest tests/unit/backend/test_qualification_agent.py

# Run entire backend test suite
$env:PYTHONPATH="backend"; python -m pytest tests/unit/backend/

# Run frontend TypeScript validation
cd frontend; npx tsc --noEmit
```
