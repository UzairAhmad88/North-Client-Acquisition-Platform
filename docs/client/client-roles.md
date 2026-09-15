# Client Roles & Access Controls

This document defines the Role-Based Access Control (RBAC) hierarchy for client accounts in **Uzaii Develop By North's**.

---

## 1. Role Hierarchy

```text
       +-----------------------+
       |     CLIENT_ADMIN      |
       +-----------------------+
                   |
       +-----------+-----------+
       |                       |
       v                       v
+---------------+      +---------------+
| CLIENT_MEMBER |      | CLIENT_VIEWER |
+---------------+      +---------------+
```

---

## 2. Role Permissions Table

| Role | Access Level | Can Approve Deliverables? | Can Post Messages? | Can Manage Members? |
| :--- | :--- | :---: | :---: | :---: |
| **CLIENT_ADMIN** | Full Client Organization Control | Yes | Yes | Yes |
| **CLIENT_MEMBER** | Project Workspace Collaborator | Yes (if delegated) | Yes | No |
| **CLIENT_VIEWER** | Read-Only Stakeholder | No | No | No |

---

## 3. Single-Use Invitation Tokens

Client member onboarding uses secure single-use invitation tokens:
- **Hashing**: Tokens are generated using strong cryptographically secure random bytes and stored as SHA-256 hashes (`token_hash`).
- **Expiration**: 48 hours from issuance.
- **Revocation**: Invoking signup consumes the token instantly (`is_used = True`).
