"""
Phase 93 — Global Digital Society, Autonomous Organizations & Networked Economic Coordination REST API Router
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.services.global_digital_society import (
    DigitalIdentityPersonaService,
    AiNativeOrgGovernanceService,
    AutonomousWorkflowEngineService,
    FinancialMarketplaceEconomyService,
    CrisisSupplyChainResilienceService,
    DpiMachineEconomyService,
    PrivacyTrustEcosystemService,
)

router = APIRouter(prefix="/digital-society", tags=["Global Digital Society OS"])

class IdentityCredentialPayload(BaseModel):
    entity_name: str = Field(..., example="Dr. Aris Thorne")
    entity_type: str = Field("person", example="person")
    verification_level: str = Field("STRONG_VERIFIED")

class PersonaConfigPayload(BaseModel):
    user_id: str = Field("usr-lead-001")
    persona_name: str = Field("Aris-AI Assistant")
    action_level: str = Field("REQUEST_APPROVAL", example="REQUEST_APPROVAL")

class OrgGraphPayload(BaseModel):
    org_name: str = Field("Aetheria Global Autonomous Corp")

class PolicyEvalPayload(BaseModel):
    policy_name: str = Field("Global Treasury Spending Cap Policy")

class WorkflowDeployPayload(BaseModel):
    name: str = Field("Autonomous Cloud Resource Rebalancing")
    org_id: str = Field("org-alpha")
    budget_limit_usd: float = Field(15000.0)

class EmergencyPausePayload(BaseModel):
    workflow_id: str = Field("ALL_WORKFLOWS")
    global_kill_switch: bool = Field(False)

class MarketplaceTxPayload(BaseModel):
    agent_id: str = Field("agt-procure-01")
    service_id: str = Field("srv-compute-09")
    amount: float = Field(250.0)
    agent_budget_cap: float = Field(5000.0)

class SupplyChainSimPayload(BaseModel):
    network_name: str = Field("Global Microchip & Component Supply Network")
    scenario: str = Field("Geographic Port Lockout")

class CrisisCommandPayload(BaseModel):
    title: str = Field("Critical Infrastructure Telemetry Outage")

class M2MNegotiationPayload(BaseModel):
    buyer_agent: str = Field("agt-buyer-01")
    seller_agent: str = Field("agt-seller-02")
    proposed_price: float = Field(1200.0)
    max_authority_usd: float = Field(2000.0)
    scope: str = Field("GPU Cluster Time 100 Hours")

class QuarantinePayload(BaseModel):
    agent_id: str = Field("agt-anomalous-99")
    reason: str = Field("Anomalous API request burst exceeding policy thresholds")

# --- API Endpoints ---

@router.post("/identities/credential", response_model=Dict[str, Any])
def issue_credential(payload: IdentityCredentialPayload):
    """Issues or verifies digital identity and SSI credential with selective disclosure."""
    return DigitalIdentityPersonaService.issue_verifiable_credential(payload.dict())

@router.post("/personas/config", response_model=Dict[str, Any])
def configure_persona(payload: PersonaConfigPayload):
    """Configures user AI persona representation and action levels."""
    return DigitalIdentityPersonaService.configure_ai_persona(payload.dict())

@router.post("/orgs/graph", response_model=Dict[str, Any])
def manage_org_graph(payload: OrgGraphPayload):
    """Manages AI-native organization graph, AI roles, and dynamic org chart."""
    return AiNativeOrgGovernanceService.manage_ai_org_graph(payload.dict())

@router.post("/governance/evaluate", response_model=Dict[str, Any])
def evaluate_policy(payload: PolicyEvalPayload):
    """Evaluates policy hierarchy, dual-approval controls, and segregation of duties."""
    return AiNativeOrgGovernanceService.evaluate_governance_policy(payload.dict())

@router.post("/workflows/contract", response_model=Dict[str, Any])
def deploy_workflow(payload: WorkflowDeployPayload):
    """Deploys an autonomous workflow contract after sandbox testing."""
    return AutonomousWorkflowEngineService.deploy_workflow_contract(payload.dict())

@router.post("/workflows/pause", response_model=Dict[str, Any])
def emergency_pause(payload: EmergencyPausePayload):
    """Triggers emergency pause or global kill-switch across autonomous workflows."""
    return AutonomousWorkflowEngineService.trigger_emergency_pause(payload.dict())

@router.get("/executive/operating-center", response_model=Dict[str, Any])
def get_executive_center(org_id: str = Query("org-alpha")):
    """Provides Executive Operating Center metrics and digital twin state."""
    return FinancialMarketplaceEconomyService.get_executive_operating_center(org_id)

@router.post("/marketplace/transaction", response_model=Dict[str, Any])
def execute_transaction(payload: MarketplaceTxPayload):
    """Executes agent-to-service economy transaction with spending cap enforcement."""
    return FinancialMarketplaceEconomyService.execute_agent_marketplace_transaction(payload.dict())

@router.post("/supply-chain/simulate", response_model=Dict[str, Any])
def simulate_supply_chain(payload: SupplyChainSimPayload):
    """Simulates supply network disruptions and resilience strategies."""
    return CrisisSupplyChainResilienceService.run_supply_chain_simulation(payload.dict())

@router.post("/crisis/command", response_model=Dict[str, Any])
def engage_crisis(payload: CrisisCommandPayload):
    """Activates Crisis Command Center with incident command roles."""
    return CrisisSupplyChainResilienceService.engage_crisis_command(payload.dict())

@router.post("/m2m/negotiate", response_model=Dict[str, Any])
def negotiate_m2m(payload: M2MNegotiationPayload):
    """Executes machine-to-machine negotiation within approved authority limits."""
    return DpiMachineEconomyService.execute_m2m_negotiation(payload.dict())

@router.get("/procurement/audit/{procurement_id}", response_model=Dict[str, Any])
def audit_procurement(procurement_id: str):
    """Audits digital procurement agent actions from request through purchase."""
    return DpiMachineEconomyService.run_procurement_audit(procurement_id)

@router.get("/privacy/trust-center", response_model=Dict[str, Any])
def get_trust_center(user_id: str = Query("usr-lead-001")):
    """Gets Digital Trust Center status, data vault controls, and data residency."""
    return PrivacyTrustEcosystemService.get_digital_trust_center_status(user_id)

@router.post("/agent/quarantine", response_model=Dict[str, Any])
def quarantine_agent(payload: QuarantinePayload):
    """Quarantines suspicious agents, preserves forensics, and logs immune alerts."""
    return PrivacyTrustEcosystemService.quarantine_agent(payload.dict())

@router.get("/analytics/systemic-risk", response_model=Dict[str, Any])
def get_systemic_risk():
    """Analyzes ecosystem health, single-point-of-failure dependencies, and emergency mode."""
    return PrivacyTrustEcosystemService.get_systemic_resilience_analytics()
