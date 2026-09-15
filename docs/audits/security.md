# Audit Security & SSRF Protection Policy

## Read-Only Guarantee

The Audit Engine operates under strict read-only guarantees:
- Never submits forms or posts payload data.
- Never clicks booking or payment links.
- Never sends email, WhatsApp, or SMS messages.
- Never attempts login or authentication bypass.

## SSRF Boundaries

All target URLs and redirects pass through `validate_url_security()` (`integrations/web/security.py`):
- Only `http` and `https` schemes allowed.
- Resolves DNS and blocks forbidden IP ranges:
  - `127.0.0.0/8` (Loopback)
  - `10.0.0.0/8` (Private Class A)
  - `172.16.0.0/12` (Private Class B)
  - `192.168.0.0/16` (Private Class C)
  - `169.254.0.0/16` & `169.254.169.254` (Link-local & AWS/GCP Metadata)
- Hostname blacklist: `localhost`, `loopback`, `metadata.google.internal`.

## Prompt-Injection Defense

Audited HTML pages are treated as untrusted text inputs. Extracted snippets and strings are sanitized and never evaluated as code or system instructions.
