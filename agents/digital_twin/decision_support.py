"""
Decision Support Agent (Phase 50).
Synthesizes simulation results into comparative decision trade-off options.
Enforces governance rule: Agent generates advisory options; only human executives decide.
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


class DecisionSupportAgent(BaseAgent):
    """
    Agent for translating simulation outputs into structured trade-off decision matrices.
    Prohibited from autonomously approving decisions or executing operational changes.
    """

    agent_id = "decision_support_agent"
    name = "Decision Support Agent"
    version = "1.0"
    description = "Prepares decision option trade-off matrices for human executive review and authorization."

    def __init__(self, service: Optional[DigitalTwinPlatformService] = None):
        super().__init__()
        self.service = service or DigitalTwinPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_TWIN_SCENARIOS,
            AgentPermission.RUN_TWIN_SIMULATION,
            AgentPermission.CREATE_DECISION_OPTIONS_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        question = str(params.get("question") or "Which strategic capacity expansion scenario should be chosen?")

        # Construct baseline scenario and growth scenarios
        base_scenario = self.service.create_scenario(
            name="Baseline Capacity",
            scenario_type=ScenarioType.RESOURCE,
            simulation_method=SimulationMethod.MONTE_CARLO,
            tenant_id=tenant_id,
        )
        alt_scenario = self.service.create_scenario(
            name="Hire 2 Developers (+33% Capacity)",
            scenario_type=ScenarioType.RESOURCE,
            simulation_method=SimulationMethod.MONTE_CARLO,
            parameter_overrides={"developer_capacity_fte": 8.0, "monthly_operating_cost_usd": 24000.0},
            tenant_id=tenant_id,
        )

        sim_base = self.service.run_scenario_simulation(base_scenario, iterations=500)
        sim_alt = self.service.run_scenario_simulation(alt_scenario, iterations=500)

        options = self.service.build_decision_options([sim_base, sim_alt])

        return {
            "status": "SUCCESS",
            "decision_question": question,
            "governance_notice": "AI recommendation only. Human executive authorization required to approve and execute.",
            "options": [
                opt.model_dump() if hasattr(opt, "model_dump") else opt.dict()
                for opt in options
            ],
        }
