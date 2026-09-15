"""
Prioritization Engine for Phase 51: Autonomous Business Strategy & Goal Optimization Engine.
Computes multi-factor explainable priority rankings across proposed initiatives.
"""

import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.strategy.base import StrategicInitiative
except ImportError:
    from app.services.strategy.base import StrategicInitiative

logger = logging.getLogger(__name__)


class PrioritizationEngine:
    """
    Evaluates strategic initiatives across Expected Value, Cost Efficiency, Strategic Alignment,
    Feasibility, Urgency, and Risk to produce an explainable priority ranking.
    """

    def score_initiative(
        self,
        initiative: StrategicInitiative,
        strategic_alignment_score: float = 0.85,
        urgency_score: float = 0.75,
    ) -> Dict[str, Any]:
        """Calculates normalized priority score (0-100) and returns component breakdown."""
        cost = max(1.0, initiative.estimated_cost_usd)
        val = max(0.0, initiative.expected_value_usd)
        
        # Value ratio normalized to 0-1 (capped at 5x return)
        roi_multiple = val / cost
        norm_roi = min(1.0, roi_multiple / 5.0)

        feasibility = max(0.0, min(1.0, initiative.feasibility_score))
        risk = max(0.0, min(1.0, initiative.risk_score))
        alignment = max(0.0, min(1.0, strategic_alignment_score))
        urgency = max(0.0, min(1.0, urgency_score))

        # Core weighted sum
        base_score = (
            (0.35 * norm_roi)
            + (0.25 * alignment)
            + (0.20 * feasibility)
            + (0.20 * urgency)
        )

        # Risk penalty discount (up to 30% reduction for high risk)
        risk_discount = 1.0 - (0.30 * risk)
        final_score = round(base_score * risk_discount * 100.0, 2)
        initiative.priority_score = final_score

        return {
            "initiative_code": initiative.initiative_code,
            "title": initiative.title,
            "priority_score": final_score,
            "components": {
                "roi_multiple": round(roi_multiple, 2),
                "normalized_roi": round(norm_roi, 3),
                "strategic_alignment": round(alignment, 2),
                "feasibility": round(feasibility, 2),
                "urgency": round(urgency, 2),
                "risk_penalty": round(risk, 2),
            },
            "explanation": (
                f"Scored {final_score:.1f}/100 with {roi_multiple:.1f}x ROI multiple, "
                f"{alignment*100:.0f}% strategic alignment, and {risk*100:.0f}% risk factor."
            ),
        }

    def rank_initiatives(
        self,
        initiatives: List[StrategicInitiative],
        weights_override: Optional[Dict[str, float]] = None,
    ) -> List[Dict[str, Any]]:
        """Ranks a list of initiatives descending by computed priority score."""
        scored = [self.score_initiative(init) for init in initiatives]
        scored.sort(key=lambda x: x["priority_score"], reverse=True)
        return scored
