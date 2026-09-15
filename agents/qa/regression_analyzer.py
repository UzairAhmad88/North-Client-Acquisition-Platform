"""Regression Analyzer Engine for intelligent test suite selection."""

from typing import Any, Dict, List
from agents.qa.models import RegressionSelectionResult


class RegressionAnalyzerEngine:
    """Selects targeted regression test cases based on modified components or requirements."""

    def select_regression_suite(
        self,
        project_id: str,
        all_test_cases: List[Dict[str, Any]],
        changed_requirement_ids: List[str],
        changed_deliverable_ids: List[str],
    ) -> RegressionSelectionResult:
        """Filter test cases to form an optimized regression suite."""
        selected_ids: List[str] = []

        req_set = set(changed_requirement_ids)
        deliv_set = set(changed_deliverable_ids)

        for tc in all_test_cases:
            tc_id = tc.get("id")
            if not tc_id:
                continue

            is_reg = tc.get("is_regression", True)
            priority = tc.get("priority", "MEDIUM")
            tc_req = tc.get("requirement_id")
            tc_deliv = tc.get("deliverable_id")

            # Include if linked to changed requirement or deliverable
            if tc_req and tc_req in req_set:
                selected_ids.append(tc_id)
            elif tc_deliv and tc_deliv in deliv_set:
                selected_ids.append(tc_id)
            # Or if marked as CRITICAL / HIGH regression case
            elif is_reg and priority in ["CRITICAL", "HIGH"]:
                selected_ids.append(tc_id)

        # Fallback: if no criteria matched, select all marked regression cases
        if not selected_ids:
            selected_ids = [tc["id"] for tc in all_test_cases if tc.get("id") and tc.get("is_regression", True)]

        return RegressionSelectionResult(
            project_id=project_id,
            selected_test_case_ids=selected_ids,
            selection_reason=f"Selected {len(selected_ids)} test cases based on modified components and critical regression paths.",
            total_selected=len(selected_ids),
        )
