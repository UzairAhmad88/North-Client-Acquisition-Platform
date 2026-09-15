"""
Assumptions, Unknowns, Hypotheses, Options, Multi-Criteria Decision Matrix, and Trade-off Engine.
"""

import uuid
from typing import Dict, Any, List, Optional


class AssumptionOptionManager:
    """Manages assumptions, unknowns, candidate options, decision matrices, and trade-off analysis."""

    def __init__(self):
        self._assumptions: Dict[str, List[Dict[str, Any]]] = {}
        self._unknowns: Dict[str, List[Dict[str, Any]]] = {}
        self._hypotheses: Dict[str, List[Dict[str, Any]]] = {}
        self._options: Dict[str, List[Dict[str, Any]]] = {}
        self._criteria: Dict[str, List[Dict[str, Any]]] = {}
        self._scores: Dict[str, List[Dict[str, Any]]] = {}  # room_id -> list of scores
        self._tradeoffs: Dict[str, List[Dict[str, Any]]] = {}

    # Assumptions & Unknowns
    def add_assumption(
        self,
        room_id: str,
        statement: str,
        confidence: float = 0.7,
        impact_if_false: str = "MEDIUM",
    ) -> Dict[str, Any]:
        item = {
            "id": f"asmp_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "statement": statement,
            "confidence": confidence,
            "validated": False,
            "validator_role": None,
            "impact_if_false": impact_if_false,
        }
        self._assumptions.setdefault(room_id, []).append(item)
        return item

    def list_assumptions(self, room_id: str) -> List[Dict[str, Any]]:
        return self._assumptions.get(room_id, [])

    def add_unknown(
        self,
        room_id: str,
        question: str,
        impact: str = "MEDIUM",
        resolution_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        item = {
            "id": f"unkn_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "question": question,
            "impact": impact,
            "resolution_path": resolution_path,
            "resolved": False,
            "resolved_value": None,
        }
        self._unknowns.setdefault(room_id, []).append(item)
        return item

    def list_unknowns(self, room_id: str) -> List[Dict[str, Any]]:
        return self._unknowns.get(room_id, [])

    # Options & Alternatives
    def create_option(
        self,
        room_id: str,
        name: str,
        description: str,
        benefits: Optional[List[str]] = None,
        costs: float = 0.0,
        risks: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None,
        resources_required: Optional[List[str]] = None,
        expected_outcome: Optional[str] = None,
        uncertainty_level: str = "MEDIUM",
        reversibility: str = "REVERSIBLE",
    ) -> Dict[str, Any]:
        option = {
            "id": f"opt_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "name": name,
            "description": description,
            "benefits": benefits or [],
            "costs": costs,
            "risks": risks or [],
            "dependencies": dependencies or [],
            "resources_required": resources_required or [],
            "expected_outcome": expected_outcome,
            "uncertainty_level": uncertainty_level,
            "reversibility": reversibility,
            "composite_score": 0.0,
            "version": 1,
        }
        self._options.setdefault(room_id, []).append(option)
        return option

    def list_options(self, room_id: str) -> List[Dict[str, Any]]:
        return self._options.get(room_id, [])

    # Decision Matrix Criteria & Scoring
    def add_criterion(
        self,
        room_id: str,
        name: str,
        weight: float = 1.0,
        criterion_type: str = "BENEFIT",
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        crit = {
            "id": f"crit_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "name": name,
            "weight": max(0.1, weight),
            "criterion_type": criterion_type,
            "description": description,
        }
        self._criteria.setdefault(room_id, []).append(crit)
        return crit

    def list_criteria(self, room_id: str) -> List[Dict[str, Any]]:
        return self._criteria.get(room_id, [])

    def score_option(
        self,
        room_id: str,
        option_id: str,
        criterion_id: str,
        raw_score: float,
        justification: Optional[str] = None,
        scored_by: str = "AI_ANALYST",
    ) -> Dict[str, Any]:
        """Score an option against a specific criterion."""
        criteria = self.list_criteria(room_id)
        crit = next((c for c in criteria if c["id"] == criterion_id), None)
        weight = crit["weight"] if crit else 1.0

        clamped_raw = max(0.0, min(100.0, raw_score))
        weighted_score = round(clamped_raw * weight, 2)

        score_entry = {
            "id": f"sc_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "option_id": option_id,
            "criterion_id": criterion_id,
            "raw_score": clamped_raw,
            "weighted_score": weighted_score,
            "justification": justification,
            "scored_by": scored_by,
        }

        # Update or add score
        room_scores = self._scores.setdefault(room_id, [])
        existing = next((s for s in room_scores if s["option_id"] == option_id and s["criterion_id"] == criterion_id), None)
        if existing:
            existing.update(score_entry)
            score_entry = existing
        else:
            room_scores.append(score_entry)

        self._recalculate_option_composite_scores(room_id)
        return score_entry

    def _recalculate_option_composite_scores(self, room_id: str):
        """Compute normalized composite score across all criteria."""
        options = self.list_options(room_id)
        criteria = self.list_criteria(room_id)
        scores = self._scores.get(room_id, [])
        total_weight = sum(c["weight"] for c in criteria) or 1.0

        for opt in options:
            opt_scores = [s for s in scores if s["option_id"] == opt["id"]]
            sum_weighted = sum(s["weighted_score"] for s in opt_scores)
            opt["composite_score"] = round(sum_weighted / total_weight, 2)

    def generate_tradeoff(
        self,
        room_id: str,
        option_a_id: str,
        option_b_id: str,
    ) -> Dict[str, Any]:
        """Generate explicit trade-off analysis between two candidate options."""
        options = self.list_options(room_id)
        opt_a = next((o for o in options if o["id"] == option_a_id), None)
        opt_b = next((o for o in options if o["id"] == option_b_id), None)

        if not opt_a or not opt_b:
            raise ValueError("Both options must exist to evaluate trade-offs")

        gains_in_a = [b for b in opt_a.get("benefits", []) if b not in opt_b.get("benefits", [])]
        sacrifices_in_a = [b for b in opt_b.get("benefits", []) if b not in opt_a.get("benefits", [])]
        if opt_a.get("costs", 0) > opt_b.get("costs", 0):
            sacrifices_in_a.append(f"Higher cost: ${opt_a.get('costs')} vs ${opt_b.get('costs')}")
        else:
            gains_in_a.append(f"Cost savings: ${opt_b.get('costs') - opt_a.get('costs'):,.2f}")

        summary = (
            f"Choosing '{opt_a['name']}' over '{opt_b['name']}' prioritizes "
            f"{', '.join(gains_in_a[:2]) if gains_in_a else 'specific benefits'} "
            f"while accepting trade-offs in {', '.join(sacrifices_in_a[:2]) if sacrifices_in_a else 'alternate benefits'}."
        )

        tradeoff = {
            "id": f"to_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "option_a_id": option_a_id,
            "option_b_id": option_b_id,
            "tradeoff_summary": summary,
            "gains_in_a": gains_in_a,
            "sacrifices_in_a": sacrifices_in_a,
        }
        self._tradeoffs.setdefault(room_id, []).append(tradeoff)
        return tradeoff

    def list_tradeoffs(self, room_id: str) -> List[Dict[str, Any]]:
        return self._tradeoffs.get(room_id, [])
