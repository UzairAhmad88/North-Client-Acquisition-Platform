"""
Phase 89: Planetary-Scale AI Infrastructure & Global Agent Mesh REST API Router.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.services.planetary_ai_infrastructure import (
    PlanetaryFabricMeshService,
    PlanetaryResilienceService,
    PlanetaryTwinFinOpsService,
    PlanetarySandboxPromotionService,
    PlanetarySecurityGovernanceService,
    PlanetaryCopilotStrategyService,
    PlanetaryAutonomyKillswitchService,
)

router = APIRouter(prefix="/planetary-infrastructure", tags=["Planetary-Scale AI Infrastructure OS"])

class RegionFailoverRequest(BaseModel):
    failed_region: str
    target_region: str

class AgentPromotionRequest(BaseModel):
    agent_id: str
    new_tier: str

class AgentQuarantineRequest(BaseModel):
    agent_id: str
    reason: str = "Anomalous Behavior Detected"

class StrategicSimulationRequest(BaseModel):
    prompt: str

class GlobalKillSwitchRequest(BaseModel):
    kill_switch_active: bool
    reason: str = "Executive Emergency Halt"

class SafeModeRequest(BaseModel):
    safe_mode_active: bool
    reason: str = "Restricted Operations Mode"

@router.get("/nodes")
def get_fabric_nodes():
    """List planetary fabric nodes and carbon intensity metrics."""
    return {"nodes": PlanetaryFabricMeshService.get_fabric_nodes()}

@router.get("/agent-mesh")
def get_agent_mesh_nodes():
    """List global agent mesh nodes and cryptographic attestations."""
    return {"mesh_nodes": PlanetaryFabricMeshService.get_agent_mesh_nodes()}

@router.get("/resilience/status")
def get_resilience_status():
    """Get global resilience engine and multi-region failover status."""
    return PlanetaryResilienceService.get_resilience_status()

@router.post("/resilience/failover")
def execute_failover(req: RegionFailoverRequest):
    """Execute automated multi-region failover."""
    return PlanetaryResilienceService.execute_region_failover(req.failed_region, req.target_region)

@router.get("/twin-finops")
def get_twin_finops():
    """Get infrastructure digital twin and FinOps carbon energy metrics."""
    return PlanetaryTwinFinOpsService.get_infrastructure_twin()

@router.get("/promotion/pipeline")
def get_promotion_pipeline():
    """List agent promotion pipeline and certification status."""
    return {"pipeline": PlanetarySandboxPromotionService.get_promotion_pipeline()}

@router.post("/promotion/promote")
def promote_agent(req: AgentPromotionRequest):
    """Promote agent to higher execution tier."""
    return PlanetarySandboxPromotionService.promote_agent(req.agent_id, req.new_tier)

@router.get("/security/quarantine")
def get_quarantine_status():
    """List security quarantine status and behavior baselines."""
    return {"quarantine": PlanetarySecurityGovernanceService.get_security_quarantine_status()}

@router.post("/security/isolate-agent")
def isolate_agent(req: AgentQuarantineRequest):
    """Isolate and quarantine compromised agent."""
    return PlanetarySecurityGovernanceService.quarantine_agent(req.agent_id, req.reason)

@router.post("/copilot/strategic-simulation")
def run_strategic_simulation(req: StrategicSimulationRequest):
    """Run Global Strategic Simulator & early warning query."""
    return PlanetaryCopilotStrategyService.run_strategic_simulation(req.prompt)

@router.get("/autonomy/governance-status")
def get_governance_status():
    """Get Global Kill Switch, Safe Mode, and Audit integrity status."""
    return PlanetaryAutonomyKillswitchService.get_governance_status()

@router.post("/autonomy/kill-switch")
def toggle_kill_switch(req: GlobalKillSwitchRequest):
    """Toggle Global Emergency Kill Switch (GLOBAL_KILL_SWITCH)."""
    return PlanetaryAutonomyKillswitchService.toggle_global_kill_switch(req.kill_switch_active, req.reason)

@router.post("/autonomy/safe-mode")
def toggle_safe_mode(req: SafeModeRequest):
    """Toggle Safe Mode (read-only restricted operations)."""
    return PlanetaryAutonomyKillswitchService.toggle_safe_mode(req.safe_mode_active, req.reason)

@router.get("/autonomy/audit-trail")
def get_audit_trail():
    """List immutable governance audit trail events."""
    return {"audits": PlanetaryAutonomyKillswitchService.get_audit_trail()}
