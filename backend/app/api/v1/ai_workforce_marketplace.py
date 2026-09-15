"""
Phase 86 Enterprise AI Workforce Marketplace REST API Router.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional

from app.services.ai_workforce_marketplace.skills import MarketplaceSkillsService
from app.services.ai_workforce_marketplace.services import MarketplaceServicesService
from app.services.ai_workforce_marketplace.discovery import MarketplaceDiscoveryService
from app.services.ai_workforce_marketplace.copilot import MarketplaceCopilotService
from app.services.ai_workforce_marketplace.autonomy import MarketplaceAutonomyService

router = APIRouter(prefix="/ai-marketplace", tags=["Enterprise AI Workforce Marketplace & Capability Exchange"])

@router.get("/capabilities", response_model=List[Dict[str, Any]])
def search_capabilities(q: Optional[str] = Query(None)):
    return MarketplaceDiscoveryService.search_capabilities(q or "")

@router.get("/skills", response_model=List[Dict[str, Any]])
def get_marketplace_skills():
    return MarketplaceSkillsService.get_marketplace_skills()

@router.get("/services", response_model=List[Dict[str, Any]])
def get_services():
    return MarketplaceServicesService.get_services()

@router.post("/copilot/query", response_model=Dict[str, Any])
def query_marketplace_copilot(payload: Dict[str, Any]):
    user_query = payload.get("query", "Which agent should handle incident triage?")
    return MarketplaceCopilotService.query_marketplace_copilot(user_query)

@router.post("/agents/action", response_model=Dict[str, Any])
def execute_capability_action(payload: Dict[str, Any]):
    capability_id = payload.get("capability_id", "cap-aria-ops")
    task_type = payload.get("task", "verify_certification")
    scope = payload.get("scope", "Aria-Ops — Autonomous SRE")
    parameters = payload.get("parameters", {})
    user_role = payload.get("user_role", "CAPABILITY_CONSUMER")
    return MarketplaceAutonomyService.execute_capability_action(capability_id, task_type, scope, parameters, user_role)
