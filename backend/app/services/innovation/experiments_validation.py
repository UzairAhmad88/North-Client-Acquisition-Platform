"""
Experiment Design, Statistical Analysis, Validation, and Structured Learning Manager.
"""

import math
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.innovation.base import (
    ExperimentType,
    ExperimentStatus,
    StatisticalOutcome,
)


class ExperimentValidationManager:
    """Manages empirical experiment execution, two-sample statistical tests, and learning generation."""

    def __init__(self):
        self._experiments: Dict[str, List[Dict[str, Any]]] = {}
        self._results: Dict[str, Dict[str, Any]] = {}
        self._learnings: Dict[str, List[Dict[str, Any]]] = {}

    def design_experiment(
        self,
        workspace_id: str,
        hypothesis_id: str,
        title: str,
        experiment_type: ExperimentType = ExperimentType.PROTOTYPE,
        objective: Optional[str] = None,
        target_population: Optional[str] = None,
        sample_size: int = 100,
        duration_days: int = 14,
        statistical_method: str = "TWO_SAMPLE_T_TEST",
    ) -> Dict[str, Any]:
        """Design a bounded empirical validation test with defined population and method."""
        exp_id = f"exp_{uuid.uuid4().hex[:12]}"
        exp = {
            "id": exp_id,
            "workspace_id": workspace_id,
            "hypothesis_id": hypothesis_id,
            "title": title,
            "experiment_type": experiment_type.value if hasattr(experiment_type, "value") else str(experiment_type),
            "objective": objective or f"Empirically validate hypothesis {hypothesis_id}",
            "target_population": target_population or "Verified Target ICP Users",
            "sample_size": sample_size,
            "duration_days": duration_days,
            "status": ExperimentStatus.DESIGNED.value,
            "risk_review_passed": True,
            "governance_approved": True,
            "statistical_method": statistical_method,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._experiments.setdefault(workspace_id, []).append(exp)
        return exp

    def list_experiments(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._experiments.get(workspace_id, [])

    def compute_statistical_test(
        self,
        control_values: List[float],
        treatment_values: List[float],
    ) -> Dict[str, Any]:
        """Compute two-sample means, relative delta, and approximated t-test p-value."""
        n_c = len(control_values)
        n_t = len(treatment_values)

        if n_c < 2 or n_t < 2:
            return {
                "observed_sample_size": n_c + n_t,
                "control_mean": float(sum(control_values) / n_c) if n_c > 0 else 0.0,
                "treatment_mean": float(sum(treatment_values) / n_t) if n_t > 0 else 0.0,
                "delta_percentage": 0.0,
                "p_value": None,
                "is_statistically_significant": False,
                "conclusion": StatisticalOutcome.INSUFFICIENT_DATA.value,
            }

        mean_c = sum(control_values) / n_c
        mean_t = sum(treatment_values) / n_t

        var_c = sum((x - mean_c) ** 2 for x in control_values) / (n_c - 1)
        var_t = sum((x - mean_t) ** 2 for x in treatment_values) / (n_t - 1)

        pooled_se = math.sqrt((var_c / n_c) + (var_t / n_t)) if (var_c + var_t) > 0 else 0.0001
        t_stat = (mean_t - mean_c) / pooled_se

        # Approximated p-value from t-stat (standard normal approximation for N >= 30)
        p_val = max(0.0001, min(1.0, 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_stat) / math.sqrt(2.0))))))
        is_sig = bool(p_val < 0.05)

        delta_pct = round(((mean_t - mean_c) / (mean_c if mean_c != 0 else 1.0)) * 100, 2)

        if is_sig and delta_pct > 0:
            conclusion = StatisticalOutcome.SUPPORTED.value
        elif is_sig and delta_pct < 0:
            conclusion = StatisticalOutcome.NOT_SUPPORTED.value
        elif not is_sig and abs(delta_pct) > 5.0:
            conclusion = StatisticalOutcome.PARTIALLY_SUPPORTED.value
        else:
            conclusion = StatisticalOutcome.INCONCLUSIVE.value

        return {
            "observed_sample_size": n_c + n_t,
            "control_mean": round(mean_c, 4),
            "treatment_mean": round(mean_t, 4),
            "delta_percentage": delta_pct,
            "p_value": round(p_val, 4),
            "is_statistically_significant": is_sig,
            "conclusion": conclusion,
        }

    def record_experiment_result(
        self,
        experiment_id: str,
        control_values: List[float],
        treatment_values: List[float],
        limitations: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record empirical observations and calculate statistical significance."""
        stats = self.compute_statistical_test(control_values, treatment_values)
        res_id = f"res_{uuid.uuid4().hex[:12]}"
        result = {
            "id": res_id,
            "experiment_id": experiment_id,
            "observed_sample_size": stats["observed_sample_size"],
            "control_mean": stats["control_mean"],
            "treatment_mean": stats["treatment_mean"],
            "delta_percentage": stats["delta_percentage"],
            "p_value": stats["p_value"],
            "is_statistically_significant": stats["is_statistically_significant"],
            "conclusion": stats["conclusion"],
            "limitations": limitations or "Standard test sample window.",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._results[experiment_id] = result
        return result

    def record_learning(
        self,
        workspace_id: str,
        insight_statement: str,
        evidence_summary: str,
        hypothesis_id: Optional[str] = None,
        experiment_id: Optional[str] = None,
        strategic_implication: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convert validated experiment result into durable organizational learning."""
        learn_id = f"lrn_{uuid.uuid4().hex[:12]}"
        learning = {
            "id": learn_id,
            "workspace_id": workspace_id,
            "hypothesis_id": hypothesis_id,
            "experiment_id": experiment_id,
            "insight_statement": insight_statement,
            "evidence_summary": evidence_summary,
            "strategic_implication": strategic_implication or "Incorporate into MVP scope.",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._learnings.setdefault(workspace_id, []).append(learning)
        return learning

    def list_learnings(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._learnings.get(workspace_id, [])
