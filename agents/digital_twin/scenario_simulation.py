"""
Scenario Simulation Agent (Phase 50).
Configures what-if business scenarios and runs isolated Monte Carlo or Deterministic simulations.
"""

from typing import Any, Dict, List, Optional, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.digital_twin.base import ScenarioType, SimulationMethod, TimeHorizon
    from backend.app.services.digital_twin.service import DigitalTwinPlatformService
except ImportError:
    from app.services.digital_twin.base import ScenarioType, SimulationMethod, TimeHorizon
    from app.services.digital_twin.service import DigitalTwinPlatformService


class ScenarioSimulationAgent(BaseAgent):
    """
    Agent for building strategic scenarios and executing sandboxed simulations.
    Operates in isolated memory sandboxes; never mutates live production state.
    """

    agent_id = "scenario_simulation_agent"
    name = "Scenario Simulation Agent"
    version = "1.0"
    description = "Formulates strategic scenarios and executes sandboxed business simulations."

    def __init__(self, service: Optional[DigitalTwinPlatformService] = None):
        super().__init__()
        self.service = service or DigitalTwinPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_TWIN_STATE,
            AgentPermission.READ_TWIN_SCENARIOS,
            AgentPermission.RUN_TWIN_SIMULATION,
            AgentPermission.CREATE_SCENARIO_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        params = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        tenant_id = str(context.metadata.get("tenant_id") or params.get("tenant_id") or "default_tenant")
        scenario_name = str(params.get("name") or "Strategic Growth Scenario")
        raw_type = str(params.get("scenario_type") or "GROWTH")
        raw_method = str(params.get("simulation_method") or "MONTE_CARLO")
        raw_horizon = str(params.get("time_horizon") or "12_MONTHS")
        overrides = params.get("parameter_overrides") or {}
        iterations = int(params.get("iterations") or 1000)

        # Map Enums
        try:
            scenario_type = ScenarioType[raw_type]
        except KeyError:
            scenario_type = ScenarioType.GROWTH

        try:
            sim_method = SimulationMethod[raw_method]
        except KeyError:
            sim_method = SimulationMethod.MONTE_CARLO

        try:
            horizon = TimeHorizon(raw_horizon)
        except ValueError:
            horizon = TimeHorizon.MONTH_12

        scenario = self.service.create_scenario(
            name=scenario_name,
            scenario_type=scenario_type,
            time_horizon=horizon,
            simulation_method=sim_method,
            parameter_overrides=overrides,
            tenant_id=tenant_id,
            created_by="scenario_simulation_agent",
        )

        sim_result = self.service.run_scenario_simulation(
            scenario=scenario,
            iterations=iterations,
        )

        return {
            "status": "SUCCESS",
            "scenario_code": scenario.scenario_code,
            "scenario_name": scenario.name,
            "simulation_code": sim_result.simulation_code,
            "method": sim_result.method.value,
            "iterations": sim_result.iterations,
            "runtime_seconds": sim_result.runtime_seconds,
            "metrics_summary": sim_result.metrics_summary,
            "uncertainty_distribution": sim_result.uncertainty_distribution,
            "constraint_violations": sim_result.constraint_violations,
            "assumptions_applied": sim_result.assumptions_applied,
        }
