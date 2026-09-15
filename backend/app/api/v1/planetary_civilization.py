"""
Planetary Civilization OS Router (Phase 96)
API Endpoints for civilization state modeling, global knowledge commons, evidence-based deliberation, institutional design lab, collective intelligence, problem-solving marketplace, forecasting scenarios, and digital rights.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Query, Body, HTTPException

from app.services.planetary_civilization import (
    CivilizationCommonsService,
    ScientificDiscoveryDeliberationService,
    InstitutionalDesignLabService,
    CollectiveIntelligenceGovernanceService,
    ProblemSolvingMarketplaceService,
    CivilizationForecastingScenarioService,
    SkillsDigitalRightsPreservationService,
)

router = APIRouter(prefix="/planetary-civilization", tags=["Planetary Civilization OS & Collective Intelligence (Phase 96)"])

commons_service = CivilizationCommonsService()
deliberation_service = ScientificDiscoveryDeliberationService()
inst_service = InstitutionalDesignLabService()
governance_service = CollectiveIntelligenceGovernanceService()
marketplace_service = ProblemSolvingMarketplaceService()
forecasting_service = CivilizationForecastingScenarioService()
rights_service = SkillsDigitalRightsPreservationService()


# ---------------------------------------------------------
# 1. CIVILIZATION STATE & GLOBAL KNOWLEDGE COMMONS
# ---------------------------------------------------------

@router.get("/state/overview", summary="Get Multi-Dimensional Civilization State Baseline")
def get_civilization_state():
    return commons_service.get_civilization_state()


@router.post("/knowledge/contribute", summary="Contribute Global Knowledge Node")
def contribute_knowledge(
    title: str = Body(..., embed=True),
    domain_category: str = Body(..., embed=True),
    claim_summary: str = Body(..., embed=True),
    author: str = Body("Dr. Elena Vance", embed=True),
    evidence_list: List[str] = Body(["Global Meta-Analysis Dataset #42"], embed=True),
    confidence: float = Body(0.92, embed=True),
):
    return commons_service.contribute_knowledge_node(
        title=title,
        domain_category=domain_category,
        claim_summary=claim_summary,
        author=author,
        evidence_list=evidence_list,
        confidence=confidence,
    )


@router.post("/knowledge/{parent_id}/fork", summary="Fork Knowledge Node for Alternative Interpretation")
def fork_knowledge(
    parent_id: str,
    forked_by: str = Body("Research Lab Beta", embed=True),
    alternative_interpretation: str = Body("Disagreement on microclimate feedback lag duration.", embed=True),
):
    return commons_service.fork_knowledge_node(parent_id, forked_by, alternative_interpretation)


@router.get("/knowledge/{claim_id}/claim-graph", summary="Get Claim-Evidence Graph")
def get_claim_graph(claim_id: str):
    return commons_service.generate_claim_evidence_graph(claim_id)


# ---------------------------------------------------------
# 2. SCIENTIFIC DISCOVERY & EVIDENCE-BASED DELIBERATION
# ---------------------------------------------------------

@router.post("/scientific/cross-disciplinary-connections", summary="Discover Cross-Disciplinary Research Connections")
def discover_connections(
    primary_discipline: str = Body("Physics", embed=True),
    target_disciplines: List[str] = Body(["Economics", "Climate Science"], embed=True),
):
    return deliberation_service.discover_cross_disciplinary_connections(primary_discipline, target_disciplines)


@router.post("/deliberation/argument-map/create", summary="Create Evidence-Based Argument Map")
def create_argument_map(
    topic_title: str = Body(..., embed=True),
    claims: List[Dict[str, Any]] = Body(..., embed=True),
    participants: List[str] = Body(["Expert A", "Analyst B"], embed=True),
):
    return deliberation_service.create_deliberation_argument_map(topic_title, claims, participants)


@router.post("/deliberation/{arg_id}/generate-memo", summary="Generate Decision Memo with Minority View Inclusion")
def generate_decision_memo(arg_id: str, problem_statement: str = Body("Policy selection for energy transition.", embed=True)):
    return deliberation_service.generate_decision_memo(arg_id, problem_statement)


# ---------------------------------------------------------
# 3. INSTITUTIONAL DESIGN LAB & GOVERNANCE SIMULATION
# ---------------------------------------------------------

@router.post("/institutional-lab/simulate", summary="Simulate Institutional Structure & Vulnerabilities")
def simulate_institution(
    institution_name: str = Body("Global Climate Finance Authority", embed=True),
    governance_model: str = Body("Multi-Stakeholder Board", embed=True),
    decision_rights_structure: Dict[str, Any] = Body({"voting": "2/3 Majority", "veto": "Public Interest Council"}, embed=True),
    incentive_mechanisms: List[str] = Body(["Transparent Performance Grants"], embed=True),
):
    return inst_service.simulate_institutional_design(
        institution_name=institution_name,
        governance_model=governance_model,
        decision_rights_structure=decision_rights_structure,
        incentive_mechanisms=incentive_mechanisms,
    )


@router.post("/policy/context-transfer-analysis", summary="Analyze Policy Context Transferability")
def policy_transfer(
    policy_name: str = Body("Grid Microgrid Mandate", embed=True),
    origin_context: str = Body("Region Alpha", embed=True),
    target_context: str = Body("Region Beta", embed=True),
):
    return inst_service.analyze_policy_context_transfer(policy_name, origin_context, target_context)


# ---------------------------------------------------------
# 4. COLLECTIVE INTELLIGENCE & CONSTITUTIONAL GOVERNANCE
# ---------------------------------------------------------

@router.post("/collective-intelligence/team/configure", summary="Configure Human-AI Team & Role Specialization")
def configure_team(
    team_name: str = Body("Planetary Foresight Taskforce", embed=True),
    human_experts: List[str] = Body(["Dr. Aris Thorne", "Prof. Sophia Lin"], embed=True),
    ai_roles: List[str] = Body(["Researcher", "Simulator", "Critic", "Reviewer"], embed=True),
):
    return governance_service.configure_human_ai_team(team_name, human_experts, ai_roles)


@router.post("/collective-intelligence/cross-check", summary="Execute Independent Multi-AI Cross-Checking")
def cross_check(
    primary_recommendation: str = Body("Implement Staged Microgrid Pilot", embed=True),
    participating_models: List[str] = Body(["Model-Alpha-70B", "Model-Beta-100B"], embed=True),
):
    return governance_service.execute_ai_cross_checking(primary_recommendation, participating_models)


@router.post("/collective-intelligence/human-override", summary="Trigger Human Override & Pause AI Action")
def trigger_human_override(
    team_id: str = Body(..., embed=True),
    human_user_id: str = Body("usr-chairperson-01", embed=True),
    reason: str = Body("Requires manual institutional audit.", embed=True),
):
    return governance_service.trigger_human_override(team_id, human_user_id, reason)


# ---------------------------------------------------------
# 5. PROBLEM SOLVING MARKETPLACE
# ---------------------------------------------------------

@router.post("/problem-marketplace/publish", summary="Publish Civilization-Scale Problem")
def publish_problem(
    title: str = Body(..., embed=True),
    category: str = Body("Energy", embed=True),
    problem_description: str = Body("Decarbonization of heavy industrial process heat.", embed=True),
    subproblems: List[str] = Body(["High temperature thermal storage", "Clean hydrogen integration"], embed=True),
    publishing_institution: str = Body("Global Clean Energy Initiative", embed=True),
):
    return marketplace_service.publish_civilization_problem(
        title=title,
        category=category,
        problem_description=problem_description,
        subproblems=subproblems,
        publishing_institution=publishing_institution,
    )


@router.post("/problem-marketplace/submit-solution", summary="Submit Qualified Solution Proposal")
def submit_solution(
    problem_id: str = Body(..., embed=True),
    solution_title: str = Body("Solid-State Thermal Storage Matrix", embed=True),
    proposer: str = Body("Advanced Thermal Dynamics Lab", embed=True),
    readiness_stage: str = Body("Pilot", embed=True),
    solution_graph: Dict[str, Any] = Body({"efficiency": "92%", "cost_per_kwh": "$18"}, embed=True),
    is_safe_to_fail: bool = Body(True, embed=True),
):
    return marketplace_service.submit_solution_proposal(
        problem_id=problem_id,
        solution_title=solution_title,
        proposer=proposer,
        readiness_stage=readiness_stage,
        solution_graph=solution_graph,
        is_safe_to_fail=is_safe_to_fail,
    )


@router.post("/problem-marketplace/failure-database/log", summary="Log Failed Experiment Lessons to Database")
def log_failure(
    project_title: str = Body("High Pressure Catalyst Test #4", embed=True),
    category: str = Body("Energy", embed=True),
    failure_type: str = Body("Material Degradation", embed=True),
    root_cause_analysis: str = Body("Thermal stress exceeded alloy limits at 850C.", embed=True),
    lessons_learned: str = Body("Switch to ceramic composite matrix for >800C applications.", embed=True),
):
    return marketplace_service.log_failed_experiment_to_database(
        project_title=project_title,
        category=category,
        failure_type=failure_type,
        root_cause_analysis=root_cause_analysis,
        lessons_learned=lessons_learned,
    )


# ---------------------------------------------------------
# 6. FORECASTING & CIVILIZATION SCENARIO ENGINE
# ---------------------------------------------------------

@router.post("/forecasting/scenarios/generate", summary="Generate Long-Horizon Civilization Scenario (1Y to 100Y+)")
def generate_scenario(
    scenario_title: str = Body("Quantum & Fusion Civilization Paradigm", embed=True),
    horizon_years: int = Body(50, embed=True),
    scenario_axes: Dict[str, Any] = Body({"energy": "Abundant", "compute": "Ubiquitous Mesh"}, embed=True),
    resource_accounting: Dict[str, Any] = Body({"energy_mwh": 1e9, "materials_recycling_percent": 98.5}, embed=True),
):
    return forecasting_service.generate_civilization_scenario(
        scenario_title=scenario_title,
        horizon_years=horizon_years,
        scenario_axes=scenario_axes,
        resource_accounting=resource_accounting,
    )


@router.post("/forecasting/calibration/evaluate", summary="Evaluate Forecast Calibration & Accuracy")
def evaluate_calibration(
    forecast_id: str = Body("fcst-2026-grid", embed=True),
    forecast_value: float = Body(120.0, embed=True),
    observed_value: float = Body(118.5, embed=True),
):
    return forecasting_service.evaluate_forecast_calibration(forecast_id, forecast_value, observed_value)


# ---------------------------------------------------------
# 7. SKILLS GRAPH & DIGITAL RIGHTS
# ---------------------------------------------------------

@router.get("/skills/reskilling-pathways", summary="Forecast Future Skills & Reskilling Pathways")
def reskilling_pathways(current_occupation: str = Query("Power Grid Dispatcher"), horizon_years: int = Query(5)):
    return rights_service.forecast_future_skills_and_reskilling_pathways(current_occupation, horizon_years)


@router.post("/digital-rights/algorithmic-appeal/submit", summary="Submit Algorithmic Decision Appeal")
def submit_appeal(
    user_id: str = Body("usr-citizen-42", embed=True),
    automated_decision_id: str = Body("dec-auto-8921", embed=True),
    reason_for_appeal: str = Body("Request human review of resource allocation score.", embed=True),
):
    return rights_service.process_algorithmic_appeal_request(user_id, automated_decision_id, reason_for_appeal)
