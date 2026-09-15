"""
Hypothesis Formation and 2x2 Impact vs Uncertainty Assumption Mapping Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.innovation.base import HypothesisStatus


class HypothesisAssumptionManager:
    """Manages testable innovation hypotheses and prioritizes assumptions on impact vs uncertainty."""

    def __init__(self):
        self._hypotheses: Dict[str, List[Dict[str, Any]]] = {}
        self._assumptions: Dict[str, List[Dict[str, Any]]] = {}

    # Hypotheses
    def form_hypothesis(
        self,
        workspace_id: str,
        idea_id: str,
        statement: str,
        prediction: str,
        metric_name: str,
        baseline_value: float = 0.0,
        target_value: float = 0.20,
        confidence: float = 0.7,
    ) -> Dict[str, Any]:
        """Formulate explicit testable hypothesis with quantitative target and metric."""
        hyp_id = f"hyp_{uuid.uuid4().hex[:12]}"
        hyp = {
            "id": hyp_id,
            "workspace_id": workspace_id,
            "idea_id": idea_id,
            "statement": statement,
            "prediction": prediction,
            "metric_name": metric_name,
            "baseline_value": baseline_value,
            "target_value": target_value,
            "confidence": max(0.1, min(1.0, confidence)),
            "status": HypothesisStatus.DRAFTED.value,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._hypotheses.setdefault(workspace_id, []).append(hyp)
        return hyp

    def list_hypotheses(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._hypotheses.get(workspace_id, [])

    # Assumptions Mapping
    def map_assumption(
        self,
        hypothesis_id: str,
        assumption_text: str,
        category: str = "CUSTOMER",
        impact_level: str = "HIGH",
        uncertainty_level: str = "HIGH",
    ) -> Dict[str, Any]:
        """
        Map critical assumption into 2x2 priority matrix:
        - HIGH Impact / HIGH Uncertainty -> CRITICAL Priority
        - HIGH Impact / LOW Uncertainty -> HIGH Priority
        - LOW Impact / HIGH Uncertainty -> MEDIUM Priority
        - LOW Impact / LOW Uncertainty -> LOW Priority
        """
        imp = impact_level.upper()
        unc = uncertainty_level.upper()

        if imp == "HIGH" and unc == "HIGH":
            priority = "CRITICAL"
        elif imp == "HIGH" and unc == "LOW":
            priority = "HIGH"
        elif imp == "LOW" and unc == "HIGH":
            priority = "MEDIUM"
        else:
            priority = "LOW"

        asm_id = f"asm_{uuid.uuid4().hex[:12]}"
        assumption = {
            "id": asm_id,
            "hypothesis_id": hypothesis_id,
            "assumption_text": assumption_text,
            "category": category.upper(),
            "impact_level": imp,
            "uncertainty_level": unc,
            "validation_priority": priority,
            "is_validated": False,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._assumptions.setdefault(hypothesis_id, []).append(assumption)
        return assumption

    def list_assumptions(self, hypothesis_id: str) -> List[Dict[str, Any]]:
        return self._assumptions.get(hypothesis_id, [])

    def mark_assumption_validated(self, hypothesis_id: str, assumption_id: str) -> Dict[str, Any]:
        assumptions = self._assumptions.get(hypothesis_id, [])
        target = next((a for a in assumptions if a["id"] == assumption_id), None)
        if not target:
            raise ValueError(f"Assumption {assumption_id} not found")
        target["is_validated"] = True
        return target
