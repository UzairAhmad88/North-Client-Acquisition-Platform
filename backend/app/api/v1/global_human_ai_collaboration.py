"""
Phase 92 — Global Human-AI Collaboration Network & Collective Intelligence REST API Router
"""

from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.services.global_human_ai_collaboration import (
    GlobalCollaborationFabricService,
    GlobalCollectiveIntelligenceService,
    GlobalFederatedSimulationService,
    GlobalTaskOrchestrationService,
    GlobalDataRoomCommunityService,
    GlobalDeliberationForecastingService,
    GlobalOrganizationalGovernanceService,
)

router = APIRouter(prefix="/collective-intelligence", tags=["Global Human-AI Collaboration OS"])

class IdentityPayload(BaseModel):
    participant_name: str = Field(..., example="Dr. Aris Thorne")
    participant_type: str = Field("human", example="expert")
    organization_id: str = Field("org-alpha", example="org-mit")
    capabilities: List[str] = Field(default=["Research", "Data Science"])
    roles: List[str] = Field(default=["Lead Researcher"])

class TeamMatchPayload(BaseModel):
    title: str = Field(..., example="Planetary Clean Energy Transition")
    domain: str = Field(..., example="Climate Resilience")
    required_capabilities: List[str] = Field(default=["Physics", "Red-Team Review"])

class ProjectRoomPayload(BaseModel):
    room_name: str = Field(..., example="Global Clean Energy Transition Workbench")
    project_scope: str = Field("civilization_workbench", example="civilization_workbench")
    owner_id: str = Field("usr-lead-001")
    participants: List[str] = Field(default=["usr-lead-001", "usr-expert-002"])

class DecisionPayload(BaseModel):
    room_id: str = Field("room-default")
    title: str = Field("Select Zero-Emission Grid Topology")
    options: List[str] = Field(default=["Option A: HVDC Mesh", "Option B: Decentralized Microgrid"])
    chosen_option: str = Field("Option A: HVDC Mesh")
    evidence: List[str] = Field(default=["Phase 90 Simulation Run #491"])
    assumptions: List[str] = Field(default=["Battery cost drops 8%/yr"])

class ContributionPayload(BaseModel):
    room_id: str = Field("room-default")
    artifact_id: str = Field("doc-spec-001")
    contribution_type: str = Field("hybrid")
    author_id: str = Field("usr-101")
    agent_id: str = Field("agt-editor-01")

class FederatedWorkspacePayload(BaseModel):
    name: str = Field("International Fusion Consortium")
    institutions: List[str] = Field(default=["MIT Plasma Lab", "CERN", "Max Planck Institute"])

class SimulationPayload(BaseModel):
    workspace_id: str = Field("fedws-default")
    scenario_type: str = Field("stress")

class TaskDelegatePayload(BaseModel):
    title: str = Field("Run Counterfactual Power Grid Simulation")
    ownership_type: str = Field("joint")
    human_owner_id: str = Field("usr-lead-001")
    ai_owner_id: str = Field("agt-sim-303")
    requires_approval: bool = Field(True)

class HandoffPayload(BaseModel):
    from_agent_id: str = Field("agt-researcher-01")
    to_agent_id: str = Field("agt-reviewer-02")
    task_id: str = Field("tsk-default")

class DataRoomPayload(BaseModel):
    room_name: str = Field("Project Horizon Due Diligence Data Room")
    owner_org_id: str = Field("org-alpha")

class MCDAPayload(BaseModel):
    topic: str = Field("Regional Water Desalination Strategy")
    options: List[str] = Field(default=["Solar Desalination Plant", "Deep Aquifer Extraction"])
    voting_type: str = Field("secret_ballot")

class ForecastPayload(BaseModel):
    project_id: str = Field("prj-clean-energy-01")

class PostmortemPayload(BaseModel):
    title: str = Field("Grid Outage Incident #402")

# --- API Endpoints ---

@router.post("/identities", response_model=Dict[str, Any])
def create_identity(payload: IdentityPayload):
    """Creates or updates a participant identity in the collaboration fabric."""
    return GlobalCollaborationFabricService.create_or_get_identity(payload.dict())

@router.get("/identities/{participant_id}", response_model=Dict[str, Any])
def get_identity(participant_id: str, domain: str = Query("General Science")):
    """Gets participant details and expertise graph nodes."""
    return GlobalCollaborationFabricService.get_expertise_node(participant_id, domain)

@router.post("/experts/match", response_model=Dict[str, Any])
def match_team(payload: TeamMatchPayload):
    """Forms complementary team combining experts, engineers, researchers, and AI agents."""
    return GlobalCollaborationFabricService.form_complementary_team(payload.dict())

@router.post("/workspaces/room", response_model=Dict[str, Any])
def create_project_room(payload: ProjectRoomPayload):
    """Creates a shared project room with project knowledge graph and memory controls."""
    return GlobalCollectiveIntelligenceService.create_project_room(payload.dict())

@router.post("/decisions/record", response_model=Dict[str, Any])
def record_decision(payload: DecisionPayload):
    """Records a structured decision with evidence, assumptions, quality score, and revision history."""
    return GlobalCollectiveIntelligenceService.record_structured_decision(payload.dict())

@router.post("/contributions/attribute", response_model=Dict[str, Any])
def attribute_contribution(payload: ContributionPayload):
    """Attributes Human/AI/Hybrid contribution, records argument map and preserves dissent."""
    return GlobalCollectiveIntelligenceService.attribute_contribution(payload.dict())

@router.post("/federated/workspace", response_model=Dict[str, Any])
def create_federated_workspace(payload: FederatedWorkspacePayload):
    """Creates cross-institution scientific collaboration workspace preserving data boundaries."""
    return GlobalFederatedSimulationService.create_federated_workspace(payload.dict())

@router.post("/federated/simulation", response_model=Dict[str, Any])
def run_simulation(payload: SimulationPayload):
    """Runs collaborative digital twin simulation under Red-Team vs Blue-Team critique."""
    return GlobalFederatedSimulationService.run_red_blue_scenario_simulation(payload.dict())

@router.post("/tasks/delegate", response_model=Dict[str, Any])
def delegate_task(payload: TaskDelegatePayload):
    """Delegates task with ownership controls, delegation policy, and human approval gates."""
    return GlobalTaskOrchestrationService.delegate_task(payload.dict())

@router.post("/tasks/handoff", response_model=Dict[str, Any])
def handoff_task(payload: HandoffPayload):
    """Executes multi-agent task handoff with verification of inherited context and constraints."""
    return GlobalTaskOrchestrationService.execute_agent_handoff(payload.dict())

@router.post("/data-rooms", response_model=Dict[str, Any])
def create_data_room(payload: DataRoomPayload):
    """Creates secure collaborative data room with access audit logging and project RAG."""
    return GlobalDataRoomCommunityService.create_secure_data_room(payload.dict())

@router.post("/community/question", response_model=Dict[str, Any])
def route_question(title: str = Query("How does folding energy scale under non-equilibrium thermodynamics?"), domain: str = Query("Computational Biology")):
    """Routes high-value community questions to domain experts based on evidence quality."""
    return GlobalDataRoomCommunityService.route_community_question({"title": title, "domain": domain})

@router.post("/deliberation/mcda", response_model=Dict[str, Any])
def run_mcda(payload: MCDAPayload):
    """Executes Multi-Criteria Decision Analysis (MCDA) with weight transparency and voting."""
    return GlobalDeliberationForecastingService.run_mcda_deliberation(payload.dict())

@router.post("/project/forecast", response_model=Dict[str, Any])
def forecast_project(payload: ForecastPayload):
    """Generates probabilistic project forecast with uncertainty ranges and early warning signals."""
    return GlobalDeliberationForecastingService.generate_project_forecast(payload.dict())

@router.get("/executive/briefing", response_model=Dict[str, Any])
def get_executive_briefing(role: str = Query("Chief Executive / Board")):
    """Generates targeted executive collaboration briefing and expert opinions."""
    return GlobalOrganizationalGovernanceService.generate_executive_briefing({"role": role})

@router.post("/postmortems/analyze", response_model=Dict[str, Any])
def execute_postmortem(payload: PostmortemPayload):
    """Executes blame-free postmortem analysis and updates organizational learning graph."""
    return GlobalOrganizationalGovernanceService.execute_blame_free_postmortem(payload.dict())

@router.get("/workbench/civilization", response_model=Dict[str, Any])
def get_civilization_workbench(domain: str = Query("Planetary Climate Resilience")):
    """Gets status of civilization-scale problem workbench under Level 5 human agency preservation."""
    return GlobalOrganizationalGovernanceService.get_civilization_workbench_status({"domain": domain})
