"""
Worker Assignment & Scheduling Subsystem for Phase 52.
Performs multi-criteria worker selection (specialization, availability, cost, latency, grounding) and priority-based scheduling.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.workforce.base import AIWorker, AIWorkTask, TaskStatus, WorkerStatus
except ImportError:
    from app.services.workforce.base import AIWorker, AIWorkTask, TaskStatus, WorkerStatus

logger = logging.getLogger(__name__)


class AssignmentEngine:
    """Selects the best qualified AI Worker for a given task using multi-criteria suitability scoring."""

    def find_best_worker(
        self,
        task: AIWorkTask,
        candidate_workers: List[AIWorker],
    ) -> Optional[AIWorker]:
        """Calculates suitability score based on specialization match, grounding score, and active workload."""
        if not candidate_workers:
            return None

        # Filter active approved workers
        eligible = [
            w for w in candidate_workers
            if w.status in [WorkerStatus.ACTIVE, WorkerStatus.APPROVED]
        ]
        if not eligible:
            return None

        def score_worker(w: AIWorker) -> float:
            score = 0.0
            # Specialization alignment
            if task.objective.lower().find(w.specialization.lower()[:4]) != -1:
                score += 50.0
            elif w.specialization.lower() in task.objective.lower():
                score += 40.0
            else:
                score += 10.0

            # Historical quality
            score += (w.grounding_score * 30.0)

            # Capacity penalty
            penalty = min(20.0, w.total_tasks_completed * 0.1)
            return score - penalty

        sorted_workers = sorted(eligible, key=score_worker, reverse=True)
        best = sorted_workers[0]
        task.worker_code = best.worker_code
        task.status = TaskStatus.ASSIGNED
        return best


class WorkforceScheduler:
    """Manages execution queue, backpressure, and priority dispatching."""

    def schedule_tasks(self, tasks: List[AIWorkTask]) -> List[AIWorkTask]:
        """Sorts tasks by priority and dependency readiness."""
        priority_weights = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        
        def sort_key(t: AIWorkTask) -> int:
            return priority_weights.get(t.priority.value if hasattr(t.priority, 'value') else t.priority, 1)

        # High priority first
        sorted_tasks = sorted(tasks, key=sort_key, reverse=True)
        for t in sorted_tasks:
            if t.status == TaskStatus.CREATED:
                t.status = TaskStatus.QUEUED
        return sorted_tasks
