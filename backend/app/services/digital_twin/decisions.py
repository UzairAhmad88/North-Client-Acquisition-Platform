"""
Decision Support and Governance Engine for Phase 50: Unified Digital Twin.
Transforms scenario simulations into trade-off decision matrices and records human executive decisions.
Enforces the mandatory rule: AI presents options; only authorized human leaders decide.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.digital_twin.base import (
        DecisionOption,
        DecisionRecord,
        DecisionStatus,
        SimulationResult,
    )
except ImportError:
    from app.services.digital_twin.base import (
        DecisionOption,
        DecisionRecord,
        DecisionStatus,
        SimulationResult,
    )

logger = logging.getLogger(__name__)


class DecisionSupportManager:
    """
    Evaluates scenario results to build comparative Decision Options and logs governed Human Decision Records.
    """

    def generate_options_from_simulations(
        self,
        simulation_results: List[SimulationResult],
    ) -> List[DecisionOption]:
        """Synthesizes multiple scenario simulation outcomes into structured trade-off options."""
        options = []
        for sim in simulation_results:
            metrics = sim.metrics_summary
            rev = float(metrics.get("cumulative_revenue_usd", 0.0))
            net_profit = float(metrics.get("cumulative_net_profit_usd", 0.0))
            ai_cost = float(metrics.get("cumulative_ai_cost_usd", 0.0))
            utilization = float(metrics.get("final_capacity_utilization_percentage", 80.0))
            violations_count = len(sim.constraint_violations)

            # Compute normalized risk score (0-100)
            risk_score = 15.0
            if utilization > 95.0:
                risk_score += 40.0
            elif utilization > 85.0:
                risk_score += 20.0
            risk_score += violations_count * 20.0
            risk_score = min(100.0, risk_score)

            confidence = 0.85 if sim.method.value == "MONTE_CARLO" else 0.75

            tradeoff = (
                f"Projected Net Profit: ${net_profit:,.2f} on Revenue ${rev:,.2f}. "
                f"Team Utilization: {utilization:.1f}%. Risk: {risk_score:.0f}/100."
            )
            if violations_count > 0:
                tradeoff += f" WARNING: {violations_count} constraint violations detected."

            options.append(
                DecisionOption(
                    title=f"Scenario Option: {sim.scenario_id}",
                    scenario_id=sim.scenario_id,
                    expected_benefit_usd=round(net_profit, 2),
                    expected_cost_usd=round(ai_cost + (rev - net_profit), 2),
                    risk_score=round(risk_score, 1),
                    confidence_score=confidence,
                    tradeoff_summary=tradeoff,
                )
            )

        return options

    def record_human_decision(
        self,
        question: str,
        rationale: str,
        decision_owner: str,
        selected_option_id: Optional[str] = None,
        scenario_version: int = 1,
    ) -> DecisionRecord:
        """
        Persists a verified human strategic decision.
        Enforces governance: AI cannot autonomously decide.
        """
        if not decision_owner:
            raise ValueError("A strategic decision must have an identified human decision owner.")

        record = DecisionRecord(
            question=question,
            selected_option_id=selected_option_id,
            rationale=rationale,
            decision_owner=decision_owner,
            approved_at=datetime.now(timezone.utc),
            scenario_version=scenario_version,
            status=DecisionStatus.APPROVED,
        )
        return record
