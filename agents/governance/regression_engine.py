"""AI Regression Testing & Version Comparison Engine."""

from typing import Any, Dict, List, Optional
from agents.governance.evaluator import AIEvaluationEngine
from agents.governance.models import EvaluationBenchmarkResult


class AIRegressionEngine:
    """Detects performance or safety regressions when evaluating candidate prompts and models against golden test suites."""

    # Configurable regression degradation thresholds
    DEFAULT_MAX_ALLOWED_DEGRADATION_PCT = 5.0
    DEFAULT_MAX_ALLOWED_SAFETY_DROP = 0.0

    def __init__(self):
        self.evaluator = AIEvaluationEngine()

    def compare_versions(
        self,
        baseline_score: float,
        candidate_score: float,
        max_allowed_degradation_pct: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Compare candidate benchmark performance against approved baseline."""
        threshold = (
            max_allowed_degradation_pct
            if max_allowed_degradation_pct is not None
            else self.DEFAULT_MAX_ALLOWED_DEGRADATION_PCT
        )
        score_diff = round(candidate_score - baseline_score, 2)
        degradation = round(baseline_score - candidate_score, 2) if candidate_score < baseline_score else 0.0
        regression_detected = degradation > threshold

        return {
            "baseline_score": baseline_score,
            "candidate_score": candidate_score,
            "score_diff": score_diff,
            "degradation": degradation,
            "threshold": threshold,
            "regression_detected": regression_detected,
            "promotion_allowed": not regression_detected,
            "recommendation": "BLOCK_PROMOTION" if regression_detected else "ALLOW_PROMOTION",
        }

    def execute_golden_suite_benchmark(
        self,
        agent_key: str,
        agent_version: str,
        prompt_version: str,
        model_version: str,
        cases: List[Dict[str, Any]],
        baseline_score: float = 90.0,
    ) -> EvaluationBenchmarkResult:
        """Run benchmark on golden cases and return structured evaluation result."""
        total_score = 0.0
        passed_count = 0
        failed_count = 0

        for case in cases:
            output = case.get("output") or {}
            req_fields = case.get("required_fields") or ["status"]
            ev_context = case.get("evidence_context") or {}
            eval_res = self.evaluator.run_comprehensive_evaluation(output, req_fields, ev_context)
            total_score += eval_res["overall_score"]
            if eval_res["passed"]:
                passed_count += 1
            else:
                failed_count += 1

        overall_score = round(total_score / max(1, len(cases)), 1) if cases else 100.0
        comparison = self.compare_versions(baseline_score, overall_score)

        return EvaluationBenchmarkResult(
            agent_key=agent_key,
            agent_version=agent_version,
            prompt_version=prompt_version,
            model_version=model_version,
            overall_score=overall_score,
            passed_cases_count=passed_count,
            failed_cases_count=failed_count,
            regression_detected=comparison["regression_detected"],
            regression_details=comparison,
        )
