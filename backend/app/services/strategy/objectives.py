"""
Strategic Objectives & Pillar Subsystem for Phase 51.
Manages strategic pillars, objectives lifecycle, and measurable target progress.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.strategy.base import (
        ObjectiveStatus,
        StrategicObjective,
        StrategicPillar,
    )
except ImportError:
    from app.services.strategy.base import (
        ObjectiveStatus,
        StrategicObjective,
        StrategicPillar,
    )

logger = logging.getLogger(__name__)


class ObjectiveManager:
    """Manages strategic objectives, status calculations, and evidence-grounded progress."""

    def __init__(self):
        self._objectives: Dict[str, StrategicObjective] = {}

    def create_objective(
        self,
        name: str,
        target_value: float,
        unit: str = "USD",
        baseline_value: float = 0.0,
        strategic_pillar: StrategicPillar = StrategicPillar.GROWTH,
        owner: str = "executive_team",
        priority: str = "HIGH",
        description: Optional[str] = None,
        target_date: Optional[datetime] = None,
    ) -> StrategicObjective:
        """Creates a measurable strategic objective."""
        obj = StrategicObjective(
            name=name,
            description=description,
            strategic_pillar=strategic_pillar,
            owner=owner,
            priority=priority,
            baseline_value=baseline_value,
            target_value=target_value,
            current_value=baseline_value,
            unit=unit,
            status=ObjectiveStatus.ACTIVE,
            target_date=target_date or datetime.now(timezone.utc),
            progress_percentage=0.0,
        )
        self._objectives[obj.objective_code] = obj
        return obj

    def update_progress(
        self,
        objective_code: str,
        current_value: float,
        evidence_summary: Optional[str] = None,
    ) -> StrategicObjective:
        """Updates objective current value, recalculates progress percentage, and assigns status."""
        obj = self._objectives.get(objective_code)
        if not obj:
            raise KeyError(f"Objective '{objective_code}' not found.")

        obj.current_value = current_value
        if evidence_summary:
            obj.evidence_summary = evidence_summary

        total_delta = obj.target_value - obj.baseline_value
        achieved_delta = obj.current_value - obj.baseline_value

        if total_delta != 0:
            progress = max(0.0, min(100.0, (achieved_delta / total_delta) * 100.0))
        else:
            progress = 100.0 if obj.current_value >= obj.target_value else 0.0

        obj.progress_percentage = round(progress, 2)

        # Status determination
        if obj.progress_percentage >= 100.0:
            obj.status = ObjectiveStatus.ACHIEVED
        elif obj.progress_percentage >= 65.0:
            obj.status = ObjectiveStatus.ON_TRACK
        elif obj.progress_percentage >= 35.0:
            obj.status = ObjectiveStatus.AT_RISK
        else:
            obj.status = ObjectiveStatus.OFF_TRACK

        return obj

    def list_objectives(self, pillar: Optional[StrategicPillar] = None) -> List[StrategicObjective]:
        """Lists registered objectives, optionally filtered by strategic pillar."""
        objs = list(self._objectives.values())
        if pillar:
            objs = [o for o in objs if o.strategic_pillar == pillar]
        return objs
