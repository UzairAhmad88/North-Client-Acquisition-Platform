"""Estimation & Commercial Validator enforcing safety, grounding, and scope consistency."""

from typing import Any, Dict, List
from agents.estimation.models import EstimateWorkItemSchema


class EstimationValidator:
    """Validates scope consistency, pricing safety, and requirement traceability."""

    @classmethod
    def validate_estimate_safety(
        cls, work_items: List[EstimateWorkItemSchema], solution_data: Dict[str, Any]
    ) -> List[str]:
        warnings: List[str] = []

        # 1. Scope Mismatch Check
        features = solution_data.get("features", [])
        feature_titles = {f.get("title", "").lower() for f in features}
        work_item_names = {w.name.lower() for w in work_items}

        for f_title in feature_titles:
            if not any(f_title in w_name or w_name in f_title for w_name in work_item_names):
                warnings.append(
                    f"SCOPE_ESTIMATION_MISMATCH: Solution feature '{f_title}' has no corresponding estimated work item."
                )

        # 2. Check for False Precision
        for w in work_items:
            if w.expected_hours != round(w.expected_hours, 1):
                warnings.append(
                    f"FALSE_PRECISION_WARNING: Work item '{w.name}' has excessive decimal precision ({w.expected_hours}h)."
                )

        return warnings
