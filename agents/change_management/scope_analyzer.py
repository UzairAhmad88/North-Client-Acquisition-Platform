"""Scope Analyzer for Change Requests."""

from typing import Any, Dict, List
from agents.change_management.models import ChangeClassificationResult


class ChangeScopeAnalyzer:
    """Evaluates scope delta against committed baseline items."""

    def compare_scope(
        self, change_request_id: str, title: str, description: str, baseline_deliverables: List[str]
    ) -> Dict[str, Any]:
        title_lower = title.lower()

        matched_deliverable = None
        for deliv in baseline_deliverables:
            if deliv.lower() in title_lower:
                matched_deliverable = deliv
                break

        is_delta = matched_deliverable is None

        return {
            "change_request_id": change_request_id,
            "matched_baseline_deliverable": matched_deliverable,
            "is_scope_delta": is_delta,
            "scope_action": "NEW_DELIVERABLE_SCOPE" if is_delta else "IN_SCOPE_REFINEMENT",
        }
