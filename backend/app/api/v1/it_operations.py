"""Phase 81 Enterprise IT Operations & AIOps API Router."""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel

from app.services.itops import (
    ItOpsServicesService,
    ItOpsObservabilityService,
    ItOpsIncidentsService,
    ItOpsRunbooksService,
    ItOpsAiOpsService,
    ItOpsSlosService,
)
from app.agents.itops import OperationsCopilotAgent

router = APIRouter(prefix="/it-operations", tags=["Enterprise IT Operations"])


class CopilotQueryRequest(BaseModel):
    prompt: str


class RunbookExecuteRequest(BaseModel):
    runbook_code: str
    target: str
    autonomy_level: Optional[str] = "L3"
    approved_by: Optional[str] = None


@router.get("/command-center")
def get_it_command_center():
    """Retrieve Executive IT Command Center metrics."""
    return {
        "status": "HEALTHY",
        "service_health_pct": 99.98,
        "active_incidents_count": 1,
        "metrics": {
            "mttd_mins": 2.8,
            "mttr_mins": 8.4,
            "noise_reduction_pct": 84.5,
            "automation_rate_pct": 74.2,
            "active_services": 42
        },
        "aiops_summary": ItOpsAiOpsService.get_aiops_summary(),
    }


@router.get("/services")
def list_services():
    return {"data": ItOpsServicesService.list_services()}


@router.get("/cmdb/topology")
def get_cmdb_topology(service_code: str = Query("SVC-PAYMENT-GATEWAY")):
    return {"data": ItOpsServicesService.get_cmdb_topology(service_code)}


@router.get("/observability/apm")
def get_apm_metrics(service_code: str = Query("SVC-PAYMENT-GATEWAY")):
    return {"data": ItOpsObservabilityService.get_apm_metrics(service_code)}


@router.get("/observability/traces")
def get_recent_traces(service_code: str = Query("SVC-PAYMENT-GATEWAY")):
    return {"data": ItOpsObservabilityService.get_recent_traces(service_code)}


@router.get("/incidents")
def list_incidents():
    return {"data": ItOpsIncidentsService.list_incidents()}


@router.get("/incidents/{incident_code}")
def get_incident_details(incident_code: str):
    return {"data": ItOpsIncidentsService.get_incident_details(incident_code)}


@router.get("/runbooks")
def list_runbooks():
    return {"data": ItOpsRunbooksService.list_runbooks()}


@router.post("/runbooks/execute")
def execute_runbook(req: RunbookExecuteRequest):
    result = ItOpsRunbooksService.execute_runbook(
        runbook_code=req.runbook_code,
        target=req.target,
        autonomy_level=req.autonomy_level,
        approved_by=req.approved_by
    )
    if not result.get("success"):
        raise HTTPException(status_code=403, detail=result.get("message"))
    return {"data": result}


@router.get("/aiops/summary")
def get_aiops_summary():
    return {"data": ItOpsAiOpsService.get_aiops_summary()}


@router.get("/slos")
def list_slos():
    return {"data": ItOpsSlosService.list_slos()}


@router.post("/copilot/query")
def query_operations_copilot(req: CopilotQueryRequest):
    copilot = OperationsCopilotAgent()
    return {"data": copilot.run_task(req.prompt)}


@router.get("/agents")
def list_itops_agents():
    agents = [
        {"agent_id": "it_operations_orchestrator", "name": "IT Operations Orchestrator Agent", "autonomy_level": "L5", "status": "ACTIVE"},
        {"agent_id": "incident_triage", "name": "Incident Triage Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "root_cause", "name": "Root Cause Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "observability", "name": "Observability Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "capacity", "name": "Capacity Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "performance", "name": "Performance Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "change_risk", "name": "Change Risk Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "deployment", "name": "Deployment Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "release", "name": "Release Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "infrastructure", "name": "Infrastructure Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "cloud_operations", "name": "Cloud Operations Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "database_operations", "name": "Database Operations Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "network_operations", "name": "Network Operations Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "service_desk", "name": "Service Desk Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "runbook", "name": "Runbook Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "finops", "name": "FinOps Agent", "autonomy_level": "L4", "status": "ACTIVE"},
        {"agent_id": "operations_copilot", "name": "Operations Copilot Agent", "autonomy_level": "L4", "status": "ACTIVE"}
    ]
    return {"data": agents}
