# Requirements Intelligence Testing Guide

## 1. Test Suite Location

The dedicated unit and integration test suite for Phase 22 is located in:
`tests/unit/backend/test_requirements_intelligence.py`

---

## 2. Running the Test Suite

Run the Phase 22 test suite:

```bash
cmd /c "set PYTHONPATH=backend;. && python -m pytest tests/unit/backend/test_requirements_intelligence.py"
```

Run the entire backend test suite (all 22 phases):

```bash
cmd /c "set PYTHONPATH=backend;. && python -m pytest tests/unit/backend/"
```

---

## 3. Test Coverage Summary

| Test Case | Description | Primary Verification |
| :--- | :--- | :--- |
| `test_requirements_agent_permissions` | Asserts `RequirementsAgent` lacks external send or contract permissions. | `SEND_EMAIL`, `SEND_MESSAGE`, `SIGN_CONTRACT` not present. |
| `test_explicit_vs_inferred_requirements` | Validates client explicit requests (`explicit=True`) vs AI inferences (`explicit=False`). | Assert `explicit` and `source_type` attributes. |
| `test_contradiction_detection` | Tests contradiction detection engine identifying access control conflicts. | Assert contradiction length > 0 and correct title matching. |
| `test_discovery_questions_generator` | Tests prioritized discovery question generator. | Assert question count <= 4 and category matching. |
| `test_scope_expansion_detection` | Tests scope expansion detection on new high-complexity features. | Assert `scope_expansion_detected is True`. |
| `test_readiness_evaluation` | Tests readiness stage, readiness score, completeness score, and complexity. | Assert `completeness_score > 0.0` and complexity tier. |
| `test_full_discovery_session_workflow` | End-to-end integration test creating session, running analysis, confirming requirement, and answering question. | Assert session status transitions and requirement/question confirmations. |
