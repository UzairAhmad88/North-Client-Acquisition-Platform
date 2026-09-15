# Personalization Agent Testing & Verification

## Overview
Comprehensive test suites verify that the Personalization Agent adheres to all permissions, security boundaries, qualification gates, claim validation policies, and draft versioning rules.

---

## Test Cases Executed (`tests/unit/backend/test_personalization_agent.py`)

1. **`test_personalization_agent_registration`**: Verifies agent is registered in `AgentRegistry` under `personalization_agent` v1.0 with required permissions (`READ_QUALIFICATION`, `CREATE_OUTREACH_DRAFT`).
2. **`test_prohibited_communication_permissions`**: Verifies prohibited permissions (`SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `SEND_SMS`, `MAKE_PAYMENT`) raise `AgentPermissionDeniedError`.
3. **`test_qualification_gate_not_qualified`**: Verifies `NOT_QUALIFIED` status enforces `outreach_readiness = NOT_RECOMMENDED`.
4. **`test_dnc_guardrail`**: Verifies Do-Not-Contact flag enforces `outreach_readiness = OUTREACH_BLOCKED`.
5. **`test_signal_extraction_and_angle_selection`**: Verifies factually verified signal extraction and primary communication angle selection.
6. **`test_prohibited_claim_detection`**: Verifies hype, revenue guarantees, and false urgency phrases flag `risk_level` as `HIGH`/`BLOCKED`.
7. **`test_draft_versioning_and_approval_reset`**: Verifies editing draft content increments version ($v \rightarrow v+1$) and resets approval to `PENDING_APPROVAL`.
8. **`test_personalization_agent_execution`**: Verifies complete end-to-end async execution of `PersonalizationAgent.run()`.

---

## Verification Commands

```powershell
# Run Personalization Agent unit tests
$env:PYTHONPATH="backend"; python -m pytest tests/unit/backend/test_personalization_agent.py

# Run entire backend test suite
$env:PYTHONPATH="backend"; python -m pytest tests/unit/backend/

# Run frontend TypeScript validation
cd frontend; npx tsc --noEmit
```
