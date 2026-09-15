"""
Planetary Resilience & Civilization Recovery Router (Phase 95)
API Endpoints for planetary resilience fabric, crisis command center, humanitarian logistics, infrastructure continuity, knowledge preservation, compound risks, and existential-risk research.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Query, Body, HTTPException

from app.services.planetary_resilience import (
    PlanetaryResilienceFabricService,
    CrisisCommandService,
    HumanitarianLogisticsService,
    InfrastructureContinuityService,
    KnowledgeGovernanceContinuityService,
    CompoundRiskBufferService,
    ExistentialRiskResearchService,
)

router = APIRouter(prefix="/planetary-resilience", tags=["Planetary Resilience & Crisis Recovery (Phase 95)"])

fabric_service = PlanetaryResilienceFabricService()
crisis_service = CrisisCommandService()
logistics_service = HumanitarianLogisticsService()
infra_service = InfrastructureContinuityService()
knowledge_service = KnowledgeGovernanceContinuityService()
compound_service = CompoundRiskBufferService()
existential_service = ExistentialRiskResearchService()


# ---------------------------------------------------------
# 1. PLANETARY RESILIENCE FABRIC & SCORECARDS
# ---------------------------------------------------------

@router.post("/systems/register", summary="Register Critical System Node")
def register_critical_system(
    name: str = Body(..., embed=True),
    category: str = Body(..., embed=True),
    criticality_level: str = Body("Essential", embed=True),
    owner_organization: str = Body("Global Infrastructure Authority", embed=True),
    dependencies: Optional[List[str]] = Body(None, embed=True),
    failure_modes: Optional[List[str]] = Body(None, embed=True),
):
    return fabric_service.register_critical_system(
        name=name,
        category=category,
        criticality_level=criticality_level,
        owner_organization=owner_organization,
        dependencies=dependencies,
        failure_modes=failure_modes,
    )


@router.get("/systems/{node_id}/scorecard", summary="Get Multi-Dimensional Resilience Scorecard")
def get_resilience_scorecard(node_id: str):
    return fabric_service.get_resilience_scorecard(node_id)


@router.post("/continuity-plans/create", summary="Create Business Continuity Plan")
def create_continuity_plan(
    organization_name: str = Body(..., embed=True),
    critical_functions: List[str] = Body(..., embed=True),
    dependencies: List[str] = Body(..., embed=True),
    fallback_locations: List[str] = Body(..., embed=True),
    backup_personnel: List[str] = Body(..., embed=True),
    rto_rpo_targets: Dict[str, Any] = Body(..., embed=True),
):
    return fabric_service.create_business_continuity_plan(
        organization_name=organization_name,
        critical_functions=critical_functions,
        dependencies=dependencies,
        fallback_locations=fallback_locations,
        backup_personnel=backup_personnel,
        rto_rpo_targets=rto_rpo_targets,
    )


@router.post("/recovery-sequence/calculate", summary="Calculate Dependency-Aware Recovery Sequence")
def calculate_recovery_sequence(impacted_nodes: List[str] = Body(..., embed=True)):
    return fabric_service.calculate_dependency_aware_recovery_sequence(impacted_nodes)


# ---------------------------------------------------------
# 2. INCIDENT COMMAND CENTER & CRISIS DECISIONS
# ---------------------------------------------------------

@router.post("/crisis/declare", summary="Declare Global Crisis Incident")
def declare_crisis_incident(
    title: str = Body(..., embed=True),
    category: str = Body(..., embed=True),
    severity_level: int = Body(3, embed=True),
    primary_location: str = Body("Global Region Alpha", embed=True),
    affected_jurisdictions: List[str] = Body(["US", "EU"], embed=True),
    declared_by_human_id: str = Body("usr-commander-01", embed=True),
    description: str = Body("Severe grid failure compounding with extreme thermal wave.", embed=True),
):
    return crisis_service.declare_crisis_incident(
        title=title,
        category=category,
        severity_level=severity_level,
        primary_location=primary_location,
        affected_jurisdictions=affected_jurisdictions,
        declared_by_human_id=declared_by_human_id,
        initial_description=description,
    )


@router.post("/crisis/{incident_id}/evaluate-escalation", summary="Evaluate Crisis Escalation Thresholds")
def evaluate_escalation(
    incident_id: str,
    metrics: Dict[str, Any] = Body(..., embed=True),
):
    return crisis_service.evaluate_escalation_thresholds(incident_id, metrics)


@router.post("/crisis/{incident_id}/record-decision", summary="Record Emergency Decision with Reversibility Analysis")
def record_decision(
    incident_id: str,
    decision_maker: str = Body(..., embed=True),
    decision_title: str = Body(..., embed=True),
    options_considered: List[str] = Body(..., embed=True),
    chosen_option: str = Body(..., embed=True),
    reversibility: str = Body("Reversible", embed=True),
    evidence_summary: str = Body("Supported by telemetry signals.", embed=True),
):
    return crisis_service.record_emergency_decision(
        incident_id=incident_id,
        decision_maker=decision_maker,
        decision_title=decision_title,
        options_considered=options_considered,
        chosen_option=chosen_option,
        reversibility=reversibility,
        evidence_summary=evidence_summary,
    )


@router.get("/crisis/{incident_id}/ai-assistant", summary="Query Crisis AI Assistant (Advisory Only)")
def query_crisis_ai(incident_id: str, query: str = Query("What is the highest priority recovery step?")):
    return crisis_service.run_crisis_ai_assistant(incident_id, query)


# ---------------------------------------------------------
# 3. HUMANITARIAN COORDINATION & LOGISTICS
# ---------------------------------------------------------

@router.post("/humanitarian/resources/register", summary="Register Humanitarian Supply")
def register_humanitarian_supply(
    resource_type: str = Body("Water", embed=True),
    quantity: float = Body(50000.0, embed=True),
    unit: str = Body("Liters", embed=True),
    location: str = Body("Depot Bravo", embed=True),
    owner_organization: str = Body("Red Cross Alliance", embed=True),
):
    return logistics_service.register_humanitarian_resource(
        resource_type=resource_type,
        quantity=quantity,
        unit=unit,
        location=location,
        owner_organization=owner_organization,
    )


@router.post("/humanitarian/needs/log", summary="Log Verified Humanitarian Need")
def log_humanitarian_need(
    incident_id: str = Body(..., embed=True),
    location: str = Body(..., embed=True),
    resource_type: str = Body(..., embed=True),
    requested_quantity: float = Body(..., embed=True),
    unit: str = Body(..., embed=True),
    urgency_level: str = Body("Critical", embed=True),
    requesting_entity: str = Body("Municipal Relief Agency", embed=True),
):
    return logistics_service.log_humanitarian_need(
        incident_id=incident_id,
        location=location,
        resource_type=resource_type,
        requested_quantity=requested_quantity,
        unit=unit,
        urgency_level=urgency_level,
        requesting_entity=requesting_entity,
    )


@router.post("/humanitarian/needs/{need_id}/match", summary="Match Resources to Needs")
def match_resources(need_id: str):
    return logistics_service.match_resources_to_needs(need_id)


@router.post("/humanitarian/logistics/simulate-route", summary="Simulate Emergency Logistics Distribution Route")
def simulate_route(
    origin: str = Body("Hub A", embed=True),
    destination: str = Body("District 4", embed=True),
    resource_type: str = Body("Medical Kits", embed=True),
    quantity: float = Body(500.0, embed=True),
    simulated_shocks: Optional[List[str]] = Body(None, embed=True),
):
    return logistics_service.simulate_logistics_distribution(
        origin=origin,
        destination=destination,
        resource_type=resource_type,
        quantity=quantity,
        simulated_shocks=simulated_shocks,
    )


# ---------------------------------------------------------
# 4. INFRASTRUCTURE CONTINUITY & AI DEGRADATION MODES
# ---------------------------------------------------------

@router.get("/infrastructure/healthcare-status", summary="Get Healthcare & Biosecurity Capacity Status")
def healthcare_status(region_code: str = Query("US-EAST")):
    return infra_service.get_healthcare_capacity_status(region_code)


@router.post("/infrastructure/grid/simulate", summary="Simulate Energy Grid Disruption & Backup Activation")
def simulate_grid(grid_region: str = Body("Grid-Alpha", embed=True), loss_percentage: float = Body(35.0, embed=True)):
    return infra_service.simulate_grid_energy_emergency(grid_region, loss_percentage)


@router.post("/ai-continuity/configure", summary="Configure AI System Degradation Modes & Defined Fallbacks")
def configure_ai_continuity(
    service_name: str = Body(..., embed=True),
    current_mode: str = Body("Full AI", embed=True),
    defined_manual_fallback: str = Body("Manual Operator Dispatch Protocol #4", embed=True),
    backup_model_provider: str = Body("Local On-Prem Llama-3-70B", embed=True),
):
    return infra_service.configure_ai_system_continuity(
        service_name=service_name,
        current_mode=current_mode,
        defined_manual_fallback=defined_manual_fallback,
        backup_model_provider=backup_model_provider,
    )


@router.post("/ai-continuity/degrade-stepdown", summary="Trigger Graceful AI Degradation Stepdown")
def degrade_stepdown(service_name: str = Body(..., embed=True), reason: str = Body("High uncertainty signal", embed=True)):
    return infra_service.trigger_ai_degradation_stepdown(service_name, reason)


# ---------------------------------------------------------
# 5. KNOWLEDGE PRESERVATION & GOVERNANCE CONTINUITY
# ---------------------------------------------------------

@router.post("/knowledge/archive", summary="Archive Critical Knowledge Node")
def archive_knowledge(
    title: str = Body(..., embed=True),
    category: str = Body("Engineering", embed=True),
    knowledge_summary: str = Body(..., embed=True),
    data_hash: str = Body("sha256-abcdef1234567890", embed=True),
    storage_locations: List[str] = Body(["S3-Vault-East", "Offline-Tape-Vault-Nordic"], embed=True),
    primary_expert_contacts: List[str] = Body(["dr.vance@uzaii.org"], embed=True),
):
    return knowledge_service.archive_critical_knowledge(
        title=title,
        category=category,
        knowledge_summary=knowledge_summary,
        data_hash=data_hash,
        storage_locations=storage_locations,
        primary_expert_contacts=primary_expert_contacts,
    )


@router.post("/governance/emergency-power/grant", summary="Grant Temporary Emergency Authority")
def grant_emergency_power(
    granted_to_user_id: str = Body(..., embed=True),
    authority_scope: str = Body("Operational", embed=True),
    duration_hours: int = Body(24, embed=True),
    approved_by_board_id: str = Body("gov-board-01", embed=True),
):
    return knowledge_service.grant_temporary_emergency_authority(
        granted_to_user_id=granted_to_user_id,
        authority_scope=authority_scope,
        duration_hours=duration_hours,
        approved_by_board_id=approved_by_board_id,
    )


@router.post("/governance/return-to-normal", summary="Execute Return-to-Normal Workflow")
def return_to_normal(incident_id: str = Body(..., embed=True)):
    return knowledge_service.execute_return_to_normal_workflow(incident_id)


# ---------------------------------------------------------
# 6. COMPOUND RISK & RESILIENCE BUFFERS
# ---------------------------------------------------------

@router.post("/buffers/register", summary="Register Systemic Resilience Buffer")
def register_buffer(
    system_id: str = Body(..., embed=True),
    buffer_name: str = Body(..., embed=True),
    buffer_type: str = Body("Energy", embed=True),
    total_capacity: float = Body(10000.0, embed=True),
    unit: str = Body("MWh", embed=True),
):
    return compound_service.register_resilience_buffer(
        system_id=system_id,
        buffer_name=buffer_name,
        buffer_type=buffer_type,
        total_capacity=total_capacity,
        unit=unit,
    )


@router.post("/compound-risk/simulate-cascading", summary="Simulate Compound Cascading Crisis")
def simulate_cascading(
    primary_shocks: List[str] = Body(["Heatwave", "Cyber Attack"], embed=True),
    duration_days: int = Body(7, embed=True),
):
    return compound_service.simulate_compound_cascading_crisis(primary_shocks, duration_days)


# ---------------------------------------------------------
# 7. EXISTENTIAL-RISK RESEARCH & GLOBAL NETWORK
# ---------------------------------------------------------

@router.post("/existential-risk/research/create", summary="Create Existential Risk Scenario Record")
def create_existential_research(
    risk_category: str = Body("Advanced AI Risks", embed=True),
    scenario_title: str = Body("Goal Misalignment in Autonomous Grid Dispatcher", embed=True),
    probability_assessment: str = Body("Plausible", embed=True),
    consequence_summary: str = Body("High systemic disruption if safeguards are unverified.", embed=True),
    containment_strategies: List[str] = Body(["Air-gapped hardware override", "Multi-party key revocation"], embed=True),
    expert_reviewers: List[str] = Body(["Dr. Aris Thorne", "Dr. Elena Rostova"], embed=True),
):
    return existential_service.create_existential_risk_research_record(
        risk_category=risk_category,
        scenario_title=scenario_title,
        probability_assessment=probability_assessment,
        consequence_summary=consequence_summary,
        containment_strategies=containment_strategies,
        expert_reviewers=expert_reviewers,
    )


@router.post("/existential-risk/ai-control/simulate", summary="Run AI Control & Containment Simulation")
def simulate_ai_control(
    ai_system_name: str = Body("Grid-AI-Agent-01", embed=True),
    test_failure_mode: str = Body("Goal Misalignment", embed=True),
):
    return existential_service.run_ai_control_and_containment_simulation(ai_system_name, test_failure_mode)


@router.post("/simulation-lab/run", summary="Run Crisis Simulation Sandbox")
def run_simulation_lab(
    scenario_name: str = Body("Global Cyber-Physical Cascading Blackout", embed=True),
    initial_conditions: Dict[str, Any] = Body({"grid_reserve_percent": 15.0}, embed=True),
    seed: int = Body(42, embed=True),
):
    return existential_service.run_crisis_simulation_lab(
        scenario_name=scenario_name,
        initial_conditions=initial_conditions,
        seed=seed,
    )
