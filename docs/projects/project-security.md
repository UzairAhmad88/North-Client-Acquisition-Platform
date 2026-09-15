# Project Execution Security & Client Visibility Controls

## Overview
The Project Execution System enforces strict RBAC, data protection, and prompt injection defense boundaries.

---

## Prohibited Agent Permissions
`ProjectAgent` is restricted from taking autonomous legal, commercial, or external action. The following permissions are **strictly prohibited** in `agents/core/permissions.py`:

```python
PROHIBITED_PERMISSIONS = {
    "MODIFY_BASELINE",
    "CHANGE_CONTRACT",
    "CHANGE_PRICE",
    "APPROVE_SCOPE",
    "APPROVE_CHANGE",
    "SEND_EXTERNAL_MESSAGE",
    "PROMISE_DEADLINE",
    "DELETE_PROJECT",
    "DELETE_AUDIT_LOG",
}
```

---

## Client Visibility Boundary (`PROJECT_CLIENT_INTERNAL_DATA_PROTECTION=true`)

> [!CAUTION]
> **Internal Data Isolation**
> Client viewing portal access is strictly gated. The following internal operational attributes are **NEVER** exposed to client users:
> 1. Internal hourly rates and labor cost margins.
> 2. Private developer/operator team notes.
> 3. Raw AI reasoning and internal prompt traces.
> 4. Internal risk assessments and commercial strategy logs.
