"""Customer Success Action Recommendations Engine."""

from decimal import Decimal
from typing import Any, Dict, List


class CustomerSuccessRecommendationEngine:
    """Generates actionable, contextual next-step recommendations for Customer Success Managers."""

    def generate_recommendations(
        self,
        health_score: Decimal,
        days_since_qbr: int = 90,
        unmet_goals_count: int = 0,
        renewal_days_remaining: int = 180,
    ) -> List[Dict[str, Any]]:
        """Synthesizes context into prioritised CSM actions."""
        recs: List[Dict[str, Any]] = []

        if days_since_qbr >= 90:
            recs.append({
                "action": "SCHEDULE_QBR",
                "priority": "HIGH" if days_since_qbr >= 120 else "MEDIUM",
                "title": "Schedule Executive Business Review (QBR)",
                "reasoning": f"Last QBR was conducted {days_since_qbr} days ago. Aligning with leadership maintains strategic momentum.",
            })

        if unmet_goals_count > 0:
            recs.append({
                "action": "REVIEW_CLIENT_GOALS",
                "priority": "HIGH",
                "title": "Review In-Progress Strategic Goals",
                "reasoning": f"Client has {unmet_goals_count} goal(s) requiring active tracking or milestone refinement.",
            })

        if 0 <= renewal_days_remaining <= 90:
            recs.append({
                "action": "PREPARE_RENEWAL_PACKAGE",
                "priority": "CRITICAL" if renewal_days_remaining <= 30 else "HIGH",
                "title": "Initiate Commercial Renewal Engagement",
                "reasoning": f"Renewal window is open ({renewal_days_remaining} days remaining). Assemble performance metrics and contract baseline.",
            })

        if health_score >= Decimal("85.00"):
            recs.append({
                "action": "REQUEST_TESTIMONIAL",
                "priority": "LOW",
                "title": "Request Client Testimonial / CSAT Review",
                "reasoning": "High health score indicates strong satisfaction; opportune time for feedback or referral program enrollment.",
            })

        return recs
