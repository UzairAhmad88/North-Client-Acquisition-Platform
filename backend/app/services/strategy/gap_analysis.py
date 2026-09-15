"""
Strategic Gap Analysis Subsystem for Phase 51.
Quantifies delta between current operational baseline and target strategic goals.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.strategy.base import StrategicObjective
except ImportError:
    from app.services.strategy.base import StrategicObjective

logger = logging.getLogger(__name__)


class GapAnalyzer:
    """Evaluates the variance between current operational state and target strategic goals."""

    def perform_gap_analysis(
        self,
        objectives: List[StrategicObjective],
    ) -> List[Dict[str, Any]]:
        """Calculates gap metrics, resource requirements, and acceleration recommendations."""
        gaps = []
        for obj in objectives:
            gap_val = obj.target_value - obj.current_value
            gap_pct = (gap_val / max(1.0, obj.target_value)) * 100.0 if obj.target_value > 0 else 0.0

            # Estimate required investment to close gap
            estimated_budget_needed = max(0.0, gap_val * 0.25) # 25% cost-to-revenue assumption
            estimated_fte_needed = max(0.5, gap_val / 100000.0)

            gaps.append({
                "objective_code": obj.objective_code,
                "objective_name": obj.name,
                "strategic_pillar": obj.strategic_pillar.value if hasattr(obj.strategic_pillar, "value") else str(obj.strategic_pillar),
                "current_value": obj.current_value,
                "target_value": obj.target_value,
                "gap_value": round(gap_val, 2),
                "gap_percentage": round(gap_pct, 1),
                "estimated_budget_needed_usd": round(estimated_budget_needed, 2),
                "estimated_fte_needed": round(estimated_fte_needed, 1),
                "urgency": "HIGH" if gap_pct > 50.0 else "MEDIUM",
            })

        return gaps
