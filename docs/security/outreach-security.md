# Outreach Security Controls

## Security Model

1. **Zero AI Agent Send Privileges**:
   - AI agents (Phase 18 Personalization Agent and others) produce outreach drafts with `approval_status="PENDING_APPROVAL"` and `is_human_approved=False`.
   - AI agents are denied access to external email/communication transport interfaces.

2. **Immutable Content Hash Binding**:
   - Human approval calculates `SHA-256("sub:<subject>|body:<body>|recip:<email>")`.
   - If an API request or user edits subject, body, or recipient after approval, `content_hash` is invalidated ($v \rightarrow v+1$, status resets to `PENDING_APPROVAL`, `is_human_approved=False`).

3. **15-Step Gatekeeping Guard**:
   - Re-runs content hash, DNC, policy, and cap checks at the exact millisecond of send dispatch to prevent race conditions or stale approvals.

4. **Safety Default**:
   - Transport defaults to `MockEmailProvider` (`REAL_SEND=false`).
   - Production send requires explicit environment toggle `REAL_SEND=true` and authenticated human administrator dispatch.
