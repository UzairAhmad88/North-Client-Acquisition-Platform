# Multi-Tenant Isolation & IDOR Protection

## 1. Multi-Tenant Architecture

Every tenant-owned resource in the platform includes an immutable `tenant_id` column.

```text
PLATFORM
 ├── Primary Tenant (North's Internal Organization)
 │    ├── Users, Internal Teams
 │    └── Client Accounts (Client A, Client B)
 │
 └── Isolated Secondary Tenants (SaaS Ready)
      ├── Users
      └── Client Accounts
```

---

## 2. Insecure Direct Object Reference (IDOR) Defense

The platform enforces tenant boundaries in both the repository and the authorization engine:

1. **Header-Based & Session-Based Tenant Resolution**: The incoming request resolves `tenant_id` from the verified JWT session. Client-supplied headers (e.g., `X-Tenant-ID`) are only permitted if authorized by the user's tenant memberships.
2. **Repository-Level Filtering**: Queries automatically filter on `tenant_id` by default.
3. **Engine-Level Validation**: If an operation specifies a `resource_tenant_id` different from `security_ctx.tenant_id`, the engine blocks execution with `TENANT_MISMATCH`.
4. **Information Leakage Prevention**: When an unauthorized tenant attempts to probe a non-existent or foreign resource ID, the API returns a consistent `404 Not Found` rather than `403 Forbidden`, preventing attackers from verifying resource existence.
