"""
Strategic Initiatives Subsystem for Phase 51.
Manages strategic initiatives, funding allocations, and operational capacity demands.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.strategy.base import InitiativeStatus, StrategicInitiative
except ImportError:
    from app.services.strategy.base import InitiativeStatus, StrategicInitiative

logger = logging.getLogger(__name__)


class InitiativeManager:
    """Manages strategic initiatives portfolio, capacity requirements, and lifecycle stages."""

    def __init__(self):
        self._initiatives: Dict[str, StrategicInitiative] = {}

    def create_initiative(
        self,
        title: str,
        owner: str,
        category: str = "GROWTH",
        expected_value_usd: float = 50000.0,
        estimated_cost_usd: float = 15000.0,
        required_fte_capacity: float = 1.5,
        estimated_duration_weeks: float = 6.0,
        description: Optional[str] = None,
    ) -> StrategicInitiative:
        """Registers a new strategic initiative proposal."""
        init = StrategicInitiative(
            title=title,
            description=description,
            category=category,
            owner=owner,
            status=InitiativeStatus.IDEA,
            expected_value_usd=expected_value_usd,
            estimated_cost_usd=estimated_cost_usd,
            required_fte_capacity=required_fte_capacity,
            estimated_duration_weeks=estimated_duration_weeks,
        )
        self._initiatives[init.initiative_code] = init
        return init

    def update_initiative_status(
        self,
        initiative_code: str,
        status: InitiativeStatus,
        is_funded: Optional[bool] = None,
    ) -> StrategicInitiative:
        """Transitions initiative status and updates funding flag."""
        init = self._initiatives.get(initiative_code)
        if not init:
            raise KeyError(f"Initiative '{initiative_code}' not found.")

        init.status = status
        if is_funded is not None:
            init.is_funded = is_funded

        return init

    def list_initiatives(self, status: Optional[InitiativeStatus] = None) -> List[StrategicInitiative]:
        """Lists registered initiatives, optionally filtered by status."""
        items = list(self._initiatives.values())
        if status:
            items = [i for i in items if i.status == status]
        return items
