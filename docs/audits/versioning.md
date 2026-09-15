# Audit Versioning & History

## Audit Versioning

All audits are versioned with `audit_version` (default `"1.0"`).
Historical audit snapshots are never mutated or destroyed. Subsequent audit runs generate new records with updated timestamps, preserving an auditable timeline of digital presence changes over time.

## Historical Snapshot Example

```text
Audit #1 — September 8
Version: 1.0
Status: AVAILABLE
Health: NEEDS_ATTENTION
Findings: Missing contact form

Audit #2 — October 10
Version: 1.0
Status: AVAILABLE
Health: HEALTHY
Findings: Contact form detected
```
