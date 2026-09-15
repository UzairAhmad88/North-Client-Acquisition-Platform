"""
REST API Router for Phase 49:
Unified Workflow Intelligence, Process Mining, Business Process Optimization & Operations.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

try:
    from app.api.deps import get_db, get_security_context
    from app.process_intelligence.base import (
        ActorType,
        DeploymentStrategy,
        ProcessDomain,
        SimulationScenario,
    )
    from app.process_intelligence.service import ProcessIntelligencePlatformService
    from app.schemas.process_intelligence import (
        ConformanceRuleCreateRequest,
        DeploymentInitiateRequest,
        DeploymentRollbackRequest,
        OptimizationProposalCreateRequest,
        ProcessCaseCreateRequest,
        ProcessCopilotRequest,
        ProcessCreateRequest,
        ProcessEventIngestRequest,
        ProcessEventResponse,
        ProcessResponse,
        SimulationRunRequest,
    )
except ImportError:
    from backend.app.api.deps import get_db, get_security_context
    from backend.app.process_intelligence.base import (
        ActorType,
        DeploymentStrategy,
        ProcessDomain,
        SimulationScenario,
    )
    from backend.app.process_intelligence.service import ProcessIntelligencePlatformService
    from backend.app.schemas.process_intelligence import (
        ConformanceRuleCreateRequest,
        DeploymentInitiateRequest,
        DeploymentRollbackRequest,
        OptimizationProposalCreateRequest,
        ProcessCaseCreateRequest,
        ProcessCopilotRequest,
        ProcessCreateRequest,
        ProcessEventIngestRequest,
        ProcessEventResponse,
        ProcessResponse,
        SimulationRunRequest,
    )

router = APIRouter(prefix="/process-intelligence", tags=["process-intelligence"])
_service = ProcessIntelligencePlatformService()


@router.get("/overview")
async def get_overview(
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Provides high-level organizational process intelligence health and metrics."""
    return _service.get_overview(tenant_id=tenant_id)


@router.get("/processes")
async def list_processes(
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Lists registered process definitions for a tenant."""
    processes = _service.list_processes(tenant_id=tenant_id)
    return [p.dict() for p in processes]


@router.post("/processes", status_code=status.HTTP_201_CREATED)
async def create_process(
    request: ProcessCreateRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Registers a new business process definition."""
    domain = ProcessDomain(request.domain) if request.domain in ProcessDomain.__members__ else ProcessDomain.SALES
    proc = _service.register_process(
        name=request.name,
        domain=domain,
        owner_id=request.owner_id,
        scope=request.scope,
        expected_outcome=request.expected_outcome,
        policy_requirements=request.policy_requirements,
        governance_controls=request.governance_controls,
        tenant_id=tenant_id,
    )
    return proc.dict()


@router.get("/processes/{process_id}")
async def get_process(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Gets details for a single process definition."""
    proc = _service.get_process(process_id, tenant_id=tenant_id)
    if not proc:
        raise HTTPException(status_code=404, detail=f"Process '{process_id}' not found.")
    return proc.dict()


@router.post("/event-log", status_code=status.HTTP_201_CREATED)
async def ingest_event(
    request: ProcessEventIngestRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Ingests a process telemetry event into the immutable event log."""
    actor_type = ActorType(request.actor_type) if request.actor_type in ActorType.__members__ else ActorType.SYSTEM
    evt = _service.event_store.ingest_event(
        process_id=request.process_id,
        activity=request.activity,
        tenant_id=tenant_id,
        case_id=request.case_id,
        actor=request.actor,
        actor_type=actor_type,
        resource=request.resource,
        duration_ms=request.duration_ms,
        attributes=request.attributes,
        anonymize_actor=request.anonymize_actor,
    )
    return evt.dict()


@router.get("/event-log")
async def list_event_logs(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Returns event log entries for a process definition."""
    events = _service.event_store.get_events_for_process(process_id, tenant_id=tenant_id)
    return [e.dict() for e in events]


@router.get("/variants")
async def get_variants(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Discovers distinct execution variant paths and sequence frequencies."""
    variants = _service.discovery_engine.discover_variants(process_id, tenant_id=tenant_id)
    return [v.dict() for v in variants]


@router.get("/maps/{process_id}")
async def get_process_map(
    process_id: str,
    map_type: str = "OBSERVED",
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Builds a directly-follows graph of activity nodes and transition latencies."""
    pmap = _service.discovery_engine.build_process_map(process_id, map_type=map_type, tenant_id=tenant_id)
    return pmap.dict()


@router.get("/conformance")
async def get_conformance_violations(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Audits process traces against conformance rules."""
    violations = _service.conformance_checker.check_process_conformance(process_id, tenant_id=tenant_id)
    return [v.dict() for v in violations]


@router.post("/conformance/rules", status_code=status.HTTP_201_CREATED)
async def register_conformance_rule(
    request: ConformanceRuleCreateRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Registers a conformance rule for a process."""
    import uuid
    rule_id = str(uuid.uuid4())
    rule = _service.conformance_checker.register_rule(
        rule_id=rule_id,
        process_id=request.process_id,
        rule_code=request.rule_code,
        rule_type=request.rule_type,
        source_activity=request.source_activity,
        target_activity=request.target_activity,
        parameters=request.parameters,
        severity=request.severity,
        tenant_id=tenant_id,
    )
    return rule


@router.get("/bottlenecks")
async def get_bottlenecks(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Detects queue latencies and bottleneck activities with root-cause evidence."""
    bottlenecks = _service.bottleneck_detector.detect_bottlenecks(process_id, tenant_id=tenant_id)
    return [b.dict() for b in bottlenecks]


@router.get("/rework")
async def get_rework_records(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Detects repetitive loops and wasted rework duration."""
    rework = _service.rework_analyzer.detect_rework(process_id, tenant_id=tenant_id)
    return [r.dict() for r in rework]


@router.get("/handoffs")
async def get_handoff_records(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Evaluates cross-role transition delays and friction scores."""
    handoffs = _service.handoff_analyzer.analyze_handoffs(process_id, tenant_id=tenant_id)
    return [h.dict() for h in handoffs]


@router.get("/automation")
async def get_automation_candidates(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Returns repetitive tasks evaluated for safe workflow automation."""
    candidates = _service.automation_evaluator.scan_for_candidates(process_id, tenant_id=tenant_id)
    return [c.dict() for c in candidates]


@router.post("/optimization", status_code=status.HTTP_201_CREATED)
async def create_optimization_proposal(
    request: OptimizationProposalCreateRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Drafts a multi-objective workflow optimization proposal."""
    prop = _service.optimization_manager.create_proposal(
        process_id=request.process_id,
        title=request.title,
        problem_statement=request.problem_statement,
        evidence_summary=request.evidence_summary,
        proposed_changes=request.proposed_changes,
        cycle_time_improvement_pct=request.cycle_time_improvement_pct,
        cost_savings_pct=request.cost_savings_pct,
        quality_score=request.quality_score,
        risk_level=request.risk_level,
        compliance_score=request.compliance_score,
        expected_cost=request.expected_cost,
        rollback_plan=request.rollback_plan,
        tenant_id=tenant_id,
    )
    return prop.dict()


@router.get("/optimization")
async def list_optimization_proposals(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> List[Dict[str, Any]]:
    """Lists optimization proposals for a process."""
    proposals = _service.optimization_manager.get_proposals_for_process(process_id, tenant_id=tenant_id)
    return [p.dict() for p in proposals]


@router.post("/simulations")
async def run_simulation(
    request: SimulationRunRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Runs an isolated what-if simulation with zero production state mutation."""
    scenario = SimulationScenario(request.scenario_type) if request.scenario_type in SimulationScenario.__members__ else SimulationScenario.OPTIMIZED
    res = _service.simulation_engine.run_simulation(
        process_id=request.process_id,
        scenario_type=scenario,
        baseline_cycle_time_seconds=request.baseline_cycle_time_seconds,
        baseline_cost_per_case=request.baseline_cost_per_case,
        baseline_failure_rate=request.baseline_failure_rate,
        baseline_rework_rate=request.baseline_rework_rate,
        arrival_rate_multiplier=request.arrival_rate_multiplier,
        automation_efficiency_gain=request.automation_efficiency_gain,
        resource_capacity_multiplier=request.resource_capacity_multiplier,
        iterations=request.iterations,
        tenant_id=tenant_id,
    )
    return res.dict()


@router.post("/deployments", status_code=status.HTTP_201_CREATED)
async def initiate_deployment(
    request: DeploymentInitiateRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Launches a controlled canary rollout for an approved workflow version."""
    strategy = DeploymentStrategy(request.strategy) if request.strategy in DeploymentStrategy.__members__ else DeploymentStrategy.CANARY
    dep = _service.deployment_governor.initiate_deployment(
        process_id=request.process_id,
        target_version=request.target_version,
        strategy=strategy,
        rollout_percentage=request.rollout_percentage,
        proposal_id=request.proposal_id,
        approved_by=request.approved_by,
        tenant_id=tenant_id,
    )
    return dep


@router.post("/deployments/rollback")
async def rollback_deployment(
    request: DeploymentRollbackRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Executes a rollback preserving history without overwriting previous versions."""
    res = _service.deployment_governor.rollback_deployment(
        deployment_code=request.deployment_code,
        reason=request.reason,
        operator_id=request.operator_id,
        tenant_id=tenant_id,
    )
    if not res:
        raise HTTPException(status_code=404, detail=f"Deployment '{request.deployment_code}' not found.")
    return res


@router.get("/health")
async def get_process_health(
    process_id: str,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Gets aggregate health state and SLO compliance for a process."""
    health = _service.get_process_health(process_id, tenant_id=tenant_id)
    return health.dict()


@router.post("/copilot/query")
async def query_copilot(
    request: ProcessCopilotRequest,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Process Intelligence Copilot query answering process questions with evidence grounding."""
    health = _service.get_process_health(request.process_id, tenant_id=tenant_id)
    bottlenecks = _service.bottleneck_detector.detect_bottlenecks(request.process_id, tenant_id=tenant_id)
    violations = _service.conformance_checker.check_process_conformance(request.process_id, tenant_id=tenant_id)

    response_text = (
        f"Process '{request.process_id}' is currently {health.health_status.value} with a flow efficiency "
        f"of {health.factors_summary.get('flow_efficiency_pct', 0.0)}%. "
        f"There are {len(bottlenecks)} active bottlenecks and {len(violations)} conformance violations detected."
    )

    return {
        "query": request.query,
        "response": response_text,
        "health_status": health.health_status.value,
        "bottlenecks_count": len(bottlenecks),
        "violations_count": len(violations),
        "guardrail_status": "ENFORCED (Autonomous production mutations blocked)",
    }
