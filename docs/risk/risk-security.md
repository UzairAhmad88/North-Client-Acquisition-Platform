# Risk Engine Security Controls

## Security Model

1. **Zero Provider Access Boundary**:
   - The Risk Engine evaluates artifacts in memory; it has zero transport provider dependencies and cannot send email, WhatsApp, or SMS messages.

2. **Deterministic Priority Over AI**:
   - Deterministic rules (claims, evidence, PII, recipient match, channel format, prompt injection) evaluate before and strictly override AI semantic assessments. An AI semantic review cannot override a deterministic `BLOCK`.

3. **Prompt Injection Defense**:
   - External web data or business descriptions embedded in drafts are wrapped in `<UNTRUSTED_EXTERNAL_DATA>` tags. Any instruction override attempts in external data trigger `CRITICAL` finding `R-SECURITY-PROMPT-INJECTION`.

4. **Staleness Invalidation**:
   - Updating draft body, subject, or recipient recalculates the SHA-256 content hash and marks prior assessments as `is_stale=True`.

5. **Auditable Human Overrides**:
   - Human reviewers can record override decisions (`ACCEPTED` / `REJECTED`) with required text rationale. Override actions preserve original evaluation records in full for auditability.
