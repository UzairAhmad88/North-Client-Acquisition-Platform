"""
Strategic Decision Governance Subsystem for Phase 51.
Records authorized human executive strategic decisions and rejected alternatives.
Enforces non-negotiable rule: AI presents options; only authorized human leaders decide.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.strategy.base import StrategicDecision
except ImportError:
    from app.services.strategy.base import StrategicDecision

logger = logging.getLogger(__name__)


class StrategicDecisionManager:
    """Manages strategic decisions, human approvals, and organizational rationale preservation."""

    def __init__(self):
        self._decisions: Dict[str, StrategicDecision] = {}

    def record_decision(
        self,
        question: str,
        context_summary: str,
        selected_option: Dict[str, Any],
        rationale: str,
        decision_owner: str,
        rejected_options: Optional[List[Dict[str, Any]]] = None,
        plan_version: int = 1,
    ) -> StrategicDecision:
        """Records an immutable human strategic decision."""
        if not decision_owner:
            raise ValueError("Strategic decisions require an explicitly named human decision owner.")

        dec = StrategicDecision(
            question=question,
            context_summary=context_summary,
            selected_option=selected_option,
            rejected_options=rejected_options or [],
            rationale=rationale,
            decision_owner=decision_owner,
            approved_at=datetime.now(timezone.utc),
            plan_version=plan_version,
        )
        self._decisions[dec.decision_code] = dec
        return dec

    def list_decisions(self) -> List[StrategicDecision]:
        """Lists recorded strategic decisions."""
        return list(self._decisions.values())
