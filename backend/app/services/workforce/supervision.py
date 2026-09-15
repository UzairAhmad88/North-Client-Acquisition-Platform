"""
Multi-Level Supervision & Human Review Subsystem for Phase 52.
Enforces supervision boundaries (Levels 0-5) and routes sensitive / high-risk tasks to the human executive review queue.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.workforce.base import AIWorkTask, SupervisionLevel, TaskStatus
except ImportError:
    from app.services.workforce.base import AIWorkTask, SupervisionLevel, TaskStatus

logger = logging.getLogger(__name__)


class SupervisionEngine:
    """
    Supervises task execution levels (0: Deterministic, 1: Read-Only, 2: Draft, 3: Bounded Action, 4: Review, 5: Approval).
    Automatically routes items to the human review queue when conditions demand human governance.
    """

    def __init__(self):
        self._review_queue: List[Dict[str, Any]] = []

    def evaluate_task_supervision(
        self,
        task: AIWorkTask,
        confidence_score: float = 1.0,
        risk_score: float = 0.1,
    ) -> Dict[str, Any]:
        """Determines if a task requires human review or can proceed autonomously."""
        level = task.supervision_level if isinstance(task.supervision_level, int) else task.supervision_level.value

        triggers = []
        requires_review = False

        if level >= SupervisionLevel.REVIEW_REQUIRED_4.value:
            requires_review = True
            triggers.append(f"Task configured with Supervision Level {level}.")

        if confidence_score < 0.75:
            requires_review = True
            triggers.append(f"Low AI confidence score ({confidence_score:.2f} < 0.75).")

        if risk_score > 0.40 or task.risk_level in ["HIGH", "CRITICAL"]:
            requires_review = True
            triggers.append(f"Elevated risk level ({task.risk_level}).")

        if requires_review:
            review_item = {
                "review_id": f"REV-Q-{uuid.uuid4().hex[:6].upper()}",
                "task_code": task.task_code,
                "objective": task.objective,
                "worker_code": task.worker_code,
                "supervision_level": level,
                "triggers": triggers,
                "status": "PENDING_HUMAN_REVIEW",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self._review_queue.append(review_item)
            task.status = TaskStatus.REVIEW_REQUIRED
            return {
                "can_execute_autonomously": False,
                "supervision_level": level,
                "triggers": triggers,
                "review_id": review_item["review_id"],
                "notice": "Task routed to Human Executive Review Queue prior to activation.",
            }

        return {
            "can_execute_autonomously": True,
            "supervision_level": level,
            "triggers": [],
            "notice": "Task cleared for autonomous execution within bounded level.",
        }

    def get_pending_reviews(self) -> List[Dict[str, Any]]:
        return [r for r in self._review_queue if r["status"] == "PENDING_HUMAN_REVIEW"]

    def resolve_review(
        self,
        review_id: str,
        approved: bool,
        reviewer_id: str,
        rationale: str,
    ) -> Dict[str, Any]:
        """Resolves an item in the human review queue."""
        for r in self._review_queue:
            if r["review_id"] == review_id:
                r["status"] = "APPROVED" if approved else "REJECTED"
                r["resolved_by"] = reviewer_id
                r["resolution_rationale"] = rationale
                r["resolved_at"] = datetime.now(timezone.utc).isoformat()
                return r
        raise ValueError(f"Review item {review_id} not found.")
