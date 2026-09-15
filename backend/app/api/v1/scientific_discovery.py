"""
Scientific Discovery Engine Router (Phase 97)
API Endpoints for question decomposition, literature graphs, AI hypotheses, experiment design, computational labs, AI scientist networks, multi-model simulations, mathematical discovery, replications, and discovery copilot.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Query, Body, HTTPException

from app.services.scientific_discovery import (
    QuestionLiteratureEngineService,
    HypothesisExperimentDesignService,
    DigitalLabReproducibilityService,
    AiScientistNetworkService,
    SimulationCausalMathEngineService,
    ReplicationMetaAnalysisService,
    DiscoveryCopilotGovernanceService,
)

router = APIRouter(prefix="/scientific-discovery", tags=["Scientific Discovery Engine & AI Scientists (Phase 97)"])

ql_service = QuestionLiteratureEngineService()
hyp_service = HypothesisExperimentDesignService()
lab_service = DigitalLabReproducibilityService()
agent_service = AiScientistNetworkService()
sim_service = SimulationCausalMathEngineService()
rep_service = ReplicationMetaAnalysisService()
copilot_service = DiscoveryCopilotGovernanceService()


# ---------------------------------------------------------
# 1. QUESTION DECOMPOSITION & LITERATURE DISCOVERY
# ---------------------------------------------------------

@router.post("/questions/decompose", summary="Define and Decompose Research Question")
def decompose_question(
    title: str = Body(..., embed=True),
    domain: str = Body("Physics", embed=True),
    desired_outcome: str = Body("High sensitivity quantum sensor design", embed=True),
    constraints: Optional[List[str]] = Body(None, embed=True),
):
    return ql_service.define_and_decompose_question(title, domain, desired_outcome, constraints)


@router.post("/literature/ingest", summary="Ingest Literature Paper & Extract Claims")
def ingest_paper(
    paper_title: str = Body(..., embed=True),
    authors: List[str] = Body(["Dr. A. Smith"], embed=True),
    publication_year: int = Body(2026, embed=True),
    abstract: str = Body("Summary of empirical findings...", embed=True),
):
    return ql_service.ingest_literature_paper(paper_title, authors, publication_year, abstract)


@router.get("/literature/contradictions-gaps", summary="Detect Scientific Contradictions & Research Gaps")
def detect_contradictions(domain: str = Query("Physics")):
    return ql_service.detect_literature_contradictions_and_gaps(domain)


# ---------------------------------------------------------
# 2. AI HYPOTHESIS GENERATION & EXPERIMENT DESIGN
# ---------------------------------------------------------

@router.post("/hypotheses/generate-ai", summary="Generate Explicitly Labeled AI Hypothesis")
def generate_ai_hypothesis(
    question_id: str = Body(..., embed=True),
    hypothesis_title: str = Body(..., embed=True),
    statement: str = Body(..., embed=True),
):
    return hyp_service.generate_ai_hypothesis(question_id, hypothesis_title, statement)


@router.post("/experiments/design", summary="Design Candidate Experiment with Information-Gain Optimization")
def design_experiment(
    hypothesis_id: str = Body(..., embed=True),
    experiment_title: str = Body("Pulse Shaping Cryogenic Trial", embed=True),
    constraints: Dict[str, Any] = Body({"budget": "$50,000", "safety": "Standard Cryo Limits"}, embed=True),
):
    return hyp_service.design_experiment(hypothesis_id, experiment_title, constraints)


@router.post("/experiments/{experiment_id}/authorize", summary="Human Scientist Experiment Authorization")
def authorize_experiment(experiment_id: str, human_authorizer_id: str = Body("usr-dr-vance-01", embed=True)):
    return hyp_service.authorize_experiment_execution(experiment_id, human_authorizer_id)


# ---------------------------------------------------------
# 3. COMPUTATIONAL LAB & REPRODUCIBILITY
# ---------------------------------------------------------

@router.post("/digital-lab/session/create", summary="Create Computational Virtual Lab Session")
def create_lab_session(
    experiment_id: str = Body(..., embed=True),
    lab_name: str = Body("Quantum Simulation Lab #4", embed=True),
):
    return lab_service.create_computational_lab_session(experiment_id, lab_name)


@router.get("/digital-lab/{session_id}/verify-reproducibility", summary="Verify Session Reproducibility Package")
def verify_reproducibility(session_id: str):
    return lab_service.verify_reproducibility_package(session_id)


# ---------------------------------------------------------
# 4. AI SCIENTIST NETWORK & ORCHESTRATION
# ---------------------------------------------------------

@router.post("/ai-scientists/team/configure", summary="Configure Specialized AI Scientist Agent Team")
def configure_team(
    team_name: str = Body("Quantum Discovery Orchestrator", embed=True),
    human_supervisor_id: str = Body("usr-lead-pi-01", embed=True),
):
    return agent_service.configure_ai_scientist_team(team_name, human_supervisor_id)


@router.post("/ai-scientists/{team_id}/peer-review", summary="Run Independent AI Scientist Peer Review Critique")
def run_peer_review(team_id: str, research_artifact_id: str = Body("art-hyp-01", embed=True)):
    return agent_service.run_ai_peer_review_critique(team_id, research_artifact_id)


# ---------------------------------------------------------
# 5. SIMULATION, CAUSAL & MATHEMATICAL DISCOVERY
# ---------------------------------------------------------

@router.post("/simulation/run", summary="Run Multi-Model Scientific Simulation & Causal Discovery")
def run_simulation(
    title: str = Body("Thermal Gradient Stress Test", embed=True),
    domain_type: str = Body("Physics", embed=True),
    multi_models: List[str] = Body(["CryoSim-v4", "ThermalMesh-v2"], embed=True),
    parameters: Dict[str, Any] = Body({"gradient_k": 0.05}, embed=True),
):
    return sim_service.run_scientific_simulation(title, domain_type, multi_models, parameters)


@router.post("/mathematical/conjecture/explore", summary="Explore Mathematical Conjecture & Formal Proof")
def explore_conjecture(
    conjecture_title: str = Body("Boundary Operator Eigenvalue Distribution", embed=True),
    formal_statement: str = Body("forall n > 0, spectral gap lambda_1 >= c / n^2", embed=True),
):
    return sim_service.explore_mathematical_conjecture(conjecture_title, formal_statement)


# ---------------------------------------------------------
# 6. REPLICATION NETWORK & META-ANALYSIS
# ---------------------------------------------------------

@router.post("/replication/register", summary="Register Replication Attempt Outcome")
def register_replication(
    original_paper_id: str = Body(..., embed=True),
    replicating_team: str = Body("Independent Lab Gamma", embed=True),
    replication_status: str = Body("Replicated", embed=True),
    sample_size: int = Body(1500, embed=True),
    effect_size_observed: float = Body(0.84, embed=True),
):
    return rep_service.register_replication_attempt(
        original_paper_id, replicating_team, replication_status, sample_size, effect_size_observed
    )


@router.post("/meta-analysis/synthesis", summary="Run Multi-Study Meta-Analysis Synthesis")
def run_meta_analysis(
    topic_title: str = Body("Quantum Sensor Signal Efficiency", embed=True),
    included_study_ids: List[str] = Body(["lit-01", "lit-02", "lit-03"], embed=True),
):
    return rep_service.run_meta_analysis_synthesis(topic_title, included_study_ids)


# ---------------------------------------------------------
# 7. DISCOVERY COPILOT & SAFETY GOVERNANCE
# ---------------------------------------------------------

@router.post("/copilot/evidence-query", summary="Query Natural-Language Scientific Evidence Copilot")
def query_copilot(natural_language_query: str = Body("What evidence supports pulse shaping for quantum sensors?", embed=True)):
    return copilot_service.query_discovery_copilot_evidence(natural_language_query)


@router.post("/safety/dual-use-eval", summary="Evaluate Dual-Use Risk & Autonomous Limits")
def eval_dual_use(
    research_topic: str = Body("Cryogenic Micro-Sensor Optimization", embed=True),
    experiment_spec: Dict[str, Any] = Body({"sample": "Silicon Wafer"}, embed=True),
):
    return copilot_service.evaluate_dual_use_and_safety_limits(research_topic, experiment_spec)


@router.post("/registry/register-discovery", summary="Register Validated Discovery in Global Registry")
def register_discovery(
    discovery_title: str = Body("Sub-Kelvin Noise Suppression via Pulse Shaping", embed=True),
    confidence_level: str = Body("Replicated", embed=True),
    provenance: Dict[str, Any] = Body({"paper_ids": ["lit-01"], "rep_ids": ["rep-01"]}, embed=True),
    credit_attribution: Dict[str, Any] = Body({"PI": "Dr. Vance", "AI": "Hypothesis Agent v97"}, embed=True),
):
    return copilot_service.register_validated_discovery(discovery_title, confidence_level, provenance, credit_attribution)
