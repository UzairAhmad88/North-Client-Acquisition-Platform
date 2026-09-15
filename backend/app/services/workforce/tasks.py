"""
AI Task Engine & DAG Decomposition Subsystem for Phase 52.
Decomposes high-level business objectives into structured dependency graphs (DAG) with explicit topological ordering.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

try:
    from backend.app.services.workforce.base import AIWorkTask, SupervisionLevel, TaskPriority, TaskStatus
except ImportError:
    from app.services.workforce.base import AIWorkTask, SupervisionLevel, TaskPriority, TaskStatus

logger = logging.getLogger(__name__)


class TaskGraphEngine:
    """
    Constructs and decomposes objectives into structured Task Directed Acyclic Graphs (DAG).
    Performs cycle detection and topological scheduling.
    """

    def decompose_objective(
        self,
        objective: str,
        domain: str = "GROWTH_EXPANSION",
        organization_id: str = "default_org",
    ) -> List[AIWorkTask]:
        """Decomposes a business goal into a sequence of dependent specialized tasks."""
        tasks: List[AIWorkTask] = []

        if domain == "GROWTH_EXPANSION" or "market" in objective.lower() or "lead" in objective.lower():
            # Standard Sales & Expansion Pipeline
            t1 = AIWorkTask(
                objective=f"Research target accounts for: {objective}",
                description="Gather digital presence, technological stack, and key company signals.",
                priority=TaskPriority.HIGH,
                supervision_level=SupervisionLevel.READ_ONLY_1,
                risk_level="LOW",
                inputs={"query": objective},
                expected_output="Structured research artifact with verified URLs and findings.",
            )
            t2 = AIWorkTask(
                parent_task_code=t1.task_code,
                objective=f"Qualify researched leads against ICP",
                description="Evaluate fit, budget indicators, and risk score.",
                priority=TaskPriority.HIGH,
                supervision_level=SupervisionLevel.DRAFT_GEN_2,
                risk_level="LOW",
                inputs={"parent_ref": t1.task_code},
                dependencies=[t1.task_code],
                expected_output="Qualification scores and service recommendations.",
            )
            t3 = AIWorkTask(
                parent_task_code=t2.task_code,
                objective=f"Generate personalized multi-channel outreach drafts",
                description="Synthesize verified findings into tailored communication drafts.",
                priority=TaskPriority.HIGH,
                supervision_level=SupervisionLevel.REVIEW_REQUIRED_4,
                risk_level="MEDIUM",
                inputs={"parent_ref": t2.task_code},
                dependencies=[t2.task_code],
                expected_output="Outreach draft ready for human ratification queue.",
            )
            tasks.extend([t1, t2, t3])
        else:
            # Generic 2-stage analysis & proposal decomposition
            t1 = AIWorkTask(
                objective=f"Perform foundational analysis for: {objective}",
                description="Extract context, evaluate historical telemetry and identify bottlenecks.",
                priority=TaskPriority.MEDIUM,
                supervision_level=SupervisionLevel.READ_ONLY_1,
                inputs={"objective": objective},
            )
            t2 = AIWorkTask(
                parent_task_code=t1.task_code,
                objective=f"Formulate recommendations and draft plan",
                description="Structure bounded action items with evidence and risk assessment.",
                priority=TaskPriority.HIGH,
                supervision_level=SupervisionLevel.REVIEW_REQUIRED_4,
                dependencies=[t1.task_code],
            )
            tasks.extend([t1, t2])

        return tasks

    def validate_task_dag(self, tasks: List[AIWorkTask]) -> Tuple[bool, Optional[str]]:
        """Verifies no cycles exist in task graph dependencies."""
        adj: Dict[str, List[str]] = {t.task_code: [] for t in tasks}
        in_degree: Dict[str, int] = {t.task_code: 0 for t in tasks}

        for t in tasks:
            for dep in t.dependencies:
                if dep in adj:
                    adj[dep].append(t.task_code)
                    in_degree[t.task_code] += 1

        queue = [k for k, v in in_degree.items() if v == 0]
        visited_count = 0

        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for nxt in adj.get(curr, []):
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    queue.append(nxt)

        if visited_count != len(tasks):
            return False, "Circular dependency detected in task graph."
        return True, None


class TaskManager:
    """Manages AI task lifecycle, status transitions, and execution result logging."""

    def __init__(self):
        self._tasks: Dict[str, AIWorkTask] = {}

    def create_task(self, task: AIWorkTask) -> AIWorkTask:
        self._tasks[task.task_code] = task
        return task

    def get_task(self, task_code: str) -> Optional[AIWorkTask]:
        return self._tasks.get(task_code)

    def list_tasks(
        self,
        worker_code: Optional[str] = None,
        status: Optional[TaskStatus] = None,
    ) -> List[AIWorkTask]:
        res = list(self._tasks.values())
        if worker_code:
            res = [t for t in res if t.worker_code == worker_code]
        if status:
            res = [t for t in res if t.status == status]
        return res

    def update_task_status(
        self,
        task_code: str,
        status: TaskStatus,
        result_summary: Optional[str] = None,
        artifacts: Optional[List[Dict[str, Any]]] = None,
        error_message: Optional[str] = None,
    ) -> AIWorkTask:
        task = self._tasks.get(task_code)
        if not task:
            raise ValueError(f"Task {task_code} not found.")

        task.status = status
        if result_summary:
            task.result_summary = result_summary
        if artifacts:
            task.result_artifacts = artifacts
        if error_message:
            task.error_message = error_message

        if status == TaskStatus.RUNNING and not task.started_at:
            task.started_at = datetime.now(timezone.utc)
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            task.completed_at = datetime.now(timezone.utc)

        return task
