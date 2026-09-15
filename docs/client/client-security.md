# Client Security & Isolation Architecture

This document describes the security guarantees and data isolation boundaries in **Uzaii Develop By North's Phase 27**.

---

## 1. Security Architecture Principles

1. **Deny-by-Default Visibility Filtering**:
   - Every project resource (thread, message, file, deliverable) defaults to `INTERNAL_ONLY`.
   - Client API queries enforce `is_client_view=True`, filtering out any record without `visibility == CLIENT_VISIBLE`.

2. **Internal Data Protection**:
   - Internal labor costs, developer hourly margins, internal risk logs, and raw AI prompts are **NEVER** exposed to client API responses.

3. **Single-Use Invitation Tokens**:
   - Cryptographically random 256-bit invitation tokens.
   - Stored in database as SHA-256 hashes (`token_hash`).
   - Expire after 48 hours.

4. **Cryptographic Audit Trail**:
   - Deliverable sign-offs compute SHA-256 hashes over payload content.
   - Activity log captures every client view, thread post, file download, and approval event.
