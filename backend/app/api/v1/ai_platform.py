"""
Phase 83 Enterprise AI/ML Platform REST API Router.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.services.ai_platform.projects import AiPlatformProjectsService
from app.services.ai_platform.experiments import AiPlatformExperimentsService
from app.services.ai_platform.registry import AiPlatformRegistryService
from app.services.ai_platform.evaluation import AiPlatformEvaluationService
from app.services.ai_platform.deployment import AiPlatformDeploymentService
from app.services.ai_platform.llm_gateway import AiPlatformLlmGatewayService
from app.services.ai_platform.copilot import AiPlatformCopilotService
from app.services.ai_platform.autonomy import AiPlatformAutonomyService
from app.services.ai_platform.costs import AiPlatformCostsService

router = APIRouter(prefix="/ai-platform", tags=["AI/ML Platform & Autonomous AI Operations"])

@router.get("/projects", response_model=List[Dict[str, Any]])
def get_projects():
    return AiPlatformProjectsService.get_projects()

@router.get("/experiments", response_model=List[Dict[str, Any]])
def get_experiments(project_id: Optional[str] = Query("prj-genai-copilot-01")):
    return AiPlatformExperimentsService.get_experiments(project_id or "prj-genai-copilot-01")

@router.get("/registry/models", response_model=List[Dict[str, Any]])
def get_registered_models():
    return AiPlatformRegistryService.get_registered_models()

@router.get("/evaluations", response_model=List[Dict[str, Any]])
def get_evaluations(model_id: Optional[str] = Query("mdl-ops-copilot-70b")):
    return AiPlatformEvaluationService.get_evaluations(model_id or "mdl-ops-copilot-70b")

@router.get("/deployments", response_model=List[Dict[str, Any]])
def get_deployments():
    return AiPlatformDeploymentService.get_deployments()

@router.post("/llm-gateway/process", response_model=Dict[str, Any])
def process_llm_request(payload: Dict[str, Any]):
    model_name = payload.get("model", "Uzaii-Ops-Copilot-Llama3-70B")
    prompt = payload.get("prompt", "Analyze root cause for payment latency spike")
    user_id = payload.get("user_id", "usr-admin")
    return AiPlatformLlmGatewayService.process_llm_request(model_name, prompt, user_id)

@router.post("/copilot/query", response_model=Dict[str, Any])
def query_ai_copilot(payload: Dict[str, Any]):
    user_query = payload.get("query", "Which model performs best?")
    return AiPlatformCopilotService.query_ai_copilot(user_query)

@router.post("/agents/action", response_model=Dict[str, Any])
def execute_autonomous_action(payload: Dict[str, Any]):
    agent_name = payload.get("agent", "evaluation_agent")
    task_type = payload.get("task", "run_eval_suite")
    scope = payload.get("scope", "mdl-ops-copilot-70b")
    parameters = payload.get("parameters", {})
    user_role = payload.get("user_role", "MLOPS_ENGINEER")
    return AiPlatformAutonomyService.execute_autonomous_action(agent_name, task_type, scope, parameters, user_role)

@router.get("/costs", response_model=Dict[str, Any])
def get_cost_summary():
    return AiPlatformCostsService.get_cost_summary()
