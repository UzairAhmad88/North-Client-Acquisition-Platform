# Security Audit Logging & Compliance Assurance

## 1. Immutable Audit Trail

Every security-sensitive operation (authentication attempts, authorization grants, permission rejections, session revocations, and cross-tenant access attempts) is immutably recorded in the `security_events` table:

```sql
CREATE TABLE security_events (
    id VARCHAR(36) PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    principal_id VARCHAR(100) NOT NULL,
    principal_type VARCHAR(50) NOT NULL,
    tenant_id VARCHAR(100) NOT NULL,
    action VARCHAR(150),
    resource VARCHAR(100),
    resource_id VARCHAR(100),
    result VARCHAR(50) NOT NULL,  -- ALLOW, DENY, BLOCK
    reason_code VARCHAR(100) NOT NULL,
    details JSON NOT NULL,
    ip_address VARCHAR(100),
    user_agent VARCHAR(500),
    request_id VARCHAR(100),
    occurred_at TIMESTAMP WITH TIME ZONE NOT NULL
);
```

---

## 2. Event Severity Ratings

- `INFO`: Normal logins, token refreshes, authorized role readings.
- `LOW`: Routine permission evaluations.
- `MEDIUM`: Failed logins, session revocations, step-up authentication challenges.
- `HIGH`: Account suspensions, API key revocations, unauthorized administrative actions.
- `CRITICAL`: Cross-tenant access attempts, prohibited AI agent execution attempts, break-glass activations.

---

## 3. Compliance Guarantee

- **Append-Only**: Security records cannot be updated or deleted by normal users or administrators.
- **Traceability**: Every security event links directly to the `request_id`, client IP address, and evaluated policy version.
