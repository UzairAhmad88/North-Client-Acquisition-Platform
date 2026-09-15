# Client Asset Management & Security Protocol

This document details the file upload and publication protocol for **Uzaii Develop By North's Phase 27**.

---

## 1. File Upload Constraints

- **Maximum File Size**: $25\text{MB}$ ($26,214,400\text{ bytes}$)
- **Default Visibility**: `INTERNAL_ONLY`
- **MIME Type Allowlist**:
  - Images: `image/png`, `image/jpeg`, `image/gif`, `image/svg+xml`
  - Documents: `application/pdf`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  - Data: `text/plain`, `text/csv`, `application/json`

---

## 2. Publication Lifecycle

```text
[ File Uploaded ] 
       ↓
(Visibility = INTERNAL_ONLY)
       ↓
[ Staff Review & Sanitize ]
       ↓
(Staff Action: publish_file_to_client)
       ↓
(Visibility = CLIENT_VISIBLE)
```

Clients cannot access files while in `INTERNAL_ONLY` status.
