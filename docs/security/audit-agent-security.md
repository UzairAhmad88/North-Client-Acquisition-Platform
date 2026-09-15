# Phase 16 — Audit Agent Security Controls

## 1. Security Architecture Summary

The Audit Agent enforces five core security guarantees:

1. **Read-Only Boundary (Passive Assessment)**: Performs GET requests only. Never submits forms, logs in, creates bookings, or alters external web resources.
2. **Zero Autonomous Outbound Communication**: Prohibits `SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT`, `MODIFY_EXTERNAL_RESOURCE`, `DELETE_DATA`.
3. **SSRF Protection**: Resolves IP addresses using `validate_url_security` to block loopback (`127.0.0.1`), private networks (`10.0.0.0/8`, `192.168.0.0/16`), link-local metadata endpoints (`169.254.169.254`), and internal hostnames (`metadata.google.internal`).
4. **Prompt Injection Defense**: Sanitizes fetched web page content inside `<UNTRUSTED_EXTERNAL_DATA>` tags to prevent untrusted web text from altering agent instructions.
5. **Crawl Limits**: Enforces `MAX_AUDIT_PAGES=10`, `MAX_RESPONSE_BYTES=1048576`, and `MAX_REDIRECTS=5` to prevent infinite loops or resource exhaustion.

---

## 2. Terminology & Security Language Policy

The Audit Agent reports observable facts only:
- **Allowed**: `"Header was not observed"`, `"HTTPS was available"`, `"Basic security configuration signal is missing"`.
- **Forbidden**: `"The website is hacked"`, `"The website is vulnerable to attack"`, `"Vulnerability exploited"`.

The audit is a passive digital presence assessment, not a penetration test.
