# Sharing, Client Boundary & Secure Links

## 1. Client Visibility Boundaries

The document system enforces strict tenant and role scoping:

| Document Scope | Internal Developers / Ops | Client Portal Users |
| :--- | :--- | :--- |
| **`INTERNAL`** | Full Access (subject to RBAC) | **BLOCKED** |
| **`CLIENT_VISIBLE`** | Full Access | View & Authorized Download |
| **`RESTRICTED`** | Admin / Security Only | **BLOCKED** |
| **`SYSTEM`** | System Background Services | **BLOCKED** |

- Files belonging to client projects do **not** automatically become client-visible. Visibility must be explicitly set to `CLIENT_VISIBLE`.
- Field masking automatically strips internal developer notes, gross margins, and cost breakdowns from metadata returned to client users.

---

## 2. Secure Expiring Share Links

Users can generate cryptographically secure share links:

- **High-Entropy Tokens**: 32-byte URL-safe random tokens (`secrets.token_urlsafe(32)`).
- **Time-Bounded Expiration**: 1h, 24h, 7d, 30d, or custom.
- **Granular Permissions**: View only vs View & Download.
- **Immediate Revocation**: Setting `revoked_at` invalidates the link instantaneously across all sessions.
