"""
Universal Intelligence OS Router (Phase 98)
API Endpoints for capability benchmarking, layered memory, world models, hierarchical action plans, multi-agent ensembles, drift monitoring, sandboxed AGI safety, kill-switches, and personal AI symbiosis.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Query, Body, HTTPException

from app.services.universal_intelligence import (
    IntelligenceCapabilityMemoryService,
    WorldModelMultimodalPerceptionService,
    HierarchicalActionPlanningService,
    MultiAgentEnsembleCognitionService,
    EvaluationAlignmentDriftService,
    SandboxedAgiSafetyKillswitchService,
    HumanSymbiosisPersonalAiService,
)

router = APIRouter(prefix="/universal-intelligence", tags=["Universal Intelligence & AGI Research (Phase 98)"])

cap_mem_service = IntelligenceCapabilityMemoryService()
wm_service = WorldModelMultimodalPerceptionService()
plan_service = HierarchicalActionPlanningService()
ensemble_service = MultiAgentEnsembleCognitionService()
drift_service = EvaluationAlignmentDriftService()
killswitch_service = SandboxedAgiSafetyKillswitchService()
symbiosis_service = HumanSymbiosisPersonalAiService()


# ---------------------------------------------------------
# 1. CAPABILITY GRAPH & LAYERED MEMORY
# ---------------------------------------------------------

@router.post("/capability/benchmark", summary="Benchmark Multi-Capability System Intelligence")
def benchmark_intelligence(
    system_name: str = Body("Uzaii-Universal-Engine-v98", embed=True),
    test_tasks: List[str] = Body(["Reasoning Benchmark #1", "Causal Transfer Test #2"], embed=True),
):
    return cap_mem_service.benchmark_system_intelligence(system_name, test_tasks)


@router.post("/memory/store", summary="Store Layered Memory Node")
def store_memory(
    memory_layer: str = Body("Semantic", embed=True),
    content_summary: str = Body("Established relationship between quantum noise and cryogenic cooling gradient.", embed=True),
    user_id: Optional[str] = Body("usr-researcher-01", embed=True),
    organization_id: Optional[str] = Body("org-research-lab", embed=True),
    scope: str = Body("Private", embed=True),
):
    return cap_mem_service.store_layered_memory(memory_layer, content_summary, user_id, organization_id, scope)


@router.post("/memory/{memory_id}/correct", summary="Correct Layered Memory Node")
def correct_memory(
    memory_id: str,
    corrected_content: str = Body("Updated relationship reflecting 300K ambient thermal noise threshold.", embed=True),
    corrector_id: str = Body("usr-researcher-01", embed=True),
):
    return cap_mem_service.correct_layered_memory(memory_id, corrected_content, corrector_id)


@router.delete("/memory/{memory_id}/delete", summary="Delete Layered Memory Node under User Control")
def delete_memory(memory_id: str, user_id: str = Query("usr-researcher-01")):
    return cap_mem_service.delete_layered_memory(memory_id, user_id)


# ---------------------------------------------------------
# 2. WORLD MODEL & MULTIMODAL PERCEPTION
# ---------------------------------------------------------

@router.post("/world-model/construct", summary="Construct Structured World Model Representation")
def construct_world_model(
    model_name: str = Body("Global Infrastructure World Model", embed=True),
    entities: List[Dict[str, Any]] = Body([{"entity": "Power Grid", "type": "Infrastructure"}], embed=True),
    relationships: List[Dict[str, Any]] = Body([{"from": "Power Grid", "to": "Water Pump", "type": "Powers"}], embed=True),
    causal_hypotheses: List[Dict[str, Any]] = Body([{"hypothesis": "Grid outage reduces water pressure"}], embed=True),
):
    return wm_service.construct_world_model_representation(model_name, entities, relationships, causal_hypotheses)


@router.post("/world-model/counterfactual-query", summary="Query World Model for Counterfactual Reasoning")
def query_counterfactual_wm(
    wm_id: str = Body(..., embed=True),
    changed_assumption: str = Body("Assume ambient thermal heat increases by +5C", embed=True),
):
    return wm_service.execute_counterfactual_world_reasoning(wm_id, changed_assumption)


# ---------------------------------------------------------
# 3. HIERARCHICAL ACTION PLANNING & AUTONOMY TIERS
# ---------------------------------------------------------

@router.post("/action-planning/create", summary="Create Hierarchical Action Plan with Autonomy Level Constraints")
def create_action_plan(
    goal: str = Body("Optimize Regional Energy Reserve", embed=True),
    strategy_summary: str = Body("Staged microgrid dispatch under supervised control", embed=True),
    tasks: List[Dict[str, Any]] = Body([{"task_id": "t1", "description": "Assess reserve"}], embed=True),
    autonomy_level: str = Body("Level 0 — Advisory", embed=True),
):
    return plan_service.create_hierarchical_action_plan(goal, strategy_summary, tasks, autonomy_level)


@router.post("/action-planning/{plan_id}/interrupt", summary="Interrupt Autonomous Action Plan Execution")
def interrupt_plan(plan_id: str, interrupted_by: str = Body("usr-operator-01", embed=True), reason: str = Body("Manual audit required", embed=True)):
    return plan_service.interrupt_action_plan(plan_id, interrupted_by, reason)


@router.post("/action-planning/{plan_id}/rollback", summary="Rollback Reversible Action Plan")
def rollback_plan(plan_id: str, human_operator_id: str = Body("usr-operator-01", embed=True)):
    return plan_service.rollback_action_plan(plan_id, human_operator_id)


# ---------------------------------------------------------
# 4. MULTI-AGENT ENSEMBLE & REFLECTION
# ---------------------------------------------------------

@router.post("/multi-agent/register", summary="Register Specialized Agent Profile with Least-Privilege Tools")
def register_agent(
    agent_name: str = Body("Critic Agent Beta", embed=True),
    role: str = Body("Critic", embed=True),
    capabilities: List[str] = Body(["Adversarial Review", "Constraint Verification"], embed=True),
    tool_permissions: Dict[str, Any] = Body({"read": True, "write": False, "execute": False}, embed=True),
):
    return ensemble_service.register_specialized_agent(agent_name, role, capabilities, tool_permissions)


@router.post("/multi-agent/reflection-cycle", summary="Run Ensemble Reflection & Self-Evaluation Cycle")
def run_reflection(task_id: str = Body("task-optimization-01", embed=True), action_outcomes: Dict[str, Any] = Body({"status": "Success"}, embed=True)):
    return ensemble_service.run_ensemble_reflection_cycle(task_id, action_outcomes)


# ---------------------------------------------------------
# 5. EVALUATION, ALIGNMENT & DRIFT MONITORING
# ---------------------------------------------------------

@router.post("/evaluation/benchmark-suite/run", summary="Run Comprehensive Model Evaluation Suite")
def run_evaluation(model_version_id: str = Body("mdl-frontier-v98.1", embed=True)):
    return drift_service.run_comprehensive_model_evaluation(model_version_id)


@router.post("/evaluation/drift-monitoring", summary="Monitor Deployment Drift & Check Rollback Triggers")
def monitor_drift(
    model_id: str = Body("mdl-frontier-v98.1", embed=True),
    current_metrics: Dict[str, Any] = Body({"data_drift_score": 0.05, "behavior_drift_score": 0.03}, embed=True),
):
    return drift_service.monitor_deployment_drift(model_id, current_metrics)


# ---------------------------------------------------------
# 6. SANDBOXED AGI SAFETY & INDEPENDENT KILL-SWITCH
# ---------------------------------------------------------

@router.post("/safety/sandbox/initialize", summary="Initialize Sandboxed AGI Research Environment")
def init_sandbox(
    experiment_id: str = Body("exp-agi-test-01", embed=True),
    compute_limit_vcpus: int = Body(64, embed=True),
    memory_limit_gb: int = Body(256, embed=True),
    network_isolation: str = Body("Strict_Air_Gap", embed=True),
):
    return killswitch_service.initialize_sandboxed_research_environment(experiment_id, compute_limit_vcpus, memory_limit_gb, network_isolation)


@router.post("/safety/killswitch/execute", summary="Execute Independent Out-of-Band Human Kill-Switch")
def execute_killswitch(
    authorized_human_operator_id: str = Body("usr-commander-01", embed=True),
    reason: str = Body("Emergency out-of-band safety intervention", embed=True),
):
    return killswitch_service.execute_independent_human_killswitch(authorized_human_operator_id, reason)


# ---------------------------------------------------------
# 7. HUMAN–AI SYMBIOSIS & PERSONAL AI
# ---------------------------------------------------------

@router.post("/personal-ai/configure", summary="Configure Personal AI Symbiosis Profile")
def configure_personal_ai(
    user_id: str = Body("usr-researcher-01", embed=True),
    preferred_explanation_depth: str = Body("Detailed", embed=True),
    cognitive_load_adaptation: bool = Body(True, embed=True),
):
    return symbiosis_service.configure_personal_ai_symbiosis(user_id, preferred_explanation_depth, cognitive_load_adaptation)


@router.post("/personal-ai/counterfactual-query", summary="Interactive Counterfactual Reasoning Query")
def query_counterfactual_pai(
    user_id: str = Body("usr-researcher-01", embed=True),
    query_text: str = Body("How will strategy efficiency change if energy cost doubles?", embed=True),
    changed_assumption: str = Body("Energy cost = $0.20/kWh", embed=True),
):
    return symbiosis_service.query_counterfactual_reasoning_engine(user_id, query_text, changed_assumption)


@router.get("/personal-ai/{user_id}/export-manifest", summary="Export Personal AI Data Portability Manifest")
def export_manifest(user_id: str):
    return symbiosis_service.export_personal_ai_data_manifest(user_id)
