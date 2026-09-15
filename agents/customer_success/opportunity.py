"""Customer Success Opportunity Discovery Intelligence."""

from decimal import Decimal
from typing import Any, Dict, List
from app.customer_success.base import OpportunityType


class CustomerSuccessOpportunityFinder:
    """Discovers expansion, cross-sell, and referral opportunities based on health, milestones, and high adoption."""

    def discover_opportunities(
        self,
        health_score: Decimal,
        completed_milestones: int = 0,
        high_csat_responses: int = 0,
        active_services_count: int = 1,
        goals_completed_percentage: Decimal = Decimal("0.00"),
    ) -> List[Dict[str, Any]]:
        """Identifies value-aligned expansion candidates for account managers."""
        opportunities: List[Dict[str, Any]] = []

        if health_score >= Decimal("80.00") and completed_milestones >= 3:
            opportunities.append({
                "opportunity_type": OpportunityType.EXPANSION.value,
                "title": "Scale-Up & Additional Feature Expansion",
                "description": f"Client exhibits strong health ({health_score}%) and has successfully completed {completed_milestones} milestones.",
                "estimated_value": Decimal("15000.00"),
                "confidence_score": Decimal("0.85"),
            })

        if high_csat_responses >= 2 and health_score >= Decimal("75.00"):
            opportunities.append({
                "opportunity_type": OpportunityType.REFERRAL.value,
                "title": "Advocate Referral & Case Study Candidate",
                "description": "Consistent high satisfaction scores make client an ideal candidate for peer referrals or case study co-marketing.",
                "estimated_value": Decimal("5000.00"),
                "confidence_score": Decimal("0.80"),
            })

        if active_services_count == 1 and health_score >= Decimal("70.00"):
            opportunities.append({
                "opportunity_type": OpportunityType.CROSS_SELL.value,
                "title": "Cross-Sell Maintenance & Dedicated Support SLA",
                "description": "Client is currently using a single core service; recommend managed maintenance or predictive optimization support.",
                "estimated_value": Decimal("10000.00"),
                "confidence_score": Decimal("0.75"),
            })

        if goals_completed_percentage >= Decimal("80.00"):
            opportunities.append({
                "opportunity_type": OpportunityType.NEW_PROJECT.value,
                "title": "Follow-On Phase Initiative",
                "description": f"Client has achieved {goals_completed_percentage}% of stated goals; initiate discovery for next strategic roadmap phase.",
                "estimated_value": Decimal("25000.00"),
                "confidence_score": Decimal("0.90"),
            })

        return opportunities
