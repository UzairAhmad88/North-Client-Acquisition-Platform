# Inbound Webhooks & Provider Normalization

## 1. Webhook Endpoint Architecture

Inbound events arrive via the public webhook router at `/api/v1/webhooks/{provider}`.

Supported providers include:
- `EMAIL` (SendGrid, Postmark, Resend)
- `WHATSAPP` (Twilio, Meta WhatsApp Cloud API)
- `SMS` (Twilio, Bandwidth)
- `LINKEDIN` (LinkedIn Messaging API)
- `GENERIC` (Custom JSON Webhook Payload)

---

## 2. Inbound Message Normalization (`InboundMessagePayload`)

All raw provider payloads are parsed into the unified `InboundMessagePayload` contract:

```python
class InboundMessagePayload(BaseModel):
    provider: str
    provider_event_id: str
    channel: str  # EMAIL, WHATSAPP, SMS, LINKEDIN
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None
    sender_name: Optional[str] = None
    recipient_address: str
    subject: Optional[str] = None
    body: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    raw_payload: Dict[str, Any] = Field(default_factory=dict)
```

---

## 3. Webhook Delivery Lifecycle

1. **HTTP Handler (`/api/v1/webhooks/{provider}`)**:
   - Verifies provider HMAC signature via `WebhookSecurityGuard`.
   - Checks 5-minute timestamp freshness window.
   - Extracts header/query metadata.
2. **Background Dispatch**:
   - Enqueues background worker task `execute_response_analysis_task(payload_dict)`.
   - Immediately returns HTTP 202 Accepted with idempotency status.
3. **Worker Processing**:
   - Checks idempotency record in `inbound_event_logs`.
   - Resolves CRM entity (`ConversationResolver`).
   - Runs deterministic opt-out check (`DeterministicOptOutDetector`).
   - Executes `ResponseAgent` analysis and persists `ConversationAnalysis`.
   - Evaluates generated draft against `RiskEngine`.
