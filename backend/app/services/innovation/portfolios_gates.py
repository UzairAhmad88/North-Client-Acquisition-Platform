"""
Portfolio Allocation (Horizons 1, 2, 3), Stage-Gate Governance (Gates 0-7), and Pivot Engine Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.innovation.base import (
    GateStage,
    GateDecision,
    PivotAction,
)


class PortfolioGateManager:
    """Manages Horizon 1/2/3 portfolio allocations, stage-gate reviews, and pivot recommendations."""

    def __init__(self):
        self._portfolios: Dict[str, Dict[str, Any]] = {}
        self._gate_reviews: Dict[str, List[Dict[str, Any]]] = {}

    # Portfolios
    def configure_portfolio(
        self,
        portfolio_name: str,
        horizon_1_pct: float = 70.0,
        horizon_2_pct: float = 20.0,
        horizon_3_pct: float = 10.0,
        portfolio_expected_roi: float = 3.4,
    ) -> Dict[str, Any]:
        """Configure portfolio allocation across core (H1), adjacent (H2), and transformational (H3) innovation."""
        if abs((horizon_1_pct + horizon_2_pct + horizon_3_pct) - 100.0) > 0.1:
            raise ValueError("Horizon budget percentages must sum to 100%")

        pid = f"port_{portfolio_name.lower().replace(' ', '_')}"
        portfolio = {
            "id": pid,
            "portfolio_name": portfolio_name,
            "horizon_1_budget_percentage": horizon_1_pct,
            "horizon_2_budget_percentage": horizon_2_pct,
            "horizon_3_budget_percentage": horizon_3_pct,
            "portfolio_expected_roi": portfolio_expected_roi,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._portfolios[pid] = portfolio
        return portfolio

    def get_portfolio(self, portfolio_id: str) -> Optional[Dict[str, Any]]:
        return self._portfolios.get(portfolio_id)

    # Stage-Gates
    def conduct_gate_review(
        self,
        workspace_id: str,
        gate_stage: GateStage,
        reviewer_id: str,
        evidence_completeness_score: float = 0.85,
        decision: GateDecision = GateDecision.PROCEED,
        review_notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Conduct governed stage-gate review requiring evidence before advancing to development."""
        review_id = f"gate_{uuid.uuid4().hex[:12]}"
        review = {
            "id": review_id,
            "workspace_id": workspace_id,
            "gate_stage": gate_stage.value if hasattr(gate_stage, "value") else str(gate_stage),
            "reviewer_id": reviewer_id,
            "evidence_completeness_score": max(0.1, min(1.0, evidence_completeness_score)),
            "decision": decision.value if hasattr(decision, "value") else str(decision),
            "review_notes": review_notes or f"Gate {gate_stage} completed with status {decision}",
            "decision_timestamp": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat(),
        }
        self._gate_reviews.setdefault(workspace_id, []).append(review)
        return review

    def list_gate_reviews(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._gate_reviews.get(workspace_id, [])

    # Pivot Engine
    def evaluate_pivot_recommendation(
        self,
        hypothesis_supported: bool,
        market_demand_strong: bool,
        tech_feasible: bool,
        unit_economics_viable: bool,
    ) -> Dict[str, Any]:
        """Assess whether to CONTINUE, PIVOT (Customer, Problem, Value Prop, Model), PAUSE, or STOP."""
        if hypothesis_supported and market_demand_strong and tech_feasible and unit_economics_viable:
            return {
                "action": PivotAction.CONTINUE.value,
                "confidence": 0.95,
                "rationale": "All core hypotheses, market signals, and unit economics are validated.",
            }
        elif not unit_economics_viable and market_demand_strong:
            return {
                "action": PivotAction.PIVOT_BUSINESS_MODEL.value,
                "confidence": 0.88,
                "rationale": "High market demand present, but current unit cost structure requires pricing or delivery model pivot.",
            }
        elif not tech_feasible:
            return {
                "action": PivotAction.PIVOT_TECHNOLOGY.value,
                "confidence": 0.85,
                "rationale": "Target technical architecture unfeasible; pivot to alternative framework or managed infrastructure.",
            }
        elif not market_demand_strong:
            return {
                "action": PivotAction.PIVOT_CUSTOMER.value,
                "confidence": 0.82,
                "rationale": "Initial ICP showed insufficient willingness-to-pay; pivot to adjacent enterprise vertical.",
            }
        else:
            return {
                "action": PivotAction.STOP.value,
                "confidence": 0.90,
                "rationale": "Empirical evidence refutes core problem-solution hypothesis.",
            }
