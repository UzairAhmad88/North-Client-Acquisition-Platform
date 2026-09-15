"""
OKR Key Results Subsystem for Phase 51.
Manages quantitative key results, measurement methods, and evidence synchronization.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.strategy.base import KeyResult
except ImportError:
    from app.services.strategy.base import KeyResult

logger = logging.getLogger(__name__)


class OKRManager:
    """Manages quantitative Key Results linked to Strategic Objectives."""

    def __init__(self):
        self._key_results: Dict[str, KeyResult] = {}

    def create_key_result(
        self,
        objective_id: str,
        name: str,
        target_value: float,
        unit: str = "PERCENT",
        baseline_value: float = 0.0,
        measurement_method: str = "AUTOMATED_TELEMETRY",
        source_metric: Optional[str] = None,
        owner: str = "team_lead",
        deadline: Optional[datetime] = None,
    ) -> KeyResult:
        """Registers a new quantitative Key Result."""
        kr = KeyResult(
            objective_id=objective_id,
            name=name,
            baseline_value=baseline_value,
            target_value=target_value,
            current_value=baseline_value,
            unit=unit,
            progress_percentage=0.0,
            measurement_method=measurement_method,
            source_metric=source_metric,
            owner=owner,
            deadline=deadline or datetime.now(timezone.utc),
        )
        self._key_results[kr.kr_code] = kr
        return kr

    def record_kr_progress(
        self,
        kr_code: str,
        current_value: float,
    ) -> KeyResult:
        """Updates Key Result telemetry and calculates progress percentage."""
        kr = self._key_results.get(kr_code)
        if not kr:
            raise KeyError(f"Key Result '{kr_code}' not found.")

        kr.current_value = current_value
        total_delta = kr.target_value - kr.baseline_value
        achieved_delta = kr.current_value - kr.baseline_value

        if total_delta != 0:
            prog = max(0.0, min(100.0, (achieved_delta / total_delta) * 100.0))
        else:
            prog = 100.0 if kr.current_value >= kr.target_value else 0.0

        kr.progress_percentage = round(prog, 2)
        return kr

    def list_key_results_for_objective(self, objective_id: str) -> List[KeyResult]:
        """Lists key results belonging to a specific objective."""
        return [kr for kr in self._key_results.values() if kr.objective_id == objective_id]
