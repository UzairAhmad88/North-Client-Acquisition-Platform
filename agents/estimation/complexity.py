"""Deterministic Complexity Evaluator for project work items."""

from typing import Any, Dict, List


class ComplexityEvaluator:
    """Evaluates complexity ratings for work items and overall projects."""

    COMPLEXITY_RULES = {
        "WEBSITE": ("LOW", 8.0, 15.0, 25.0),
        "BOOKING": ("MEDIUM", 15.0, 25.0, 40.0),
        "PAYMENT": ("HIGH", 12.0, 20.0, 35.0),
        "AUTOMATION": ("MEDIUM", 10.0, 18.0, 30.0),
        "AI_FEATURE": ("VERY_HIGH", 20.0, 35.0, 60.0),
        "CRM": ("MEDIUM", 15.0, 24.0, 38.0),
        "DASHBOARD": ("MEDIUM", 12.0, 20.0, 32.0),
        "AUTHENTICATION": ("MEDIUM", 8.0, 14.0, 22.0),
    }

    @classmethod
    def evaluate_feature_complexity(
        cls, category: str
    ) -> tuple[str, float, float, float]:
        cat_upper = category.upper()
        if cat_upper in cls.COMPLEXITY_RULES:
            return cls.COMPLEXITY_RULES[cat_upper]
        return ("MEDIUM", 10.0, 18.0, 28.0)

    @classmethod
    def evaluate_overall_complexity(cls, total_hours: float, feature_count: int) -> str:
        if total_hours >= 120 or feature_count >= 6:
            return "HIGH"
        elif total_hours >= 60 or feature_count >= 3:
            return "MEDIUM"
        return "LOW"
