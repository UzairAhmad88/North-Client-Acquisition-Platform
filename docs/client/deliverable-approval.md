# Cryptographic Deliverable Sign-Off & Approval Workflow

This document outlines the deliverable review and sign-off protocol for **Uzaii Develop By North's Phase 27**.

---

## 1. Non-Approval Disclaimer Policy

> **CRITICAL LEGAL SAFEGUARD**:
> Viewing, opening, or downloading a deliverable version does **NOT** equal approval or baseline commitment. Formal approval requires explicit submission via the client sign-off form.

---

## 2. SHA-256 Fingerprinting Protocol

When a client submits an approval:
1. The server extracts the exact payload of the deliverable version (`content_payload`).
2. Calculates the canonical SHA-256 fingerprint:
   $$\text{content\_hash} = \text{SHA256}(\text{content\_payload})$$
3. Records an immutable audit log entry in `deliverable_approvals` containing:
   - `deliverable_id` & `version_number`
   - `content_hash`
   - `approval_statement`
   - `signer_name` & `signer_email`
   - `approved_at` timestamp (UTC)

---

## 3. Auditable Sign-Off Schema

```json
{
  "id": "appr-8821",
  "deliverable_id": "del-001",
  "version_number": 1,
  "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "approval_statement": "I explicitly confirm and approve this deliverable version.",
  "signer_name": "John Doe",
  "signer_email": "john@acme.com",
  "approved_at": "2026-09-08T21:40:00Z"
}
```
