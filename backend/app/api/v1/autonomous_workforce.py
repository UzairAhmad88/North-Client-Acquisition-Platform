"""
Phase 85 Enterprise Autonomous Workforce REST API Router.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.services.autonomous_workforce.employees import WorkforceEmployeesService
from app.services.autonomous_workforce.delegation import WorkforceDelegationService
from app.services.autonomous_workforce.consensus import WorkforceConsensusService
from app.services.autonomous_workforce.copilot import WorkforceCopilotService
from app.services.autonomous_workforce.autonomy import WorkforceAutonomyService

router = APIRouter(prefix="/autonomous-workforce", tags=["Enterprise Autonomous Workforce & AI Employees"])

@router.get("/employees", response_model=List[Dict[str, Any]])
def get_ai_employees():
    return WorkforceEmployeesService.get_ai_employees()

@router.get("/tasks", response_model=List[Dict[str, Any]])
def get_delegated_tasks():
    return WorkforceDelegationService.get_delegated_tasks()

@router.post("/consensus/run", response_model=Dict[str, Any])
def run_consensus(payload: Dict[str, Any]):
    topic = payload.get("topic", "Production Canary Rollout Promotion")
    return WorkforceConsensusService.run_consensus(topic)

@router.post("/copilot/query", response_model=Dict[str, Any])
def query_workforce_copilot(payload: Dict[str, Any]):
    user_query = payload.get("query", "What is the status of active AI Employees?")
    return WorkforceCopilotService.query_workforce_copilot(user_query)

@router.post("/agents/action", response_model=Dict[str, Any])
def execute_employee_action(payload: Dict[str, Any]):
    employee_id = payload.get("employee_id", "emp-ai-sre-01")
    task_type = payload.get("task", "triage_incident")
    scope = payload.get("scope", "Production Payment Gateway")
    parameters = payload.get("parameters", {})
    user_role = payload.get("user_role", "HUMAN_SUPERVISOR")
    return WorkforceAutonomyService.execute_employee_action(employee_id, task_type, scope, parameters, user_role)
