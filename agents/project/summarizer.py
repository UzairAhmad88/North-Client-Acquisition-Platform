"""Project status summarizer engine."""

from typing import Any, Dict, List
from agents.project.models import ProjectStatusSummaryResult


class ProjectSummarizerEngine:
    """Generates human-readable executive status summaries and activity rollups."""

    def summarize_project(
        self,
        project_data: Dict[str, Any],
        tasks: List[Dict[str, Any]],
        milestones: List[Dict[str, Any]],
        blockers: List[Dict[str, Any]],
        risks: List[Dict[str, Any]],
        client_dependencies: List[Dict[str, Any]],
    ) -> ProjectStatusSummaryResult:
        project_id = str(project_data.get("id") or "")
        name = str(project_data.get("name") or "Project")
        status = str(project_data.get("status") or "IN_PROGRESS")
        health = str(project_data.get("health") or "HEALTHY")
        progress = float(project_data.get("progress_percent") or 0.0)

        completed_tasks = [t for t in tasks if t.get("status") == "COMPLETED"]
        overdue_tasks = [t for t in tasks if t.get("status") in ("TODO", "IN_PROGRESS") and t.get("is_overdue")]
        active_blockers_list = [b.get("title") or "Active blocker" for b in blockers if b.get("status") in ("OPEN", "IN_PROGRESS")]
        risk_list = [r.get("title") or "Identified risk" for r in risks if r.get("status") != "CLOSED"]
        pending_client_deps = [c.get("title") or "Client input" for c in client_dependencies if c.get("status") in ("REQUESTED", "OVERDUE")]

        achievements = [f"Completed {len(completed_tasks)} out of {len(tasks)} tasks ({progress:.1f}% overall progress)."]
        if milestones:
            completed_m = [m for m in milestones if m.get("status") == "COMPLETED"]
            achievements.append(f"Achieved {len(completed_m)} out of {len(milestones)} milestones.")

        overdue_items = [t.get("name") or "Overdue task" for t in overdue_tasks]

        next_actions = []
        if active_blockers_list:
            next_actions.append(f"Resolve active blocker: {active_blockers_list[0]}")
        if pending_client_deps:
            next_actions.append(f"Follow up on client dependency: {pending_client_deps[0]}")
        if not next_actions:
            next_actions.append("Proceed with next planned engineering tasks in queue.")

        summary_text = (
            f"Project '{name}' is currently {status} with a health status of {health}. "
            f"Overall progress stands at {progress:.1f}%. There are {len(active_blockers_list)} active blockers "
            f"and {len(pending_client_deps)} pending client dependencies."
        )

        return ProjectStatusSummaryResult(
            project_id=project_id,
            status=status,
            health=health,
            progress_percent=progress,
            executive_summary=summary_text,
            key_achievements=achievements,
            active_blockers=active_blockers_list,
            risks=risk_list,
            overdue_items=overdue_items,
            recommended_next_actions=next_actions,
        )
