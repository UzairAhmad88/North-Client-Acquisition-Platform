# Phase 08 — Dashboard Operational Command Center

## Overview

The **Dashboard** serves as the primary authenticated workspace and personal AI-business command center for **Uzaii Develop By North's**. It provides immediate clarity for operating North's client acquisition and service management workflow by answering three operational questions:

1. **What is happening?** (Active businesses, open lead metrics, service catalog overview)
2. **What needs my attention?** (High priority leads, overdue scheduled actions, incomplete business records)
3. **What should I do next?** (Upcoming scheduled lead actions, pipeline stage progression, quick action shortcuts)

---

## Architectural Principles

1. **Operational Command Center, Not Decorative Analytics**: Focuses strictly on actionable CRM operational data without vanity metrics or speculative AI projections.
2. **Database Aggregate Query Efficiency**: All metrics and summary snapshots use SQL aggregate queries (`COUNT`, `GROUP BY`, filtered aggregates) executed directly in PostgreSQL.
3. **Graceful UI Degradation & Skeleton Loading**: Handles loading, empty, and partial data states with clean skeleton placeholders and retry mechanisms.
4. **Security & Authentication Enforcement**: Protected by JWT session token validation; unauthenticated requests are intercepted and redirected to `/login`.

---

## Metric Definitions

| Metric Name | Source / Filter Criteria | Description |
| :--- | :--- | :--- |
| **Active Businesses** | `Business.status == 'ACTIVE'` | Real-world organizations ready for engagement. |
| **Total Businesses** | All `Business` records | Total count of registered businesses. |
| **Open Leads** | `Lead.status NOT IN ('LOST', 'WON', 'ARCHIVED')` | Active sales opportunities in progress. |
| **Qualified Leads** | `Lead.qualification_status == 'QUALIFIED' AND Lead.status != 'ARCHIVED'` | Leads meeting qualification requirements. |
| **High Priority Leads** | Open Leads with `Lead.priority IN ('HIGH', 'URGENT')` | High-value or urgent lead opportunities. |
| **Overdue Actions** | Active Leads with `next_action_at < UTC now` | Past-due scheduled follow-ups or reviews. |
| **Upcoming Actions** | Active Leads with `next_action_at >= UTC now` | Future scheduled sales actions. |
| **Incomplete Businesses**| Active Businesses missing phone, email, or website | Data quality improvement targets. |

---

## REST API Specification

### 1. Get Dashboard Summary

```http
GET /api/v1/dashboard/summary
Authorization: Bearer <JWT_ACCESS_TOKEN>
```

#### Response (200 OK)

```json
{
  "data": {
    "businesses": {
      "active_count": 24,
      "total_count": 28
    },
    "leads": {
      "open_count": 17,
      "qualified_count": 6,
      "high_priority_count": 4,
      "total_count": 22
    },
    "pipeline": {
      "counts": {
        "NEW": 8,
        "QUALIFIED": 6,
        "CONTACTED": 3
      }
    },
    "attention": {
      "high_priority_leads_count": 4,
      "overdue_actions_count": 2,
      "incomplete_data_businesses_count": 3
    },
    "overdue_actions": [
      {
        "lead_id": "...",
        "lead_title": "Apex Web Redesign",
        "business_id": "...",
        "business_name": "Apex Solutions",
        "next_action": "Prepare Proposal",
        "next_action_at": "2026-09-06T12:00:00Z",
        "priority": "HIGH"
      }
    ],
    "upcoming_actions": [
      {
        "lead_id": "...",
        "lead_title": "Apex AI Chatbot",
        "business_id": "...",
        "business_name": "Apex Solutions",
        "next_action": "Client Demo",
        "next_action_at": "2026-09-11T14:00:00Z",
        "priority": "URGENT"
      }
    ],
    "recent_leads": [],
    "recent_businesses": [],
    "services": {
      "active_services_count": 4,
      "featured_services_count": 2,
      "total_services_count": 4,
      "category_counts": {
        "WEB_DEVELOPMENT": 1,
        "AI_SYSTEMS": 1
      }
    }
  }
}
```

---

## Frontend Components & Layout

- **`DashboardHeader`**: Displays personalized greeting based on current user time and display name, plus manual refresh button.
- **`PrimaryKPIs`**: 4 high-value metric cards linking directly to filtered views.
- **`QuickActionsBar`**: Direct navigation shortcuts (`+ Add Business`, `+ Create Lead`, `View Businesses`, `View Leads`, `Manage Services`).
- **`AttentionPanel`**: Highlights items requiring immediate operational review (high priority, overdue actions, incomplete data).
- **`PipelineSnapshot`**: Visual distribution of leads across all lifecycle stages.
- **`RecentLeadsCard` & `RecentBusinessesCard`**: Compact bounded lists showing recent system updates.
- **`UpcomingActionsCard` & `ServiceSnapshotCard`**: Chronological schedule and catalog overview.
- **`DashboardSkeleton`**: Smooth animated skeleton loading state.

---

## Verification & Testing

- **Backend Unit Tests**: `tests/unit/backend/test_dashboard.py` (Passing 3/3).
- **Full Backend Suite**: `tests/unit/backend/` (Passing 42/42).
- **Mypy Type Check**: Clean (0 errors across 122 source files).
- **Ruff Linter**: Clean (0 errors).
- **Next.js Production Build**: Clean build output across all 18 routes.
