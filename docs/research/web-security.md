# Research System Web Security & SSRF Defense

## Overview

The Research System fetches external public web pages to extract business facts. Because external web requests present severe SSRF (Server-Side Request Forgery) and prompt-injection risks, strict security boundaries are enforced.

---

## SSRF Security Controls (`integrations/web/security.py`)

1. **Protocol / Scheme Restriction**:
   - Only `http://` and `https://` schemes are allowed.
   - `file://`, `ftp://`, `data://`, `gopher://`, `javascript://` schemes are immediately rejected.
2. **DNS & IP Resolution Blocking**:
   - Before connecting to a target domain, DNS resolution resolves all IP addresses.
   - Any IP resolving to a private, loopback, link-local, or cloud metadata network is blocked:
     - `127.0.0.0/8` (IPv4 Loopback)
     - `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` (RFC 1918 Private Networks)
     - `169.254.0.0/16` (Link-Local & Cloud Metadata e.g. `169.254.169.254`)
     - `::1/128`, `fc00::/7`, `fe80::/10` (IPv6 Loopback & Link-Local)
3. **Redirect Target Inspection**:
   - `follow_redirects` is handled manually. Every redirect `Location` header URL is passed through `validate_url_security()` before the next request is initiated.
   - Redirect limit is capped at 3 max.
4. **Resource Caps**:
   - Request timeout: 15 seconds.
   - Response size cap: 5,000,000 bytes (5 MB).

---

## Prompt-Injection Defense

- Text extracted from web pages is strictly treated as untrusted data.
- Web content is passed through HTML stripping, entity unescaping, and string sanitization.
- Web text is stored only as `raw_value`, `normalized_value`, or `evidence_text` attributes and is **never** executed as system instructions or prompt templates.
