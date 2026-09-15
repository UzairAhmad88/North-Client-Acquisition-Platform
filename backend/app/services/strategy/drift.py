"""
Strategic Drift Detection Engine for Phase 51.
Identifies divergence between operational reality and strategic plan assumptions.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


class DriftDetectionEngine:
    """Monitors live metric telemetry against planned baselines to detect strategic drift."""

    def check_metric_drift(
        self,
        metric_name: str,
        expected_value: float,
        actual_value: float,
        drift_tolerance_pct: float = 10.0,
    ) -> Optional[Dict[str, Any]]:
        """Calculates drift delta; returns drift event if threshold is exceeded."""
        if expected_value == 0:
            return None

        delta_pct = ((actual_value - expected_value) / abs(expected_value)) * 100.0
        abs_drift = abs(delta_pct)

        if abs_drift >= drift_tolerance_pct:
            severity = "WARNING"
            if abs_drift >= 25.0:
                severity = "HIGH"
            if abs_drift >= 50.0:
                severity = "CRITICAL"

            direction = "ABOVE" if delta_pct > 0 else "BELOW"
            action = (
                f"Reforecast strategic timeline and adjust quarterly resource allocations. "
                f"{metric_name} is tracking {abs_drift:.1f}% {direction} expected plan baseline."
            )

            return {
                "drift_code": f"DRIFT-{uuid.uuid4().hex[:6].upper()}",
                "metric_name": metric_name,
                "expected_value": expected_value,
                "actual_value": actual_value,
                "drift_percentage": round(delta_pct, 2),
                "severity": severity,
                "recommended_action": action,
                "detected_at": datetime.now(timezone.utc).isoformat(),
            }

        return None
