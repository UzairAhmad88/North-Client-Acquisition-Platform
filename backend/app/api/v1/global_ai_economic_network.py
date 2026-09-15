"""
Phase 88: Global AI Economic Network & Autonomous Machine Commerce REST API Router.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.services.global_ai_economic_network import (
    EconomicNetworkEntityService,
    EconomicCatalogService,
    EconomicCommerceService,
    EconomicSupplyChainService,
    EconomicDisputeAuditService,
    EconomicCopilotService,
    EconomicAutonomyService,
)

router = APIRouter(prefix="/economic-network", tags=["Global AI Economic Network OS"])

class DynamicPriceRequest(BaseModel):
    sku: str
    demand_multiplier: float = 1.0

class M2MTransactionRequest(BaseModel):
    buyer_id: str
    seller_id: str
    sku: str
    offer_price_usd: float
    autonomy_tier: int = 4

class ShockSimulationRequest(BaseModel):
    scenario: str = "PROVIDER_OUTAGE"

class CopilotQueryRequest(BaseModel):
    prompt: str

class EmergencyPauseRequest(BaseModel):
    pause_active: bool
    reason: str = "Executive Manual Override"

@router.get("/entities")
def get_entities():
    """List machine-native organizations and network nodes."""
    return {"entities": EconomicNetworkEntityService.get_network_entities()}

@router.get("/provider-graph")
def get_provider_graph():
    """Get global provider & economic dependency graph."""
    return EconomicNetworkEntityService.get_provider_graph()

@router.get("/catalog")
def get_catalog():
    """List machine-native product & service catalog with dynamic pricing."""
    return {"catalog": EconomicCatalogService.get_product_catalog()}

@router.post("/catalog/dynamic-price")
def calculate_dynamic_price(req: DynamicPriceRequest):
    """Calculate real-time dynamic pricing based on demand & capacity."""
    return EconomicCatalogService.calculate_dynamic_price(req.sku, req.demand_multiplier)

@router.get("/commerce/orders")
def get_orders():
    """List machine-to-machine commercial orders."""
    return {"orders": EconomicCommerceService.get_commerce_orders()}

@router.post("/commerce/orders")
def execute_order(req: M2MTransactionRequest):
    """Execute autonomous machine-to-machine commercial transaction."""
    return EconomicCommerceService.execute_m2m_transaction(req.buyer_id, req.seller_id, req.sku, req.offer_price_usd, req.autonomy_tier)

@router.get("/risk-graph")
def get_risk_graph():
    """Get global risk graph & concentration risk metrics."""
    return {"risk_nodes": EconomicSupplyChainService.get_risk_graph()}

@router.post("/supply-chain/simulate")
def simulate_shock(req: ShockSimulationRequest):
    """Simulate supply-chain shock and contingency failover."""
    return EconomicSupplyChainService.simulate_supply_chain_shock(req.scenario)

@router.get("/disputes/evidence")
def get_disputes():
    """Get machine dispute network & evidence graph records."""
    return {"disputes": EconomicDisputeAuditService.get_dispute_evidences()}

@router.get("/reconciliation")
def get_reconciliation():
    """Get automated AP/AR reconciliation status."""
    return EconomicDisputeAuditService.reconcile_ap_ar()

@router.post("/copilot/query")
def query_copilot(req: CopilotQueryRequest):
    """Query Autonomous Strategy Assistant & Executive AI Engine."""
    return EconomicCopilotService.query_strategy_copilot(req.prompt)

@router.get("/autonomy/pause-status")
def get_pause_status():
    """Get Emergency Economic Pause and Sandbox status."""
    return EconomicAutonomyService.get_pause_status()

@router.post("/autonomy/emergency-pause")
def toggle_emergency_pause(req: EmergencyPauseRequest):
    """Toggle Global AI Economic Pause emergency killswitch."""
    return EconomicAutonomyService.toggle_emergency_pause(req.pause_active, req.reason)

@router.get("/autonomy/tasks")
def get_autonomy_tasks():
    """List Level 5 governance audit trail & agent tasks."""
    return {"tasks": EconomicAutonomyService.get_agent_tasks()}
