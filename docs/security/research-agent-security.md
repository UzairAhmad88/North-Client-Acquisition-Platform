# Phase 15 — Research Agent Security Controls

## 1. Security Architecture Summary

The Research Agent enforces three key defense mechanisms:

1. **Prompt Injection Protection**: Sanitizes external web contents inside `<UNTRUSTED_EXTERNAL_DATA>` XML block tags.
2. **SSRF Protection**: Resolves IP addresses using `validate_url_security` to block loopback (`127.0.0.1`), private networks (`10.0.0.0/8`, `192.168.0.0/16`), link-local metadata endpoints (`169.254.169.254`), and internal hostnames (`metadata.google.internal`).
3. **Zero Autonomous Outbound Communication**: Prohibits permissions `SEND_EMAIL`, `SEND_MESSAGE`, `SEND_WHATSAPP`, `MAKE_PAYMENT`.

---

## 2. SSRF Protection Details

All URLs supplied to `FetchWebTool` are validated against `integrations.web.security.validate_url_security`:
- Scheme restriction: Only `http` and `https`.
- Hostname blacklist: `localhost`, `loopback`, `metadata.google.internal`.
- IP address resolution check against `FORBIDDEN_NETWORKS`.

---

## 3. Untrusted Data Isolation

External HTML or plain text content fetched via web tools is sanitized using `AgentValidator.sanitize_untrusted_input`:

```html
<UNTRUSTED_EXTERNAL_DATA>
Fetched page text...
</UNTRUSTED_EXTERNAL_DATA>
```

This prevents external malicious web pages from hijacking the agent prompt instructions or injecting instructions to alter execution flow.
