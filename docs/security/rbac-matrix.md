# Predefined RBAC Role Hierarchy & Permission Matrix

## 1. Role Taxonomy

The platform establishes explicit role separations between internal North's team operations and external client portal workspaces.

### Internal Team Roles
- **`OWNER`**: Full unrestricted platform authority across all subsystems, security settings, and multi-tenant configurations.
- **`ADMIN`**: Operational platform administration, user management, and API key management.
- **`SALES`**: Lead CRM, Business Discovery, Outreach drafting, and Client Proposals.
- **`DEVELOPER`**: Assigned project execution, deliverables, technical tasks, change requests, and QA defect logging.
- **`QA`**: Test plans, test runs, defects, and release readiness evaluation.
- **`AI_ENGINEER`**: AI agent observability, prompt registry management, and evaluation runs.
- **`SECURITY`**: Security audit log inspection, tenant isolation, and emergency AI kill-switch activation.
- **`ANALYST`**: Read-only business intelligence, forecasting, and data export.
- **`VIEWER`**: Basic internal read-only access.

### External Client Roles
- **`CLIENT_OWNER`**: Full authority over client organization projects, change intake, and delivery UAT acceptance.
- **`CLIENT_ADMIN`**: Project administration, feedback submission, and change request creation.
- **`CLIENT_MEMBER`**: Project workspace collaboration and support request submission.
- **`CLIENT_REVIEWER`**: Deliverable review and UAT acceptance signoff.
- **`CLIENT_VIEWER`**: Read-only access to approved project deliverables and announcements.

---

## 2. Authoritative Permission Matrix

| Permission Domain | OWNER | ADMIN | SALES | DEVELOPER | QA | AI ENG | CLIENT ADMIN | CLIENT VIEWER |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `lead.*` | Full | Full | Full | View | View | None | None | None |
| `project.read` | Yes | Yes | Yes | Assigned | Assigned | None | Assigned | Assigned |
| `project.update` | Yes | Yes | None | Assigned | None | None | None | None |
| `outreach.send` | Yes (Gate) | Yes (Gate) | Yes (Gate) | None | None | None | None | None |
| `contract.sign` | Yes (MFA) | None | None | None | None | None | Yes (MFA) | None |
| `price.change` | Yes (Step-Up) | None | None | None | None | None | None | None |
| `uat.accept` | Yes | Yes | None | None | None | None | Yes | None |
| `ai_trace.read` | Full | Full | None | View | None | Full | None | None |
| `ai_model.promote` | Yes (MFA) | None | None | None | None | None | None | None |
| `user.manage` | Yes | Yes | None | None | None | None | Client Org | None |
| `security.audit_read` | Full | Full | None | None | None | None | None | None |
