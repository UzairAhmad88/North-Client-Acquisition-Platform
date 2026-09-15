# Storage, File Validation & Security Isolation

## 1. Multi-Tenant Storage Partitioning

All stored objects are partitioned strictly by `tenant_id` and `workspace_id`:

$$\text{storage\_key} = \text{tenants}/\{\text{tenant\_id}\}/\text{workspaces}/\{\text{workspace\_id}\}/\{\text{file\_id}\}/\{\text{filename}\}$$

- Cross-tenant directory traversal attacks are neutralized via path resolution sandboxing.
- Storage keys cannot be guessed by malicious callers.

---

## 2. File Validation & Obfuscation Defense

The `FileValidator` performs multi-tier verification before any persistent write:

1. **Size Ceilings**: Files exceeding maximum thresholds (default: 100 MB) are rejected immediately.
2. **Blocked Extensions**: `.exe`, `.bat`, `.cmd`, `.vbs`, `.ps1`, `.sh`, `.dll`, `.msi` are rejected unconditionally.
3. **Obfuscation Detection**: Disguised double extensions (such as `invoice.pdf.exe` or `contract.docx.vbs`) are identified and rejected.
4. **Magic Byte Signature Verification**: Header bytes are compared against declared extensions:
   - PDF: `%PDF-`
   - PNG: `\x89PNG\r\n\x1a\n`
   - JPEG: `\xff\xd8\xff`

---

## 3. Malware Quarantine Architecture

Every upload passes through `BaseFileScanner`:

- **Clean Status**: Progresses to persistent storage and indexing.
- **Infected Status**: Transitioned to `QUARANTINED` status, moved to quarantine isolation, and blocked from global availability.
- **Audit Logging**: Emits structured security audit records in `file_scans`.

---

## 4. Secret & Credential File Policy

Files containing credentials (API keys, private keys, database credentials) are classified as `RESTRICTED`:
- Hard-blocked from indexing in global search.
- Excluded from AI prompt context and summarization.
- Inaccessible to client portal accounts.
