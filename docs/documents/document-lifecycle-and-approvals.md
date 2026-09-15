# Document Lifecycle, Immutability & Approval Governance

## 1. Document Lifecycle States

Managed documents follow a formal business lifecycle:

```text
       ┌──────────┐
       │  DRAFT   │
       └────┬─────┘
            │ Submit
            ▼
┌───────────────────────┐
│ SUBMITTED_FOR_REVIEW  │
└───────────┬───────────┘
            │ Reviewer Picks Up
            ▼
     ┌──────────────┐
     │  IN_REVIEW   │
     └──────┬───────┘
            ├───► CHANGES_REQUESTED ──► DRAFT
            ├───► REJECTED
            └───► APPROVED ──► (Checksum Locked & Immutable)
                     │
                     └── Modify ──► New Draft Version v(N+1)
```

---

## 2. Immutable Approved Versions

When an operator approves a document:

1. The approval record binds to `document_id`, `version_id`, `version_number`, and `checksum_sha256`.
2. The binary content of that version is frozen and immutable.
3. If modifications are required, a new version ($v_{N+1}$) is generated in `DRAFT` status.
4. **Non-Inheritance Rule**: Approval granted to version $v_N$ does not transfer to version $v_{N+1}$.

---

## 3. Approval Integrity & Hash Verification

Before treating an approved document as an authoritative baseline or contractual commitment:

$$\text{assert } \text{SHA256}(\text{Current Content}) == \text{approval.checksum}$$

If the checksum differs, the approval is deemed invalid and flagged for security review.

---

## 4. Retention & Legal Hold Governance

- **Retention Schedules**: Configurable lifecycle retention (e.g., 365 days) after which documents transition to `ARCHIVED`.
- **Soft Deletion**: Standard deletion sets `is_deleted=True`, preserving history and audit trails.
- **Legal Hold Override**: Documents under `LEGAL_HOLD` are strictly protected from deletion. Any soft or permanent deletion attempts are halted with `403 Forbidden`.
