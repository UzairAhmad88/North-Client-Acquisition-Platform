# Outreach System Testing Specification

## Unit Testing Suite

The unit test suite for the Outreach System is located at `tests/unit/backend/test_outreach_system.py`.

### Test Coverage

1. **Content Hash Verification (`test_approval_hash_verification`)**:
   - Validates that modifying draft body or subject fails `verify_approval` check.
2. **DNC Enforcement (`test_dnc_guard_check`)**:
   - Ensures recipients registered on the DNC list are blocked by `CommunicationGuard`.
3. **Daily Cap Enforcement (`test_frequency_controller_daily_cap`)**:
   - Verifies that exceeding business daily limit prevents message dispatch.
4. **Duplicate Detection (`test_duplicate_detection`)**:
   - Verifies that sending duplicate subject/recipient within 7 days is caught and blocked.
5. **Idempotency Lock (`test_idempotency_lock`)**:
   - Ensures concurrent or duplicate send requests for the same draft version are rejected.
6. **Mock Provider Dispatch (`test_mock_provider_send`)**:
   - Validates end-to-end send flow using `MockEmailProvider` with audit event emission.

## Running Tests

```bash
$env:PYTHONPATH="backend"
python -m pytest tests/unit/backend/test_outreach_system.py
```
