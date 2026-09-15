"""
Research Workspace and Question Decomposition Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.research_intelligence.base import (
    ResearchStatus,
    ResearchType,
)


class ResearchWorkspaceManager:
    """Manages research workspaces, question scoping, and sub-question task decomposition."""

    def __init__(self):
        self._workspaces: Dict[str, Dict[str, Any]] = {}
        self._tasks: Dict[str, List[Dict[str, Any]]] = {}

    def create_workspace(
        self,
        title: str,
        research_question: str,
        owner_id: str,
        research_type: ResearchType = ResearchType.MARKET,
        objective: Optional[str] = None,
        scope: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new bounded research workspace."""
        ws_id = f"rws_{uuid.uuid4().hex[:12]}"
        now = datetime.utcnow().isoformat()
        ws = {
            "id": ws_id,
            "title": title,
            "research_question": research_question,
            "objective": objective or f"Investigate and synthesize intelligence on: {title}",
            "research_type": research_type.value if hasattr(research_type, "value") else str(research_type),
            "status": ResearchStatus.PLANNED.value,
            "owner_id": owner_id,
            "scope": scope or {"geography": "GLOBAL", "time_range": "LAST_12_MONTHS"},
            "confidence_score": 0.85,
            "version": 1,
            "created_at": now,
            "updated_at": now,
        }
        self._workspaces[ws_id] = ws
        return ws

    def get_workspace(self, workspace_id: str) -> Optional[Dict[str, Any]]:
        return self._workspaces.get(workspace_id)

    def list_workspaces(
        self,
        status: Optional[str] = None,
        research_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        workspaces = list(self._workspaces.values())
        if status:
            workspaces = [w for w in workspaces if w["status"] == status]
        if research_type:
            workspaces = [w for w in workspaces if w["research_type"] == research_type]
        return workspaces

    def decompose_question(
        self,
        workspace_id: str,
        subquestions: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Decompose the core research question into prioritized, bounded tasks."""
        ws = self._workspaces.get(workspace_id)
        if not ws:
            raise ValueError(f"Workspace {workspace_id} not found")

        defaults = [
            f"Identify primary market demand & size for: {ws['research_question']}",
            f"Map key competitors and their product offerings",
            f"Analyze technology architecture & model requirements",
            f"Assess regulatory compliance & data privacy risks",
            f"Synthesize strategic opportunities and recommended next steps",
        ]
        questions = subquestions or defaults
        created_tasks = []

        for q in questions:
            task = {
                "id": f"rtask_{uuid.uuid4().hex[:12]}",
                "workspace_id": workspace_id,
                "question": q,
                "task_type": "SOURCE_DISCOVERY",
                "priority": "HIGH" if "demand" in q or "competitor" in q else "MEDIUM",
                "assigned_worker": "research_specialist_agent",
                "status": "QUEUED",
                "budget_tokens": 8000,
                "result_summary": None,
                "created_at": datetime.utcnow().isoformat(),
            }
            created_tasks.append(task)

        self._tasks[workspace_id] = created_tasks
        ws["status"] = ResearchStatus.RESEARCHING.value
        return created_tasks

    def create_task(
        self,
        workspace_id: str,
        question: str,
        task_type: str = "SUBQUESTION",
        priority: int = 1,
        assigned_worker: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create an explicit bounded research task."""
        task = {
            "id": f"rtask_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "question": question,
            "task_type": task_type,
            "priority": "HIGH" if priority == 1 else "MEDIUM",
            "assigned_worker": assigned_worker or "research_specialist_agent",
            "dependencies": dependencies or [],
            "status": "QUEUED",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._tasks.setdefault(workspace_id, []).append(task)
        return task

    def transition_status(
        self,
        workspace_id: str,
        target_status: ResearchStatus,
    ) -> Dict[str, Any]:
        """Transition workspace to next status in governed research lifecycle."""
        ws = self._workspaces.get(workspace_id)
        if not ws:
            raise ValueError(f"Workspace {workspace_id} not found")
        ws["status"] = target_status.value if hasattr(target_status, "value") else str(target_status)
        ws["version"] = ws.get("version", 1) + 1
        ws["updated_at"] = datetime.utcnow().isoformat()
        return ws

    def list_tasks(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._tasks.get(workspace_id, [])

