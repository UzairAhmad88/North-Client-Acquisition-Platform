"""
Phase 82 Enterprise Data Platform REST API Router.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.services.data_platform.sources import DataPlatformSourcesService
from app.services.data_platform.pipelines import DataPlatformPipelinesService
from app.services.data_platform.catalog import DataPlatformCatalogService
from app.services.data_platform.lineage import DataPlatformLineageService
from app.services.data_platform.governance import DataPlatformGovernanceService
from app.services.data_platform.quality import DataPlatformQualityService
from app.services.data_platform.mdm import DataPlatformMdmService
from app.services.data_platform.copilot import DataPlatformCopilotService
from app.services.data_platform.agents import DataPlatformAgentsService
from app.services.data_platform.costs import DataPlatformCostsService

router = APIRouter(prefix="/data-platform", tags=["Data Platform & Autonomous Data Operations"])

@router.get("/sources", response_model=List[Dict[str, Any]])
def get_data_sources():
    return DataPlatformSourcesService.get_registered_sources()

@router.get("/sources/discover", response_model=List[Dict[str, Any]])
def discover_data_sources():
    return DataPlatformSourcesService.discover_data_sources()

@router.get("/pipelines", response_model=List[Dict[str, Any]])
def get_pipelines():
    return DataPlatformPipelinesService.get_pipelines()

@router.get("/pipelines/{pipeline_id}/runs", response_model=List[Dict[str, Any]])
def get_pipeline_runs(pipeline_id: str):
    return DataPlatformPipelinesService.get_pipeline_runs(pipeline_id)

@router.get("/catalog", response_model=List[Dict[str, Any]])
def search_catalog(q: Optional[str] = Query(None)):
    return DataPlatformCatalogService.search_catalog(q or "")

@router.get("/lineage/{asset_id}", response_model=Dict[str, Any])
def get_asset_lineage(asset_id: str):
    return DataPlatformLineageService.get_asset_lineage(asset_id)

@router.get("/governance", response_model=Dict[str, Any])
def get_governance_summary():
    return DataPlatformGovernanceService.get_governance_summary()

@router.get("/quality", response_model=Dict[str, Any])
def get_quality_overview():
    return DataPlatformQualityService.get_quality_overview()

@router.get("/mdm/golden-records", response_model=List[Dict[str, Any]])
def get_golden_records(domain: str = "Customer"):
    return DataPlatformMdmService.get_golden_records(domain)

@router.post("/copilot/query", response_model=Dict[str, Any])
def query_data_copilot(payload: Dict[str, Any]):
    user_query = payload.get("query", "Where does net revenue come from?")
    return DataPlatformCopilotService.query_data_copilot(user_query)

@router.post("/agents/action", response_model=Dict[str, Any])
def execute_agent_action(payload: Dict[str, Any]):
    agent_name = payload.get("agent", "data_quality_agent")
    task_type = payload.get("task", "run_quality_check")
    scope = payload.get("scope", "gold_customer_revenue_daily")
    parameters = payload.get("parameters", {})
    user_role = payload.get("user_role", "DATA_ENGINEER")
    return DataPlatformAgentsService.execute_agent_action(agent_name, task_type, scope, parameters, user_role)

@router.get("/costs", response_model=Dict[str, Any])
def get_cost_summary():
    return DataPlatformCostsService.get_cost_summary()
