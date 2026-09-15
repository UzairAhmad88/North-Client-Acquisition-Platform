"""Project delivery risk analyzer."""

from typing import Any, Dict, List


class ProjectRiskAnalyzer:
    """Analyzes execution risks, overdue trends, and probability/impact matrices."""

    def analyze_risks(
        self,
        tasks: List[Dict[str, Any]],
        milestones: List[Dict[str, Any]],
        client_dependencies: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        identified_risks: List[Dict[str, Any]] = []

        # 1. Overdue Tasks Risk
        overdue = [t for t in tasks if t.get("status") in ("TODO", "IN_PROGRESS") and t.get("is_overdue")]
        if len(overdue) >= 3:
            identified_risks.append({
                "title": "Multiple Overdue Tasks Threatening Schedule",
                "description": f"{len(overdue)} tasks are currently past their planned end date.",
                "probability": "HIGH",
                "impact": "HIGH",
                "severity": "HIGH",
                "mitigation_plan": "Reassign tasks or re-evaluate task scope with Project Manager.",
            })

        # 2. Overdue Client Dependencies Risk
        overdue_client_deps = [c for c in client_dependencies if c.get("status") == "OVERDUE"]
        if overdue_client_deps:
            identified_risks.append({
                "title": "Unfulfilled Client Dependencies",
                "description": f"{len(overdue_client_deps)} requested client inputs are overdue.",
                "probability": "HIGH",
                "impact": "CRITICAL",
                "severity": "CRITICAL",
                "mitigation_plan": "Issue formal client dependency alert via account manager.",
            })

        # 3. Missed Milestones Risk
        missed = [m for m in milestones if m.get("status") == "MISSED"]
        if missed:
            identified_risks.append({
                "title": "Missed Milestone Target",
                "description": f"{len(missed)} delivery milestones have passed target completion dates.",
                "probability": "HIGH",
                "impact": "CRITICAL",
                "severity": "CRITICAL",
                "mitigation_plan": "Re-baseline internal schedule and submit change log for review.",
            })

        return identified_risks
