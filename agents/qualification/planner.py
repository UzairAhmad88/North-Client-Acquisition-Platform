"""Qualification Planner evaluating upstream data completeness across Research, Audit, Score, and CRM."""

from typing import Any, Dict, List, Tuple


class QualificationPlanner:
    """Evaluates availability and completeness of upstream intelligence systems."""

    @staticmethod
    def evaluate_upstream_completeness(
        research_data: Dict[str, Any],
        audit_data: Dict[str, Any],
        score_data: Dict[str, Any],
        recommended_services: List[Dict[str, Any]],
    ) -> Tuple[bool, List[str]]:
        missing_upstream = []

        has_research = bool(research_data.get("records"))
        if not has_research:
            missing_upstream.append("Research Intelligence Profile")

        has_audit = bool(audit_data.get("audit") or audit_data.get("findings"))
        if not has_audit:
            missing_upstream.append("Website Digital Presence Audit")

        has_score = bool(score_data.get("score") is not None)
        if not has_score:
            missing_upstream.append("Deterministic Lead Opportunity Score")

        has_recs = len(recommended_services) > 0
        if not has_recs:
            missing_upstream.append("Service Recommendations")

        # Sufficient if at least Score + (Research OR Audit) exist
        is_sufficient = has_score and (has_research or has_audit)
        return is_sufficient, missing_upstream
