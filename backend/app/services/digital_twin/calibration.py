"""
Outcome Learning and Model Calibration Engine for Phase 50: Unified Digital Twin.
Compares simulated predictions against real-world observed outcomes and computes calibration adjustments.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.digital_twin.base import (
        CalibrationReport,
        OutcomeRecord,
    )
except ImportError:
    from app.services.digital_twin.base import (
        CalibrationReport,
        OutcomeRecord,
    )

logger = logging.getLogger(__name__)


class OutcomeLearningManager:
    """
    Tracks prediction errors, calculates model variance, and prepares parameter calibration reports.
    """

    def record_outcome(
        self,
        observed_period: str,
        predicted_metrics: Dict[str, Any],
        actual_metrics: Dict[str, Any],
        decision_id: Optional[str] = None,
        scenario_id: Optional[str] = None,
    ) -> OutcomeRecord:
        """Records actual observed performance metrics alongside prior simulation predictions."""
        pred_rev = float(predicted_metrics.get("cumulative_revenue_usd", 1.0))
        act_rev = float(actual_metrics.get("cumulative_revenue_usd", pred_rev))

        variance_pct = ((act_rev - pred_rev) / pred_rev * 100.0) if pred_rev != 0 else 0.0
        model_error = abs(variance_pct) / 100.0

        return OutcomeRecord(
            decision_id=decision_id,
            scenario_id=scenario_id,
            observed_period=observed_period,
            predicted_metrics=predicted_metrics,
            actual_metrics=actual_metrics,
            variance_percentage=round(variance_pct, 2),
            model_error=round(model_error, 4),
        )

    def generate_calibration_report(
        self,
        outcome_records: List[OutcomeRecord],
    ) -> CalibrationReport:
        """
        Analyzes historical outcome records and proposes parameter calibration nudges without
        silently overwriting production baselines.
        """
        if not outcome_records:
            return CalibrationReport(
                calibrations_count=0,
                parameter_updates=[],
                average_prediction_error=0.0,
                summary="No outcome records available for calibration.",
            )

        avg_error = sum(r.model_error for r in outcome_records) / len(outcome_records)
        avg_variance = sum(r.variance_percentage for r in outcome_records) / len(outcome_records)

        # Propose calibration adjustment for primary driver
        proposed_updates = []
        if abs(avg_variance) > 5.0:
            direction = "INCREASE" if avg_variance > 0 else "DECREASE"
            proposed_updates.append({
                "parameter_code": "lead_conversion_rate",
                "recommended_action": f"{direction} baseline estimate by {abs(avg_variance) * 0.5:.1f}%",
                "reason": f"Systematic historical revenue variance of {avg_variance:+.1f}% observed across {len(outcome_records)} cycles.",
            })

        summary = (
            f"Evaluated {len(outcome_records)} historical outcome cycles. "
            f"Average model prediction error: {avg_error * 100.0:.1f}%. "
            f"Average directional variance: {avg_variance:+.1f}%."
        )

        return CalibrationReport(
            calibrations_count=len(outcome_records),
            parameter_updates=proposed_updates,
            average_prediction_error=round(avg_error, 4),
            summary=summary,
        )
