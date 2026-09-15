"""
AI Worker Structured Handoff Subsystem for Phase 52.
Enforces that inter-worker communications pass structured, verifiable artifacts (Context, Inputs, Evidence, Assumptions, Unknowns, Output) rather than opaque reasoning strings.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.workforce.base import AIHandoff
except ImportError:
    from app.services.workforce.base import AIHandoff

logger = logging.getLogger(__name__)


class HandoffEngine:
    """Manages verified structured handoffs between specialized AI workers."""

    def __init__(self):
        self._handoffs: Dict[str, AIHandoff] = {}

    def create_handoff(
        self,
        from_worker_code: str,
        to_worker_code: str,
        task_code: str,
        context_summary: str,
        artifacts: List[Dict[str, Any]],
        expected_next_action: str,
        evidence: Optional[List[str]] = None,
        assumptions: Optional[List[str]] = None,
        unknowns: Optional[List[str]] = None,
        confidence_score: float = 1.0,
    ) -> AIHandoff:
        """Constructs an auditable structured handoff record."""
        handoff = AIHandoff(
            from_worker_code=from_worker_code,
            to_worker_code=to_worker_code,
            task_code=task_code,
            context_summary=context_summary,
            artifacts=artifacts,
            evidence=evidence or [],
            assumptions=assumptions or [],
            unknowns=unknowns or [],
            confidence_score=confidence_score,
            expected_next_action=expected_next_action,
            status="DELIVERED",
        )
        self._handoffs[handoff.handoff_code] = handoff
        logger.info(f"Structured handoff {handoff.handoff_code} created from {from_worker_code} to {to_worker_code} for task {task_code}.")
        return handoff

    def get_handoff(self, handoff_code: str) -> Optional[AIHandoff]:
        return self._handoffs.get(handoff_code)

    def list_handoffs(
        self,
        worker_code: Optional[str] = None,
        task_code: Optional[str] = None,
    ) -> List[AIHandoff]:
        res = list(self._handoffs.values())
        if worker_code:
            res = [h for h in res if h.from_worker_code == worker_code or h.to_worker_code == worker_code]
        if task_code:
            res = [h for h in res if h.task_code == task_code]
        return res
