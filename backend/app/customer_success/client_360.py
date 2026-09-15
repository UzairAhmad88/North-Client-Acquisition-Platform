"""Client 360 synthesizer consolidating identity, projects, financials, support, health, risks, and renewals."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional


class Client360Synthesizer:
    """Synthesizes all cross-module data into a complete 360-degree client relationship model."""

    @classmethod
    def build_360_view(
        cls,
        profile: Dict[str, Any],
        contacts: List[Dict[str, Any]],
        health_score: Optional[Dict[str, Any]],
        goals: List[Dict[str, Any]],
        success_plans: List[Dict[str, Any]],
        projects: List[Dict[str, Any]],
        financial_summary: Dict[str, Any],
        support_summary: Dict[str, Any],
        risks: List[Dict[str, Any]],
        opportunities: List[Dict[str, Any]],
        renewals: List[Dict[str, Any]],
        surveys: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Builds an integrated 360-degree client relationship payload."""
        now = datetime.now(timezone.utc)

        # Active vs completed project counts
        active_projects = [p for p in projects if p.get("status") not in ("COMPLETED", "CANCELLED", "ARCHIVED")]
        completed_projects = [p for p in projects if p.get("status") == "COMPLETED"]

        # Open risks count by severity
        critical_risks = [r for r in risks if r.get("severity") == "CRITICAL" and r.get("status") != "RESOLVED"]
        high_risks = [r for r in risks if r.get("severity") == "HIGH" and r.get("status") != "RESOLVED"]

        # Upcoming renewals within 90 days
        upcoming_renewals = [
            r for r in renewals
            if r.get("status") in ("UPCOMING", "PREPARATION", "REVIEW", "NEGOTIATION", "AT_RISK")
        ]

        return {
            "client_id": profile.get("client_id") or profile.get("id"),
            "business_name": profile.get("business_name", "Unknown Organization"),
            "lifecycle_stage": profile.get("lifecycle_stage", "ACTIVE"),
            "relationship_strength": profile.get("relationship_strength", "ESTABLISHED"),
            "owners": {
                "account_owner_id": profile.get("relationship_owner_id"),
                "sales_owner_id": profile.get("sales_owner_id"),
                "project_owner_id": profile.get("project_owner_id"),
                "customer_success_owner_id": profile.get("cs_owner_id"),
            },
            "contacts_count": len(contacts),
            "contacts": contacts,
            "health": health_score or {
                "overall_score": "0.00",
                "health_band": "INSUFFICIENT_DATA",
                "confidence": "LOW",
                "trend": "UNKNOWN",
            },
            "projects_overview": {
                "active_count": len(active_projects),
                "completed_count": len(completed_projects),
                "active_projects": active_projects,
            },
            "financial_overview": financial_summary,
            "support_overview": support_summary,
            "goals_overview": {
                "total_goals": len(goals),
                "goals": goals,
            },
            "success_plans": success_plans,
            "risks_overview": {
                "total_open_risks": len(critical_risks) + len(high_risks),
                "critical_count": len(critical_risks),
                "high_count": len(high_risks),
                "risks": risks,
            },
            "opportunities_overview": {
                "total_opportunities": len(opportunities),
                "opportunities": opportunities,
            },
            "renewals_overview": {
                "upcoming_count": len(upcoming_renewals),
                "renewals": upcoming_renewals,
            },
            "surveys_count": len(surveys),
            "synthesized_at": now.isoformat(),
        }
