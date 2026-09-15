# CommunicationGuard Validation Pipeline

## Pipeline Steps (Executed in Strict Sequence)

1. **Authentication Check**: Verifies sender identity and session validity.
2. **Authorization Check**: Ensures user has permission to trigger outreach actions.
3. **Outreach Object Existence**: Validates that outreach ID exists in DB.
4. **Draft Status Verification**: Ensures outreach status is `APPROVED` (or eligible state).
5. **Recipient Email Validity**: Validates email format, domain format, and syntax.
6. **Human Approval Verification**: Asserts that `is_human_approved` is `True` and `approved_at` is present.
7. **Content Hash Consistency**: Re-computes SHA-256 hash of subject, body, and recipient, comparing it against `approved_content_hash`.
8. **Do Not Contact (DNC) Registry Check**: Checks email, domain, and business against `do_not_contact` table.
9. **Duplicate Detection**: Queries `outreach_events` for identical recipient/subject within 7 days.
10. **Frequency Cap Enforcement**: Ensures daily send limit for the business is not exceeded.
11. **Channel Cooldown Verification**: Checks minimum required gap between messages for the business.
12. **Policy Compliance**: Evaluates active `communication_policies` for business/channel restrictions.
13. **Risk Level Assessment**: Validates risk rating before dispatching.
14. **Idempotency Lock**: Acquires atomic lock on `outreach:{id}:send:{version}`.
15. **Provider Readiness Check**: Verifies active provider status.

## Failure Handling
If any step fails, `CommunicationGuard` aborts the pipeline, records an `OUTREACH_SEND_FAILED` event with details of the failing check, and sets outreach status to `FAILED_VALIDATION`.
