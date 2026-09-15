"""
Phase 90: Planetary AI Civilization Layer & Scientific Discovery REST API Router.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.services.planetary_ai_civilization import (
    PlanetaryKnowledgeFabricService,
    PlanetaryHypothesisService,
    PlanetaryCausalReasoningService,
    PlanetaryLongHorizonService,
    PlanetaryDatasetCollaborationService,
    PlanetaryCopilotBriefingService,
    PlanetaryGovernanceSafetyService,
)

router = APIRouter(prefix="/civilization-intelligence", tags=["Planetary AI Civilization OS"])

class SimulateExperimentRequest(BaseModel):
    hypothesis_id: str

class CounterfactualRequest(BaseModel):
    intervention: str
    variable_changed: str

class EvaluateReversibilityRequest(BaseModel):
    action_name: str

class ScienceBriefingRequest(BaseModel):
    prompt: str
    audience_level: str = "EXECUTIVE"

class EthicalQuorumRequest(BaseModel):
    research_id: str
    proposed_action: str

@router.get("/claims")
def get_knowledge_claims():
    """List multi-domain knowledge fabric claims and evidence quality scores."""
    return {"claims": PlanetaryKnowledgeFabricService.get_knowledge_claims()}

@router.get("/contradictions")
def detect_contradictions(domain: str = Query("SCIENCE_MATERIALS", description="Knowledge domain")):
    """Check for contradictions across indexed scientific claims."""
    return PlanetaryKnowledgeFabricService.detect_contradictions(domain)

@router.get("/hypotheses")
def get_hypotheses():
    """List hypotheses (strictly labeled as hypotheses, NOT facts)."""
    return {"hypotheses": PlanetaryHypothesisService.get_hypotheses()}

@router.get("/experiments")
def get_experiments():
    """List research experiments and reproducibility lineage."""
    return {"experiments": PlanetaryHypothesisService.get_experiments()}

@router.post("/experiments/simulate")
def simulate_experiment(req: SimulateExperimentRequest):
    """Simulate scientific experiment in silico."""
    return PlanetaryHypothesisService.simulate_experiment(req.hypothesis_id)

@router.get("/causal/graph")
def get_causal_nodes():
    """Get directed causal graph nodes and effect sizes."""
    return {"causal_nodes": PlanetaryCausalReasoningService.get_causal_nodes()}

@router.post("/causal/counterfactual")
def query_counterfactual(req: CounterfactualRequest):
    """Query counterfactual analysis engine."""
    return PlanetaryCausalReasoningService.query_counterfactual(req.intervention, req.variable_changed)

@router.get("/long-horizon/scenarios")
def get_long_horizon_scenarios():
    """List long-horizon strategic scenarios (1–20 years)."""
    return {"scenarios": PlanetaryLongHorizonService.get_long_horizon_scenarios()}

@router.post("/long-horizon/evaluate-reversibility")
def evaluate_reversibility(req: EvaluateReversibilityRequest):
    """Evaluate decision reversibility and institutional quorum requirements."""
    return PlanetaryLongHorizonService.evaluate_decision_reversibility(req.action_name)

@router.get("/datasets")
def get_datasets():
    """List governed research dataset registries."""
    return {"datasets": PlanetaryDatasetCollaborationService.get_datasets()}

@router.post("/copilot/briefing")
def generate_science_briefing(req: ScienceBriefingRequest):
    """Generate audience-aware executive science briefing."""
    return PlanetaryCopilotBriefingService.generate_science_briefing(req.prompt, req.audience_level)

@router.get("/governance/safety-gate-status")
def get_safety_gate_status():
    """Get scientific safety gate and ethical quorum status."""
    return PlanetaryGovernanceSafetyService.get_safety_gate_status()

@router.post("/governance/request-ethical-approval")
def request_ethical_approval(req: EthicalQuorumRequest):
    """Request multi-stakeholder ethical review quorum approval."""
    return PlanetaryGovernanceSafetyService.request_ethical_quorum_approval(req.research_id, req.proposed_action)

@router.get("/governance/audit-trail")
def get_audit_trail():
    """List immutable research governance audit trail."""
    return {"audits": PlanetaryGovernanceSafetyService.get_audit_trail()}
