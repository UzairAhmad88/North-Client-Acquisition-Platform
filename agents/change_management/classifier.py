"""Classifier and triage engine for Change Requests."""

from typing import Any, Dict
from agents.change_management.models import ChangeClassificationResult


class ChangeClassifier:
    """Classifies incoming change requests into scope and technical buckets."""

    def classify_change(
        self, change_request_id: str, title: str, description: str, baseline_scope_items: list = None
    ) -> ChangeClassificationResult:
        content_lower = f"{title} {description}".lower()

        # Keywords
        out_of_scope_keywords = ["new mobile app", "additional module", "extra integration", "brand new feature", "build custom", "second portal"]
        defect_keywords = ["bug", "error", "broken", "does not work", "fix crash", "defect", "flaw"]
        clarification_keywords = ["how do we", "clarify", "explain", "meaning of", "details for"]
        content_keywords = ["copy change", "update text", "wording", "logo update"]

        if any(kw in content_lower for kw in out_of_scope_keywords):
            return ChangeClassificationResult(
                change_request_id=change_request_id,
                classification="OUT_OF_SCOPE",
                confidence_score=0.92,
                reasoning="Request specifies new major capabilities not present in committed baseline scope.",
                is_out_of_scope=True,
                suggested_action="PROCEED_TO_IMPACT_ANALYSIS",
            )
        elif any(kw in content_lower for kw in defect_keywords):
            return ChangeClassificationResult(
                change_request_id=change_request_id,
                classification="DEFECT",
                confidence_score=0.88,
                reasoning="Request specifies software bug or defect remediation.",
                is_out_of_scope=False,
                suggested_action="ROUTE_TO_BUG_TASK",
            )
        elif any(kw in content_lower for kw in clarification_keywords):
            return ChangeClassificationResult(
                change_request_id=change_request_id,
                classification="CLARIFICATION",
                confidence_score=0.85,
                reasoning="Request seeks clarification on existing baseline requirement.",
                is_out_of_scope=False,
                suggested_action="UPDATE_REQUIREMENT_SPEC",
            )
        elif any(kw in content_lower for kw in content_keywords):
            return ChangeClassificationResult(
                change_request_id=change_request_id,
                classification="IN_SCOPE",
                confidence_score=0.90,
                reasoning="Minor copy/content adjustment aligned with committed deliverables.",
                is_out_of_scope=False,
                suggested_action="EXECUTE_AS_IN_SCOPE_TASK",
            )
        else:
            return ChangeClassificationResult(
                change_request_id=change_request_id,
                classification="OUT_OF_SCOPE",
                confidence_score=0.80,
                reasoning="Unmatched scope item requiring formal impact and effort evaluation.",
                is_out_of_scope=True,
                suggested_action="PROCEED_TO_IMPACT_ANALYSIS",
            )
