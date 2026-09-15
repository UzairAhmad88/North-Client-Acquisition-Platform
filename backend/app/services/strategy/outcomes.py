"""
Strategic Outcome Learning Subsystem for Phase 51.
Compares planned strategic milestones against observed real-world outcomes to calculate prediction errors.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


class OutcomeLearningEngine:
    """Calculates strategic variance, tracks execution efficacy, and prepares organizational learning items."""

    def record_strategic_outcome(
        self,
        observed_period: str,
        planned_metrics: Dict[str, Any],
        actual_metrics: Dict[str, Any],
        decision_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Calculates prediction variance and returns outcome learning record."""
        plan_rev = float(planned_metrics.get("expected_revenue_usd", 1.0))
        act_rev = float(actual_metrics.get("actual_revenue_usd", plan_rev))

        variance_pct = ((act_rev - plan_rev) / plan_rev * 100.0) if plan_rev != 0 else 0.0
        model_error = round(abs(variance_pct) / 100.0, 4)

        return {
            "outcome_code": f"OUT-{uuid.uuid4().hex[:6].upper()}",
            "observed_period": observed_period,
            "decision_id": decision_id,
            "planned_metrics": planned_metrics,
            "actual_metrics": actual_metrics,
            "variance_percentage": round(variance_pct, 2),
            "model_prediction_error": model_error,
            "learning_lesson": (
                f"Observed {variance_pct:+.1f}% variance in {observed_period}. "
                f"Prediction error {model_error * 100:.1f}%. "
                f"Feed variance parameters into Phase 48 Organizational Memory."
            ),
        }
