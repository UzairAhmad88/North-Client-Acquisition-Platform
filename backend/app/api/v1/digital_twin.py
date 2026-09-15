"""
Phase 84 Enterprise Digital Twin REST API Router.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.services.digital_twin.entities import DigitalTwinEntitiesService
from app.services.digital_twin.snapshots import DigitalTwinSnapshotsService
from app.services.digital_twin.scenarios import DigitalTwinScenariosService
from app.services.digital_twin.simulation import DigitalTwinSimulationService
from app.services.digital_twin.optimization import DigitalTwinOptimizationService
from app.services.digital_twin.recommendations import DigitalTwinRecommendationsService
from app.services.digital_twin.copilot import DigitalTwinCopilotService
from app.services.digital_twin.autonomy import DigitalTwinAutonomyService

router = APIRouter(prefix="/digital-twin", tags=["Enterprise Digital Twin & Autonomous Optimization"])

@router.get("/entities", response_model=List[Dict[str, Any]])
def get_twin_entities():
    return DigitalTwinEntitiesService.get_twin_entities()

@router.get("/snapshots/current", response_model=Dict[str, Any])
def get_current_snapshot():
    return DigitalTwinSnapshotsService.get_current_snapshot()

@router.get("/scenarios", response_model=List[Dict[str, Any]])
def get_scenarios():
    return DigitalTwinScenariosService.get_scenarios()

@router.post("/simulation/run", response_model=Dict[str, Any])
def run_simulation(payload: Dict[str, Any]):
    scenario_id = payload.get("scenario_id", "scn-sales-surge-20")
    return DigitalTwinSimulationService.run_simulation(scenario_id)

@router.post("/optimization/run", response_model=Dict[str, Any])
def run_optimization(payload: Dict[str, Any]):
    objective = payload.get("objective", "MAXIMIZE_REVENUE_MINIMIZE_RISK")
    return DigitalTwinOptimizationService.run_optimization(objective)

@router.get("/recommendations", response_model=List[Dict[str, Any]])
def get_recommendations():
    return DigitalTwinRecommendationsService.get_recommendations()

@router.post("/copilot/query", response_model=Dict[str, Any])
def query_twin_copilot(payload: Dict[str, Any]):
    user_query = payload.get("query", "What happens if sales increase 20%?")
    return DigitalTwinCopilotService.query_twin_copilot(user_query)

@router.post("/agents/action", response_model=Dict[str, Any])
def execute_autonomous_action(payload: Dict[str, Any]):
    agent_name = payload.get("agent", "digital_twin_orchestrator")
    task_type = payload.get("task", "run_simulation")
    scope = payload.get("scope", "scn-sales-surge-20")
    parameters = payload.get("parameters", {})
    user_role = payload.get("user_role", "STRATEGY_VP")
    return DigitalTwinAutonomyService.execute_autonomous_action(agent_name, task_type, scope, parameters, user_role)
