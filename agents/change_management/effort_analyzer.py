"""Effort Analyzer using PERT 3-Point re-estimation methodology."""

from typing import Any, Dict, List
from agents.change_management.models import ChangeEffortEstimate


class ChangeEffortAnalyzer:
    """Calculates PERT three-point effort re-estimations for change proposals."""

    def calculate_effort(
        self, change_request_id: str, title: str, description: str
    ) -> ChangeEffortEstimate:
        content_lower = f"{title} {description}".lower()

        # Heuristic estimation base
        if "mobile app" in content_lower:
            o, m, p = 80.0, 120.0, 180.0
        elif "integration" in content_lower or "gateway" in content_lower:
            o, m, p = 20.0, 40.0, 70.0
        elif "dashboard" in content_lower or "page" in content_lower:
            o, m, p = 16.0, 30.0, 50.0
        else:
            o, m, p = 8.0, 16.0, 32.0

        expected = (o + (4.0 * m) + p) / 6.0

        return ChangeEffortEstimate(
            change_request_id=change_request_id,
            optimistic_hours=o,
            most_likely_hours=m,
            pessimistic_hours=p,
            expected_hours=round(expected, 2),
            confidence=0.85,
            assumptions=[
                "Effort derived using PERT 3-point estimation (O + 4M + P)/6.",
                "Assumes standard engineering velocity and role availability.",
            ],
        )
