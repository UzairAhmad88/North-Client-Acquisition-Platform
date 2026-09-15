# Client Portal Overview

The **Uzaii Develop By North's Client Portal** is a secure, audited, and isolated workspace that enables seamless collaboration between North's internal development team and client organizations.

---

## 1. System Architecture

```text
+-----------------------------------------------------------------------+
|                    Client Organization Members                       |
|           (CLIENT_ADMIN, CLIENT_MEMBER, CLIENT_VIEWER)               |
+-----------------------------------------------------------------------+
                                   |
                                   v (HTTPS / REST API)
+-----------------------------------------------------------------------+
|                  Client Portal Router & Service Layer                 |
|             (Visibility Filter: CLIENT_VISIBLE vs INTERNAL_ONLY)     |
+-----------------------------------------------------------------------+
       |                                                   |
       v                                                   v
+-----------------------------+         +-------------------------------+
| Client Collaboration Agent  |         | Cryptographic Sign-Off Engine |
|  • Request Classifier       |         |  • SHA-256 Deliverable Finger- |
|  • Feedback Summarizer      |         |    printing                   |
|  • Action Extractor         |         |  • Non-repudiable audit logs  |
|  • Scope Creep Detector     |         +-------------------------------+
+-----------------------------+
```

---

## 2. Key Features

1. **Deliverable Review & SHA-256 Sign-Off**:
   - Version-controlled deliverable review.
   - Non-approval disclaimer: Viewing or downloading a deliverable does *NOT* equal approval.
   - Explicit assent form submission required with cryptographic SHA-256 payload hashing.

2. **Client Discussion Threads**:
   - Organized discussion threads per project or deliverable.
   - Outbound messages to clients are client-friendly and sanitized.

3. **File Asset Management**:
   - Default security setting: `INTERNAL_ONLY`.
   - Explicit staff publication required to transition files to `CLIENT_VISIBLE`.
   - MIME allowlist enforcement and 25 MB file size limits.

4. **Client Action Item Tracking**:
   - Structured checklist for required client inputs (e.g. API credentials, brand logos, domain access).

5. **ClientCollaborationAgent v1.0**:
   - AI assistant that classifies requests, extracts action items, and flags scope creep.
   - **Zero Side-Effect Policy**: Strictly prohibited from approving deliverables, accepting scope changes, modifying contracts, or promising deadlines.
