# Security Boundaries & Compliance Controls

## 1. Zero Autonomous Sending Policy

The **Response & Conversation Intelligence System** enforces strict boundary controls to guarantee AI cannot send outbound messages autonomously:

1. **Permission Denials**: `ResponseAgent` holds read permissions (`READ_BUSINESS`, `READ_LEAD`, `READ_CONVERSATION`, etc.) and `CREATE_DRAFT`. It is explicitly forbidden from holding `SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, or `SEND_SMS`.
2. **Phase 19 `CommunicationGuard` Verification**: Any attempt to dispatch an outbound email or message checks that:
   - Recipient is NOT in `DoNotContact` registry.
   - Outbound status is explicitly set to `APPROVED` by a human operator.
   - Risk assessment passes configured thresholds.

---

## 2. Webhook Security Guard (`WebhookSecurityGuard`)

### HMAC Signature Verification
All incoming webhooks are validated using HMAC-SHA256 signatures matching the configured provider secret (`WEBHOOK_SECRET` environment variable).

### Timestamp Replay Protection
Webhooks with timestamp headers (`X-Webhook-Timestamp`) exceeding 300 seconds (5 minutes) skew from server time are rejected with `HTTP 401 Unauthorized`.

### Idempotency & Deduplication
Every inbound message payload is indexed by `(provider, provider_event_id)` in `inbound_event_logs`. Duplicate webhooks return `HTTP 200 OK` with status `DUPLICATE_IGNORED` without executing duplicate processing or AI runs.

---

## 3. Opt-Out Registry & Enforcement

When `DeterministicOptOutDetector` matches an opt-out phrase:
1. Target email or phone is immediately saved in the `do_not_contact` database table.
2. Active conversation stage is updated to `OPTED_OUT`.
3. AI analysis skips draft generation and sets recommended action to `DO_NOT_CONTACT`.
