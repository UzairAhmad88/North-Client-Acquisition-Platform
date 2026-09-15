"""Project blocker analyzer."""

from typing import Any, Dict, List


class ProjectBlockerAnalyzer:
    """Analyzes active task and milestone blockers."""

    def analyze_blockers(self, tasks: List[Dict[str, Any]], blockers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        active_blockers = [b for b in blockers if b.get("status") in ("OPEN", "IN_PROGRESS")]
        results = []

        for b in active_blockers:
            results.append({
                "blocker_id": b.get("id"),
                "title": b.get("title"),
                "severity": b.get("severity", "HIGH"),
                "task_id": b.get("task_id"),
                "recommendation": "Escalate to Project Manager for resource reallocation or client intervention.",
            })

        blocked_tasks = [t for t in tasks if t.get("status") == "BLOCKED" and not t.get("blocker_id")]
        for t in blocked_tasks:
            results.append({
                "task_id": t.get("id"),
                "title": f"Blocked Task: {t.get('name')}",
                "severity": "HIGH",
                "recommendation": f"Reason given: {t.get('blocked_reason') or 'Unspecified dependency constraint'}",
            })

        return results
