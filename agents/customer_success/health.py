"""Customer Success Health Assessment Intelligence."""

from decimal import Decimal
from typing import Any, Dict, List, Optional
from app.customer_success.health_engine import HealthScoringEngine


class CustomerSuccessHealthEvaluator:
    """Provides automated evaluation of client health dimensions using HealthScoringEngine."""

    def __init__(self) -> None:
        self.engine = HealthScoringEngine()

    def evaluate_client_health(
        self,
        client_id: str = "client-default",
        engagement_score: Optional[Decimal] = None,
        project_health_score: Optional[Decimal] = None,
        support_satisfaction_score: Optional[Decimal] = None,
        financial_health_score: Optional[Decimal] = None,
        relationship_health_score: Optional[Decimal] = None,
        goal_progress_score: Optional[Decimal] = None,
        historical_scores: Optional[List[Decimal]] = None,
    ) -> Dict[str, Any]:
        """Calculates multi-factor health, confidence, trend, and explanation."""
        factors_input = {
            "engagement": engagement_score,
            "project_health": project_health_score,
            "support_health": support_satisfaction_score,
            "financial_health": financial_health_score,
            "satisfaction": support_satisfaction_score,
            "relationship": relationship_health_score,
            "goal_progress": goal_progress_score,
        }

        res = self.engine.calculate_health_score(
            client_id=client_id,
            factors_input=factors_input,
            historical_scores=historical_scores,
        )

        return {
            "client_id": res.client_id,
            "composite_score": res.overall_score,
            "health_band": res.health_band.value,
            "confidence_score": res.confidence,
            "trend": res.trend,
            "explanation_summary": res.explanation,
            "positive_factors": res.positive_factors,
            "risk_factors": res.risk_factors,
            "factors": [
                {
                    "factor_name": f.factor_name,
                    "weight": str(f.weight),
                    "score": str(f.score) if f.score is not None else None,
                    "confidence": f.confidence,
                }
                for f in res.factors
            ],
        }
