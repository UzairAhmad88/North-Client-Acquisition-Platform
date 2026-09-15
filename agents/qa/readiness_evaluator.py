"""Release Readiness Gate Evaluator Engine."""

from typing import List
from agents.qa.models import ReleaseReadinessEvaluationResult


class ReadinessEvaluatorEngine:
    """Evaluates release readiness score and enforces deterministic quality gate rules."""

    def evaluate_readiness(
        self,
        project_id: str,
        version_tag: str,
        total_test_count: int,
        passed_test_count: int,
        failed_test_count: int,
        open_critical_defects: int,
        open_high_defects: int,
        uat_approved: bool,
    ) -> ReleaseReadinessEvaluationResult:
        """Calculate quality score (0-100) and enforce deterministic blocking gates."""
        blocking_conditions: List[str] = []
        recommendations: List[str] = []

        # 1. Deterministic Blocking Conditions
        if failed_test_count > 0:
            blocking_conditions.append(f"{failed_test_count} failing test(s) detected in execution run.")

        if open_critical_defects > 0:
            blocking_conditions.append(f"{open_critical_defects} open CRITICAL defect(s) unresolved.")

        if not uat_approved:
            blocking_conditions.append("Client User Acceptance Testing (UAT) signoff has not been granted.")

        # 2. Score Calculation
        if total_test_count > 0:
            test_pass_ratio = passed_test_count / total_test_count
        else:
            test_pass_ratio = 1.0

        # Base score starts from test pass ratio (max 70 pts)
        score = test_pass_ratio * 70.0

        # UAT approval contributes 20 pts
        if uat_approved:
            score += 20.0

        # Absence of high defects contributes 10 pts
        if open_high_defects == 0:
            score += 10.0
        else:
            score -= (open_high_defects * 5.0)

        readiness_score = max(0.0, min(100.0, round(score, 2)))

        # 3. Decision Rule: ANY blocking condition forces is_ready_for_release = False
        is_ready = (len(blocking_conditions) == 0) and (readiness_score >= 85.0)

        if is_ready:
            recommendations.append("Release gate passed. Ready for deployment and client handover.")
        else:
            if open_critical_defects > 0:
                recommendations.append("Resolve all CRITICAL defects before re-evaluating release readiness.")
            if failed_test_count > 0:
                recommendations.append("Fix failing test cases and re-run automated test suite.")
            if not uat_approved:
                recommendations.append("Obtain formal client UAT sign-off via client portal.")

        return ReleaseReadinessEvaluationResult(
            project_id=project_id,
            version_tag=version_tag,
            readiness_score=readiness_score,
            is_ready_for_release=is_ready,
            failing_test_count=failed_test_count,
            open_critical_defects=open_critical_defects,
            open_high_defects=open_high_defects,
            uat_approved=uat_approved,
            blocking_conditions=blocking_conditions,
            recommendations=recommendations,
        )
