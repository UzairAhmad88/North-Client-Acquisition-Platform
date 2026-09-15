# Phase 07 — Service Catalog Documentation

## 1. Overview & Core Domain Concept
The Service Catalog defines the structured offerings of **North's** (web development, software systems, business automation, AI assistants). It serves as the single source of truth for solution capabilities, delivery models, pricing structures, features, requirements, and target business types.

### Domain Hierarchy
```
SERVICE CATALOG (North's Solution Capabilities)
    │
    ├── Web Development (Business Website, Restaurant Website, Gym Website)
    ├── Software Development (Custom CRM, Business Dashboard, Management Systems)
    ├── Business Automation (Lead Routing, Notification Workflows)
    └── AI Systems (AI Support Agent, AI Lead Qualification RAG)
            │
            └── LEAD-SERVICE JUNCTION (lead_services)
                   ├── Relationship Type (CONSIDERED, RECOMMENDED, SELECTED, REJECTED)
                   └── Provenance Source (HUMAN, RULE, AI)
```

---

## 2. Service Data Models

### Table: `services`
| Column | Type | Constraints / Description |
|---|---|---|
| `id` | `UUID` | Primary Key (UUIDv4) |
| `name` | `VARCHAR(255)` | Service display title (Required, Indexed) |
| `slug` | `VARCHAR(255)` | Unique URL-safe identifier (Unique, Required, Indexed) |
| `short_description` | `VARCHAR(500)` | Summary for cards and quick overview (Optional) |
| `description` | `TEXT` | Detailed solution explanation (Optional) |
| `category` | `VARCHAR(100)` | Taxonomy: `WEB_DEVELOPMENT`, `SOFTWARE_DEVELOPMENT`, `BUSINESS_AUTOMATION`, `AI_SYSTEMS`, `DATA_ANALYTICS`, etc. |
| `subcategory` | `VARCHAR(100)` | Sub-category classification (Optional) |
| `status` | `VARCHAR(50)` | `DRAFT`, `ACTIVE`, `PAUSED`, `ARCHIVED` (Default: `ACTIVE`) |
| `delivery_model` | `VARCHAR(50)` | `FIXED_PROJECT`, `CUSTOM_QUOTE`, `SUBSCRIPTION`, `RETAINER`, `HOURLY`, `CONSULTATION` |
| `pricing_model` | `VARCHAR(50)` | `FIXED`, `STARTING_AT`, `RANGE`, `CUSTOM`, `NOT_SET` |
| `base_price` | `NUMERIC(12,2)` | Base price estimate (Optional) |
| `price_min` | `NUMERIC(12,2)` | Minimum price bound (Optional) |
| `price_max` | `NUMERIC(12,2)` | Maximum price bound (Optional) |
| `currency` | `VARCHAR(10)` | ISO currency code (Default: `USD`) |
| `estimated_duration_days` | `INTEGER` | Estimated delivery timeframe in days (Optional) |
| `is_featured` | `BOOLEAN` | Highlighted catalog item flag (Default: `false`) |
| `is_active` | `BOOLEAN` | Commercial availability flag (Default: `true`) |
| `features` | `JSON` | Structured list of solution features |
| `requirements` | `JSON` | Structured list of client inputs required |
| `target_business_types` | `JSON` | Target business industry tags |
| `archived_at` | `TIMESTAMPTZ` | Archival timestamp |
| `created_at` | `TIMESTAMPTZ` | Creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Modification timestamp |

### Table: `lead_services` (Junction)
| Column | Type | Constraints / Description |
|---|---|---|
| `id` | `UUID` | Primary Key (UUIDv4) |
| `lead_id` | `UUID` | Foreign Key → `leads.id` (`ON DELETE CASCADE`, Indexed) |
| `service_id` | `UUID` | Foreign Key → `services.id` (`ON DELETE CASCADE`, Indexed) |
| `relationship_type` | `VARCHAR(50)` | `CONSIDERED`, `RECOMMENDED`, `SELECTED`, `REJECTED` |
| `source` | `VARCHAR(50)` | Provenance: `HUMAN`, `RULE`, `AI`, `IMPORT`, `OTHER` |
| `notes` | `TEXT` | Notes on service fit |

---

## 3. Seed Framework
North's initial service catalog is automatically seeded via `backend/app/services/seed_catalog.py` and `scripts/seed.py`.
The seed process is repeatable and idempotent based on slug checking:
- `business-website`: Business Website
- `restaurant-website`: Restaurant Website & Menu System
- `gym-website`: Gym & Fitness Club Platform
- `crm-system`: Custom CRM & Lead Management System
- `business-dashboard`: Business Executive Dashboard
- `lead-management-automation`: Lead Management & Outreach Automation
- `ai-customer-support`: AI Customer Support Assistant
- `ai-lead-qualification`: AI Lead Qualification System

---

## 4. API Endpoints

All service administration and lead-service mutation APIs require HTTP Bearer JWT Authentication.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/services` | Create new catalog service |
| `GET` | `/api/v1/services` | List catalog services (Pagination, Search, Category/Status/Pricing Filters, Sort) |
| `GET` | `/api/v1/services/{id}` | Get service by ID |
| `GET` | `/api/v1/services/slug/{slug}` | Get service by unique slug |
| `PATCH` | `/api/v1/services/{id}` | Update service fields |
| `DELETE` | `/api/v1/services/{id}` | Archive service (Soft delete) |
| `POST` | `/api/v1/services/{id}/archive` | Explicit archive |
| `POST` | `/api/v1/services/{id}/restore` | Explicit restore |
| `GET` | `/api/v1/leads/{lead_id}/services` | List services associated with a lead |
| `POST` | `/api/v1/leads/{lead_id}/services` | Associate catalog service with lead |
| `DELETE` | `/api/v1/leads/{lead_id}/services/{service_id}` | Remove service association from lead |

---

## 5. Frontend UI
- **Catalog Directory** (`/services`): Category tabs (`All`, `Web Development`, `Software Systems`, `Business Automation`, `AI Systems`), search bar, pricing model filter, service cards grid displaying price indicators, delivery models, and duration estimates.
- **Service Detail Profile** (`/services/[id]`): Solution overview, structured features checklist, required client inputs, target business types, pricing overview, and record metadata.
- **Lead Detail Services Component** (`/leads/[id]`): "Offered / Target Services" manager enabling operators to attach catalog solutions to a Lead, specify relationship type (`CONSIDERED`, `RECOMMENDED`, `SELECTED`), and manage existing attachments.
