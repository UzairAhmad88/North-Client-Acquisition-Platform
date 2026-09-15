# Client UAT, Delivery Package & Handover Policy

## 1. Client UAT Verification & Cryptographic Sign-off

Client UAT is conducted inside the dedicated Client Portal workspace.
- **Client Sign-off**: Requires explicit form submission with signer name, title, and acceptance statement.
- **SHA-256 Content Hash**: The system computes a cryptographic SHA-256 hash over the session ID, signer ID, and acceptance statement:
  $$\text{Sign-off Hash} = \text{SHA256}(\text{uat\_session\_id} \mathbin{\Vert} \text{signer\_id} \mathbin{\Vert} \text{statement})$$
- **Non-Repudiation**: Viewing, downloading, or email discussions do **NOT** constitute acceptance.

---

## 2. Delivery Package Manifest

Final software deliverables are registered as immutable delivery packages:
- Each package contains file URL, size in bytes, and SHA-256 checksum.
- Linked directly to approved release version tag.

---

## 3. Final Handover Checklist & Project Completion

To transition project status to `COMPLETED`, the following 5 criteria must be verified:
1. **Code Repository Transferred**: Write access and main branch ownership transferred to client organization.
2. **Technical Documentation Delivered**: System architecture, API documentation, and runbooks delivered.
3. **Credentials Transferred**: Production API keys, database credentials, and secrets securely transferred via encrypted vault.
4. **Training Completed**: Client administrator training completed.
5. **Deployment Verified**: Production deployment smoke test verified.

Upon final sign-off, `Project.status` is set to `COMPLETED` and locked.
