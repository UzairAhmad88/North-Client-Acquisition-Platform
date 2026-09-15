# Dual Approval Protocol & Invalidations

This document describes internal operator approvals, client sign-offs, and approval invalidation rules in **Uzaii Develop By North's Phase 28**.

---

## 1. Dual Approval Protocol

To advance a change request from proposal to baseline revision:
1. **Internal Approval**: Granted by an authorized internal operator (`approver_id`).
2. **Client Approval**: Explicit assent submitted by an authorized client signer with cryptographic SHA-256 payload verification.

---

## 2. Approval Invalidation Rule

> **CRITICAL RULE**:
> Any edit or modification to a change proposal version invalidates all prior internal and client approvals. The system forces a version increment ($v \rightarrow v+1$) and requires re-issue and re-signing of the new version's SHA-256 content hash.
