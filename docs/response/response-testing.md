# Response & Conversation Intelligence Testing Guide

## 1. Test Suite Location

The unit and integration tests for Phase 21 are located in:
`tests/unit/backend/test_response_intelligence.py`

---

## 2. Running the Test Suite

Run the dedicated Phase 21 test suite:

```bash
cmd /c "set PYTHONPATH=backend;. && python -m pytest tests/unit/backend/test_response_intelligence.py"
```

Run the entire backend test suite:

```bash
cmd /c "set PYTHONPATH=backend;. && python -m pytest tests/unit/backend/"
```

---

## 3. Test Coverage Summary

| Test Case | Description | Primary Verification |
| :--- | :--- | :--- |
| `test_response_agent_permissions` | Asserts `ResponseAgent` lacks external send permissions. | `SEND_EMAIL`, `SEND_MESSAGE` not present in agent permissions. |
| `test_intent_classification` | Validates keyword pattern matching for pricing, meeting, and interest intents. | Assert primary intent matches expectations. |
| `test_buying_signals_and_objections` | Tests commercial readiness signals and objection detection. | Assert buying signal level (`STRONG`) and objection type (`PRICE`). |
| `test_requirement_extraction` | Tests scope extraction and missing detail identification. | Assert `WEBSITE` and `BOOKING` extracted; `Budget Range` missing. |
| `test_deterministic_opt_out_and_dnc_trigger` | Tests opt-out detection and instant `DoNotContact` insertion. | Assert `dnc.is_active is True`. |
| `test_full_inbound_response_processing` | End-to-end flow from inbound payload to resolution, analysis, draft generation, and human correction. | Assert `INBOUND` message creation, intent detection, analysis, and human correction recording. |
