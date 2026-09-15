"""
Sensitivity & Impact Agent (Phase 50).
Conducts parameter sensitivity analysis, Tornado chart rankings, and counterfactual evaluations.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.digital_twin.base import ScenarioType, SimulationMethod
    from backend.app.services.digital_twin.service import DigitalTwinPlatformService
except ImportError:
    from app.services.digital_twin.base import ScenarioType, SimulationMethod
    from app.services.digital_twin.service import DigitalTwinPlatformService


class SensitivityImpactAgent(BaseAgent):
    """
    Agent for ranking parameter sensitivities and evaluating counterfactual "what-if" divergences.
    """

    agent_id = "sensitivity_impact_agent"
    name = "Sensitivity & Impact Agent"
    version = "1.0"
    description = "Calculates parameter elasticity, Tornado rankings, and counterfactual historical variances."

    def __init__(self, service: Optional[DigitalTwinPlatformService] = None):
        super().__init__()
        self.service = service or DigitalTwinPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_TWIN_STATE,
            AgentPermission.READ_TWIN_SCENARIOS,
            AgentPermission.RUN_SENSITIVITY_ANALYSIS,
            AgentPermission.RUN_COUNTERFACTUAL,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        analysis_mode = str(params.get("mode") or "SENSITIVITY").upper()

        if analysis_mode == "COUNTERFACTUAL":
            event_id = str(params.get("historical_event_id") or "EVT-2025-Q3")
            condition = str(params.get("hypothetical_condition") or "Conversion was 12% instead of 8%")
            actuals = params.get("historical_actual_metrics") or {"cumulative_revenue_usd": 140000.0, "ending_active_clients": 12.0}
            overrides = params.get("hypothetical_parameter_overrides") or {"lead_conversion_rate": 0.12}

            cf_res = self.service.run_counterfactual(
                historical_event_id=event_id,
                hypothetical_condition=condition,
                historical_actual_metrics=actuals,
                hypothetical_parameter_overrides=overrides,
            )

            return {
                "status": "SUCCESS",
                "mode": "COUNTERFACTUAL",
                "counterfactual_code": cf_res.counterfactual_code,
                "historical_actual": cf_res.historical_actual,
                "simulated_alternative": cf_res.simulated_alternative,
                "divergence_summary": cf_res.divergence_summary,
                "limitations": cf_res.limitations,
            }
        else:
            # Default Sensitivity Tornado analysis
            scenario = self.service.create_scenario(
                name="Sensitivity Base Scenario",
                scenario_type=ScenarioType.GROWTH,
                simulation_method=SimulationMethod.DETERMINISTIC,
                tenant_id=tenant_id,
            )
            target_metric = str(params.get("target_metric") or "cumulative_revenue_usd")
            rankings = self.service.analyze_sensitivity(scenario, target_metric=target_metric)

            return {
                "status": "SUCCESS",
                "mode": "SENSITIVITY",
                "target_metric": target_metric,
                "rankings": [
                    r.model_dump() if hasattr(r, "model_dump") else r.dict()
                    for r in rankings
                ],
            }
