# Attribute-Based Access Control (ABAC) & Dynamic Policies

## 1. Why Pure RBAC is Insufficient

While Role-Based Access Control defines broad operational responsibilities, real-world business constraints require contextual evaluation:
- A developer should only be allowed to modify **projects to which they are actively assigned**.
- Client users may view approved deliverables but **never internal cost margins, hourly rates, or AI traces**.
- Suspended or locked accounts must have **all active sessions and background actions immediately severed**.

---

## 2. Dynamic ABAC Attributes Evaluated

The `AuthorizationEngine` combines RBAC permissions with contextual attributes in `AuthorizationContext`:

1. **`principal.status`**: If status is `SUSPENDED` or `LOCKED`, the request is immediately rejected (`ACCOUNT_SUSPENDED`).
2. **`resource_tenant_id`**: If the target resource belongs to a different tenant than `security_ctx.tenant_id`, the request is rejected with `TENANT_MISMATCH`.
3. **`project_id` & `assigned_project_ids`**: For operational roles (`DEVELOPER`, `QA`, `DESIGNER`), membership in the target project is strictly enforced (`PROJECT_MEMBERSHIP_REQUIRED`).
4. **`is_client_visible`**: If a client principal attempts to query an internal-only resource (`ai_trace`, `cost_model`, `security_events`), access is denied (`CLIENT_ACCESS_BOUNDARY_VIOLATION`).
