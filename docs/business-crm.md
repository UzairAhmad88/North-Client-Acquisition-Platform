# Phase 05 — Business CRM Documentation

## 1. Overview & Core Domain Concept
The Business CRM serves as the canonical organization-level registry for the **Uzaii Develop By North's** platform.
A **Business** represents a real-world organization (company, local service provider, clinic, gym, restaurant) that may eventually be associated with leads, website audits, outreach campaigns, proposals, or contracts.

### Concept Hierarchy
```
Business (Canonical Real-World Organization)
  ├── Contacts
  ├── Leads (Phase 06)
  ├── Research Records (Phase 10)
  ├── Website Audits (Phase 11)
  ├── Outreach Messages (Phase 14)
  ├── Conversations (Phase 16)
  ├── Opportunities (Phase 18)
  └── Activities
```

> **Key Distinction**: A **Business** is the real-world company itself. A **Lead** represents a specific sales/outreach opportunity involving that company.

---

## 2. Business Data Model
Table: `businesses`

| Column | Type | Constraints / Description |
|---|---|---|
| `id` | `UUID` | Primary key (UUIDv4) |
| `name` | `VARCHAR(255)` | Display name (Required, Indexed) |
| `normalized_name` | `VARCHAR(255)` | Cleaned name for deduplication & search (Required, Indexed) |
| `legal_name` | `VARCHAR(255)` | Registered corporate name (Optional) |
| `description` | `TEXT` | Summary of operations (Optional) |
| `business_type` | `VARCHAR(100)` | Classification e.g. `SERVICE`, `RETAIL`, `CLINIC` |
| `industry` | `VARCHAR(100)` | Field taxonomy e.g. `FITNESS`, `HEALTHCARE`, `RESTAURANT` |
| `category` | `VARCHAR(100)` | Specific category (Optional) |
| `subcategory` | `VARCHAR(100)` | Subcategory detail (Optional) |
| `phone` | `VARCHAR(50)` | Display phone number (Optional, Indexed) |
| `normalized_phone` | `VARCHAR(50)` | Digits-only representation (Optional, Indexed) |
| `email` | `VARCHAR(255)` | Contact email (Optional, Indexed) |
| `normalized_email` | `VARCHAR(255)` | Lowercase stripped email (Optional, Indexed) |
| `website_url` | `VARCHAR(500)` | Official web address (Optional, Indexed) |
| `normalized_website` | `VARCHAR(500)` | Host/domain string without protocol or trailing slash (Indexed) |
| `address` | `VARCHAR(255)` | Street address (Optional) |
| `city` | `VARCHAR(100)` | City location (Optional, Indexed) |
| `state` | `VARCHAR(100)` | Region / Province (Optional) |
| `country` | `VARCHAR(100)` | Country (Default: `Pakistan`) |
| `postal_code` | `VARCHAR(20)` | ZIP/Postal code (Optional) |
| `status` | `VARCHAR(50)` | Lifecycle state: `ACTIVE`, `INACTIVE`, `ARCHIVED` (Default: `ACTIVE`) |
| `source` | `VARCHAR(100)` | Origination e.g. `MANUAL`, `CSV`, `GOOGLE_MAPS` (Default: `MANUAL`) |
| `source_url` | `VARCHAR(500)` | External directory link (Optional) |
| `external_id` | `VARCHAR(255)` | External identifier from source provider (Optional, Indexed) |
| `created_by_user_id` | `UUID` | Foreign Key → `users.id` (Optional, Indexed) |
| `archived_at` | `TIMESTAMPTZ` | Timestamp when record was archived |
| `created_at` | `TIMESTAMPTZ` | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Record last modification timestamp |

---

## 3. Duplicate Detection Engine
To prevent duplicate records without dangerous automatic merges, the service features a deterministic matching engine (`check_duplicates`):

### Confidence Signals
1. `same_source_external_id` → Confidence: **0.99**
2. `same_email` → Confidence: **0.95**
3. `same_website_domain` → Confidence: **0.90**
4. `same_phone` → Confidence: **0.85**
5. `same_name_and_city` → Confidence: **0.80**

If maximum confidence across matching candidates is $\ge 0.70$, `possible_duplicate` is flagged with evidence signals in API responses.

---

## 4. Business Data Quality Engine
Calculates an objective completeness score (0–100%) for each business record:
- Base score: **100**
- Missing `website_url`: **-20**
- Missing `email`: **-15**
- Missing `phone`: **-15**
- Missing `city`: **-15**
- Missing `address`: **-10**
- Missing `description`: **-10**
- Missing `category`: **-5**
- Missing `source_url`: **-5**

---

## 5. API Endpoints

All endpoints require HTTP Bearer JWT Authentication (`Authorization: Bearer <token>`).

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/businesses` | Create a new business organization |
| `GET` | `/api/v1/businesses` | List businesses (Pagination, Search, Filter, Sort) |
| `GET` | `/api/v1/businesses/{id}` | Get business profile detail |
| `PATCH` | `/api/v1/businesses/{id}` | Update business profile fields |
| `DELETE` | `/api/v1/businesses/{id}` | Archive business record (Soft delete) |
| `POST` | `/api/v1/businesses/{id}/archive` | Explicitly archive business record |
| `POST` | `/api/v1/businesses/{id}/restore` | Restore archived business record |
| `POST` | `/api/v1/businesses/check-duplicate` | Query candidate duplicate signals |

---

## 6. Frontend UI
- **Directory List View** (`/businesses`): Paginated business records with real-time text search, status filters (`ACTIVE`, `INACTIVE`, `ARCHIVED`), sorting options, data quality score indicators, and a creation modal with live duplicate detection alerts.
- **Detail View** (`/businesses/[id]`): Detailed organization profile with overview details, location, record metadata, data quality breakdown, status toggle, archive/restore dialogs, and future CRM relationship placeholders.
