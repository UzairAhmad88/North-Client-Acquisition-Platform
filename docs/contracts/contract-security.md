# Contract System Security, Governance & Compliance

## Overview
The Contract & Scope Commitment System handles highly sensitive commercial and legal operations. Strict security boundaries and permission controls govern all components.

---

## Permission Matrices

### Prohibited Permissions for AI Agents (`ContractAgent`)
`ContractAgent` is strictly restricted from executing autonomous legal actions. The following permissions are **explicitly prohibited** in `agents/core/permissions.py`:

```python
PROHIBITED_AGENT_PERMISSIONS = {
    "SEND_EMAIL",
    "SEND_MESSAGE",
    "APPROVE_CONTRACT",
    "ACCEPT_CONTRACT",
    "SIGN_CONTRACT",
    "SEND_CONTRACT",
    "EXECUTE_CONTRACT",
    "MODIFY_PRICING",
}
```

### Human Operator Permissions
Only authenticated operators with RBAC roles (e.g. `admin`, `legal_operator`, `project_manager`) are granted permission to:
* `APPROVE_CONTRACT`: Provide internal clearance after Risk Engine evaluation.
* `SEND_CONTRACT`: Share contract access links with clients.
* `EXECUTE_CONTRACT`: Manually trigger signature process or baseline lock.

---

## Non-Legal Advice Disclaimer & System Scope Boundary

> [!CAUTION]
> **Legal Disclaimer**
> The Contract System in **Uzaii Develop By North's** is a software platform designed to manage structured business specifications, scope commitments, document drafting, versioning, and client assent workflows.
> 
> The system does **not** provide legal advice, representation, or guarantee legal enforceability in any specific jurisdiction. All generated contract templates and sections must be reviewed by qualified legal counsel prior to formal execution.

---

## Anti-Tamper Verification & Hashing
1. **Canonical JSON Section Serialization**: Document sections are ordered canonically by `section_order` and serialized to JSON.
2. **SHA-256 Checksum**: Calculated across canonical section JSON and stored on `ContractVersion.content_hash`.
3. **Audit Trail**: Every state transition (creation, edit, evaluation, internal approval, client acceptance, signature execution, baseline lock) emits an immutable audit event to `AuditService`.
