# Phase 06 — Lead CRM Documentation

## 1. Overview & Core Domain Concept
The Lead CRM establishes the canonical sales-opportunity layer for the **Uzaii Develop By North's** platform.

### Distinction: Business vs. Lead
- **Business**: Represents the real-world organization (e.g., gym, clinic, restaurant).
- **Lead**: Represents a specific sales opportunity involving that organization (e.g., website redesign consultation, AI automation system).

```
BUSINESS (Organization Layer)
    │
    └── LEAD (Sales Opportunity Layer)
           ├── Contacts (Primary & Secondary points of contact)
           ├── Lifecycle Stage (NEW → RESEARCHING → ... → WON / LOST)
           ├── Priority (LOW, MEDIUM, HIGH, URGENT)
           ├── Qualification & Contactability State
           └── Next Action Plan
```

---

## 2. Lead & Contact Data Models

### Table: `leads`
| Column | Type | Constraints / Description |
|---|---|---|
| `id` | `UUID` | Primary key (UUIDv4) |
| `business_id` | `UUID` | Foreign Key → `businesses.id` (`ON DELETE RESTRICT`) |
| `title` | `VARCHAR(255)` | Opportunity title (Required, Indexed) |
| `description` | `TEXT` | Detailed opportunity description (Optional) |
| `status` | `VARCHAR(50)` | Lifecycle status (Default: `NEW`, Indexed) |
| `source` | `VARCHAR(100)` | Lead origination taxonomy (Default: `MANUAL`, Indexed) |
| `source_detail` | `VARCHAR(255)` | Additional source context (Optional) |
| `priority` | `VARCHAR(50)` | Attention level: `LOW`, `MEDIUM`, `HIGH`, `URGENT` (Indexed) |
| `owner_user_id` | `UUID` | Foreign Key → `users.id` (`ON DELETE SET NULL`, Indexed) |
| `qualification_status` | `VARCHAR(50)` | `UNQUALIFIED`, `PENDING`, `QUALIFIED`, `DISQUALIFIED` |
| `contactability_status` | `VARCHAR(50)` | `UNKNOWN`, `CONTACTABLE`, `UNCONTACTABLE`, `DO_NOT_CONTACT` |
| `estimated_value` | `NUMERIC(12,2)` | Monetary value estimation (Optional) |
| `currency` | `VARCHAR(10)` | ISO currency code (Default: `USD`) |
| `next_action` | `VARCHAR(255)` | Next planned CRM action |
| `next_action_at` | `TIMESTAMPTZ` | Next action deadline timestamp |
| `first_contacted_at` | `TIMESTAMPTZ` | Timestamp when first contacted |
| `last_contacted_at` | `TIMESTAMPTZ` | Timestamp when last contacted |
| `converted_at` | `TIMESTAMPTZ` | Timestamp when converted to WON |
| `lost_at` | `TIMESTAMPTZ` | Timestamp when marked LOST |
| `loss_reason` | `VARCHAR(100)` | Categorized loss reason (Optional) |
| `notes` | `TEXT` | Internal CRM notes |
| `archived_at` | `TIMESTAMPTZ` | Archival timestamp |
| `created_at` | `TIMESTAMPTZ` | Creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | Last modification timestamp |

### Table: `contacts`
| Column | Type | Constraints / Description |
|---|---|---|
| `id` | `UUID` | Primary key (UUIDv4) |
| `business_id` | `UUID` | Foreign Key → `businesses.id` (`ON DELETE CASCADE`, Indexed) |
| `lead_id` | `UUID` | Foreign Key → `leads.id` (`ON DELETE SET NULL`, Indexed) |
| `name` | `VARCHAR(255)` | Contact full name (Required) |
| `role` | `VARCHAR(100)` | Job title or role (e.g. Owner, CTO) |
| `email` | `VARCHAR(255)` | Email address (Optional, Indexed) |
| `phone` | `VARCHAR(50)` | Phone number (Optional, Indexed) |
| `is_primary` | `BOOLEAN` | Primary contact flag for organization |

---

## 3. Lead Lifecycle & Status Transitions

Supported lifecycle stages:
- `NEW`: Newly created opportunity.
- `RESEARCHING`: Public presence analysis under way.
- `QUALIFIED`: Verified fit for platform services.
- `CONTACTED`: First outreach initiated.
- `RESPONDED`: Prospect responded.
- `INTERESTED`: Qualified interest confirmed.
- `MEETING`: Meeting scheduled.
- `PROPOSAL`: Proposal submitted.
- `WON`: Client acquired.
- `FOLLOW_UP`: Retain for follow-up.
- `NOT_INTERESTED`: Declined.
- `LOST`: Opportunity lost (recorded with `loss_reason`).
- `ARCHIVED`: Archived record.

---

## 4. API Endpoints

All endpoints require HTTP Bearer JWT Authentication.

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/leads` | Create a new lead opportunity |
| `GET` | `/api/v1/leads` | List leads (Pagination, Search, Filters, Sort) |
| `GET` | `/api/v1/leads/{id}` | Get lead profile detail |
| `PATCH` | `/api/v1/leads/{id}` | Update lead details |
| `DELETE` | `/api/v1/leads/{id}` | Archive lead (Soft delete) |
| `POST` | `/api/v1/leads/{id}/archive` | Explicit archive |
| `POST` | `/api/v1/leads/{id}/restore` | Explicit restore |
| `POST` | `/api/v1/leads/{id}/transition` | Transition status with timestamps |
| `POST` | `/api/v1/leads/{id}/assign` | Assign lead owner |
| `POST` | `/api/v1/leads/check-duplicate` | Query candidate duplicate opportunities |
| `POST` | `/api/v1/contacts` | Create contact |
| `GET` | `/api/v1/contacts` | List contacts by business or lead |
| `PATCH` | `/api/v1/contacts/{id}` | Update contact details |
| `DELETE` | `/api/v1/contacts/{id}` | Delete contact |

---

## 5. Frontend UI
- **Directory List View** (`/leads`): Paginated sales opportunities table/cards with real-time text search, status pills, priority badges, searchable Business selector dropdown in creation modal, and live duplicate opportunity warnings.
- **Detail View** (`/leads/[id]`): Detailed opportunity profile with lifecycle stage control buttons, business link, financial estimation, next action plan, primary & secondary contacts manager, internal notes, and future intelligence placeholders.
