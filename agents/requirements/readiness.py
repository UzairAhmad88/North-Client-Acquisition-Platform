"""Requirements Readiness Evaluator computing readiness and completeness scores."""

from typing import List
from agents.requirements.models import ExtractedRequirementSchema, ReadinessEvaluationSchema, ScopeItemSchema


class ReadinessEvaluator:
    """Evaluates readiness stage, completeness score, and complexity tier."""

    @classmethod
    def evaluate(
        cls,
        requirements: List[ExtractedRequirementSchema],
        scope_items: List[ScopeItemSchema],
        questions_count: int,
        message_body: str,
    ) -> ReadinessEvaluationSchema:
        if not requirements:
            return ReadinessEvaluationSchema(
                readiness_stage="NOT_READY",
                readiness_score=0.0,
                completeness_score=0.0,
                scope_complexity="UNKNOWN",
                missing_critical_areas=["Requirements list empty"],
            )

        # 1. Calculate Completeness Score
        categories = {req.category for req in requirements}
        total_expected_areas = 5  # Core categories for a typical project
        present_areas = len(categories)
        completeness = min(100.0, round((present_areas / total_expected_areas) * 100, 1))

        # 2. Calculate Readiness Score
        confirmed_count = sum(1 for req in requirements if req.status == "CONFIRMED")
        explicit_count = sum(1 for req in requirements if req.explicit)
        readiness_score = min(
            100.0,
            round(
                (explicit_count * 20) + (confirmed_count * 30) + (completeness * 0.5) - (questions_count * 10),
                1,
            ),
        )
        readiness_score = max(0.0, readiness_score)

        # 3. Readiness Stage Determination
        stage = "NOT_READY"
        if readiness_score >= 80 and confirmed_count > 0:
            stage = "READY_FOR_NEXT_STAGE"
        elif readiness_score >= 60:
            stage = "READY_FOR_REVIEW"
        elif readiness_score >= 30:
            stage = "PARTIALLY_READY"

        # 4. Scope Complexity Tier
        complexity = "LOW"
        if len(requirements) >= 5 or any(c in categories for c in ("AI_FEATURE", "MOBILE", "CRM", "INVENTORY")):
            complexity = "HIGH"
        elif len(requirements) >= 3 or "PAYMENT" in categories:
            complexity = "MEDIUM"

        # 5. Missing Critical Areas
        missing = []
        if "WEBSITE" not in categories and "BOOKING" not in categories:
            missing.append("Project Type / Core Deliverable")
        if "budget" not in message_body.lower():
            missing.append("Target Budget")
        if "timeline" not in message_body.lower():
            missing.append("Target Timeline")

        return ReadinessEvaluationSchema(
            readiness_stage=stage,
            readiness_score=readiness_score,
            completeness_score=completeness,
            scope_complexity=complexity,
            missing_critical_areas=missing,
        )
