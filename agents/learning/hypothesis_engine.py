"""Continuous Improvement Hypothesis and Experiment Engine."""

from typing import Any, Dict, List
from agents.learning.models import ExperimentDraft


class HypothesisEngine:
    """Manages continuous improvement hypotheses, trial metrics, and statistical evaluation."""

    def create_experiment_draft(
        self,
        title: str,
        hypothesis: str,
        target_workflow: str,
        target_metric: str,
        baseline_value: float,
        target_value: float,
        sample_target: int = 10,
    ) -> ExperimentDraft:
        """Create a formal structured experiment draft."""
        return ExperimentDraft(
            title=title,
            hypothesis=hypothesis,
            target_workflow=target_workflow,
            target_metric=target_metric,
            baseline_value=baseline_value,
            target_value=target_value,
            sample_target=max(5, sample_target),
        )

    def evaluate_experiment_results(
        self,
        experiment_meta: Dict[str, Any],
        results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Statistically evaluate trial results against experimental baseline and target."""
        sample_count = len(results)
        baseline = float(experiment_meta.get("baseline_value", 0.0))
        target = float(experiment_meta.get("target_value", 0.0))
        target_sample = int(experiment_meta.get("sample_target", 10))

        if sample_count < 5:
            return {
                "status": "INSUFFICIENT_DATA",
                "sample_count": sample_count,
                "target_sample": target_sample,
                "conclusion": f"Need at least 5 recorded trials (currently {sample_count}/{target_sample}) before evaluating hypothesis.",
            }

        observed_values = [float(r.get("observed_value", 0.0)) for r in results]
        mean_observed = sum(observed_values) / sample_count

        # Direction of improvement: if target < baseline (e.g. reducing errors/changes) vs target > baseline (e.g. response rate)
        improving_downward = target < baseline
        if improving_downward:
            progress_pct = ((baseline - mean_observed) / (baseline - target)) * 100 if baseline != target else 100.0
            is_success = mean_observed <= target
        else:
            progress_pct = ((mean_observed - baseline) / (target - baseline)) * 100 if target != baseline else 100.0
            is_success = mean_observed >= target

        conclusion = (
            f"Observed mean of {mean_observed:.2f} across {sample_count} trials vs baseline {baseline:.2f} "
            f"and target {target:.2f} ({progress_pct:.1f}% progress). "
            f"Hypothesis {'SUPPORTED by empirical data' if is_success else 'NOT FULLY SUPPORTED yet'}."
        )

        return {
            "status": "EVALUATED",
            "sample_count": sample_count,
            "target_sample": target_sample,
            "baseline_value": baseline,
            "target_value": target,
            "observed_mean": round(mean_observed, 2),
            "progress_pct": round(progress_pct, 1),
            "hypothesis_supported": is_success,
            "conclusion": conclusion,
        }
