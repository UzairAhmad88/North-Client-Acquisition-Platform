"""Role-Based Effort Allocation Engine."""

from typing import Dict, List
from agents.estimation.models import EstimateWorkItemSchema


class RoleEffortDistributor:
    """Distributes estimated work item hours across team roles."""

    CATEGORY_ROLE_WEIGHTS = {
        "FRONTEND": {"FRONTEND_DEVELOPER": 0.70, "UI_UX_DESIGNER": 0.20, "QA_ENGINEER": 0.10},
        "BACKEND": {"BACKEND_DEVELOPER": 0.75, "QA_ENGINEER": 0.15, "DEVOPS_ENGINEER": 0.10},
        "DESIGN": {"UI_UX_DESIGNER": 0.85, "FRONTEND_DEVELOPER": 0.15},
        "DATABASE": {"BACKEND_DEVELOPER": 0.80, "DEVOPS_ENGINEER": 0.20},
        "API": {"BACKEND_DEVELOPER": 0.80, "QA_ENGINEER": 0.20},
        "INTEGRATION": {"BACKEND_DEVELOPER": 0.70, "QA_ENGINEER": 0.20, "DEVOPS_ENGINEER": 0.10},
        "AI": {"AI_ENGINEER": 0.75, "BACKEND_DEVELOPER": 0.15, "QA_ENGINEER": 0.10},
        "TESTING": {"QA_ENGINEER": 0.90, "FRONTEND_DEVELOPER": 0.10},
        "DEVOPS": {"DEVOPS_ENGINEER": 0.90, "BACKEND_DEVELOPER": 0.10},
    }

    @classmethod
    def distribute_hours(
        cls, work_items: List[EstimateWorkItemSchema]
    ) -> Dict[str, float]:
        role_totals: Dict[str, float] = {}

        for item in work_items:
            cat = item.category.upper()
            weights = cls.CATEGORY_ROLE_WEIGHTS.get(
                cat, {"BACKEND_DEVELOPER": 0.50, "FRONTEND_DEVELOPER": 0.30, "QA_ENGINEER": 0.20}
            )
            item_hours = item.expected_hours

            for role, weight in weights.items():
                role_totals[role] = round(role_totals.get(role, 0.0) + (item_hours * weight), 1)

        return role_totals
