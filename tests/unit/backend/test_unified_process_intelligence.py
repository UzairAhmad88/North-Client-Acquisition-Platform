"""
Unit Tests for Phase 49: Unified Process Intelligence, Process Mining, Optimization & Operations.
"""

import pytest
from datetime import datetime, timezone
import uuid

try:
    from backend.app.process_intelligence.base import (
        ActorType,
        AutomationSuitability,
        DeploymentStrategy,
        OptimizationStatus,
        ProcessDomain,
        ProcessHealthStatus,
        ProcessLifecycle,
        SimulationScenario,
        ViolationType,
    )
    from backend.app.process_intelligence.service import ProcessIntelligencePlatformService
except ImportError:
    from app.process_intelligence.base import (
        ActorType,
        AutomationSuitability,
        DeploymentStrategy,
        OptimizationStatus,
        ProcessDomain,
        ProcessHealthStatus,
        ProcessLifecycle,
        SimulationScenario,
        ViolationType,
    )
    from app.process_intelligence.service import ProcessIntelligencePlatformService
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission, AgentPermissionDeniedError, validate_agent_permissions
from agents.process_intelligence.discovery import ProcessIntelligenceAgent
from agents.process_intelligence.optimization import ProcessOptimizationAgent
from agents.process_intelligence.automation import AutomationCandidateAgent


@pytest.fixture
def service():
    """Initializes a fresh ProcessIntelligencePlatformService instance."""
    return ProcessIntelligencePlatformService()


def test_process_registration_and_retrieval(service):
    """Test registering and retrieving canonical business process definitions."""
    proc = service.register_process(
        name="Enterprise Sales Pipeline",
        domain=ProcessDomain.SALES,
        owner_id="sales_lead_user",
        expected_outcome="Convert qualified lead to signed contract",
        policy_requirements=["POL-01", "POL-02"],
        governance_controls=["CTRL-SALES-APPROVAL"],
        tenant_id="tenant_alpha",
    )

    assert proc.id is not None
    assert proc.name == "Enterprise Sales Pipeline"
    assert proc.domain == ProcessDomain.SALES
    assert proc.status == ProcessLifecycle.ACTIVE
    assert "CTRL-SALES-APPROVAL" in proc.governance_controls

    retrieved = service.get_process(proc.id, tenant_id="tenant_alpha")
    assert retrieved is not None
    assert retrieved.name == proc.name

    # Cross-tenant isolation
    assert service.get_process(proc.id, tenant_id="tenant_beta") is None


def test_event_log_ingestion_and_case_lifecycle(service):
    """Test ingesting process events, linking them to a case, and computing cycle times."""
    proc = service.register_process("Client Onboarding", domain=ProcessDomain.CLIENT_ONBOARDING)
    case = service.event_store.create_or_get_case(
        process_id=proc.id,
        entity_type="client",
        entity_id="cli_9942",
        tenant_id="tenant_alpha",
    )

    assert case.id is not None
    assert case.status == "ACTIVE"

    # Ingest Sequential Events
    evt1 = service.event_store.ingest_event(
        process_id=proc.id,
        activity="NEW_CLIENT_INVITE",
        case_id=case.id,
        actor="onboarding_rep_1",
        actor_type=ActorType.USER,
        duration_ms=120000,  # 2 min
        tenant_id="tenant_alpha",
        anonymize_actor=True,
    )
    assert evt1.actor.startswith("actor_")  # anonymized

    evt2 = service.event_store.ingest_event(
        process_id=proc.id,
        activity="KYC_VERIFICATION",
        case_id=case.id,
        actor="system",
        actor_type=ActorType.SYSTEM,
        duration_ms=300000,  # 5 min
        tenant_id="tenant_alpha",
    )

    evt3 = service.event_store.ingest_event(
        process_id=proc.id,
        activity="CONTRACT_SIGNING",
        case_id=case.id,
        actor="client_user",
        actor_type=ActorType.CLIENT,
        duration_ms=180000,  # 3 min
        tenant_id="tenant_alpha",
    )

    completed_case = service.event_store.complete_case(case.id, outcome="WON", tenant_id="tenant_alpha")
    assert completed_case is not None
    assert completed_case.status == "COMPLETED"
    assert completed_case.outcome == "WON"
    assert completed_case.processing_time_seconds == (120000 + 300000 + 180000) / 1000.0


def test_process_discovery_and_variant_mining(service):
    """Test discovering process execution variants and directly-follows transitions."""
    proc = service.register_process("Deal Flow", domain=ProcessDomain.SALES)

    # Simulate 3 cases following Variant A: Lead -> Outreach -> Won
    for i in range(3):
        case = service.event_store.create_or_get_case(proc.id, "lead", f"lead_a_{i}")
        service.event_store.ingest_event(proc.id, "LEAD_IN", case_id=case.id, duration_ms=60000)
        service.event_store.ingest_event(proc.id, "OUTREACH", case_id=case.id, duration_ms=120000)
        service.event_store.ingest_event(proc.id, "WON", case_id=case.id, duration_ms=60000)
        service.event_store.complete_case(case.id, outcome="WON")

    # Simulate 1 case following Variant B: Lead -> Outreach -> FollowUp -> Won
    case_b = service.event_store.create_or_get_case(proc.id, "lead", "lead_b_1")
    service.event_store.ingest_event(proc.id, "LEAD_IN", case_id=case_b.id, duration_ms=60000)
    service.event_store.ingest_event(proc.id, "OUTREACH", case_id=case_b.id, duration_ms=120000)
    service.event_store.ingest_event(proc.id, "FOLLOW_UP", case_id=case_b.id, duration_ms=90000)
    service.event_store.ingest_event(proc.id, "WON", case_id=case_b.id, duration_ms=60000)
    service.event_store.complete_case(case_b.id, outcome="WON")

    variants = service.discovery_engine.discover_variants(proc.id)
    assert len(variants) == 2
    assert variants[0].frequency == 3
    assert variants[0].percentage == 75.0
    assert variants[1].frequency == 1
    assert variants[1].percentage == 25.0

    process_map = service.discovery_engine.build_process_map(proc.id)
    assert len(process_map.nodes) >= 4
    assert len(process_map.edges) >= 3


def test_conformance_checking_bypassed_approval_and_skipped_step(service):
    """Test detecting conformance violations (skipped approval, skipped mandatory step)."""
    proc = service.register_process("Proposal Flow", domain=ProcessDomain.PROPOSAL)

    # Register Rules
    service.conformance_checker.register_rule(
        rule_id="RULE-1",
        process_id=proc.id,
        rule_code="RULE-MANDATORY-DISCOVERY",
        rule_type="MANDATORY_STEP",
        source_activity="DISCOVERY_CALL",
    )
    service.conformance_checker.register_rule(
        rule_id="RULE-2",
        process_id=proc.id,
        rule_code="RULE-APPR-BEFORE-SEND",
        rule_type="REQUIRED_APPROVAL",
        source_activity="HUMAN_APPROVAL",
        target_activity="SEND_PROPOSAL",
    )

    # Case 1: Skips Discovery, Bypasses Approval (Proposal -> Send)
    bad_case = service.event_store.create_or_get_case(proc.id, "proposal", "prop_101")
    service.event_store.ingest_event(proc.id, "DRAFT_PROPOSAL", case_id=bad_case.id)
    service.event_store.ingest_event(proc.id, "SEND_PROPOSAL", case_id=bad_case.id)
    service.event_store.complete_case(bad_case.id)

    violations = service.conformance_checker.check_case_conformance(proc.id, bad_case.id)
    assert len(violations) == 2
    types = {v.violation_type for v in violations}
    assert ViolationType.SKIPPED_STEP in types
    assert ViolationType.MISSING_APPROVAL in types


def test_bottleneck_and_cycle_time_detection(service):
    """Test detecting activity queue wait times and flow efficiency."""
    proc = service.register_process("Estimations", domain=ProcessDomain.ESTIMATION)
    case = service.event_store.create_or_get_case(proc.id, "estimate", "est_55")

    # Ingest event with large wait gap
    service.event_store.ingest_event(proc.id, "REQUIREMENTS_REVIEW", case_id=case.id, duration_ms=1000)
    service.event_store.ingest_event(proc.id, "TECHNICAL_ESTIMATION", case_id=case.id, duration_ms=1000)
    service.event_store.complete_case(case.id)

    # Bottleneck detection with lower threshold
    bottlenecks = service.bottleneck_detector.detect_bottlenecks(proc.id, wait_threshold_seconds=0.0)
    assert len(bottlenecks) >= 1

    cycle_stats = service.cycle_time_analyzer.analyze_cycle_times(proc.id)
    assert cycle_stats["total_cases"] == 1
    assert "flow_efficiency_percentage" in cycle_stats


def test_rework_and_handoff_analytics(service):
    """Test detecting rework loops (repeated design activities) and cross-role handoff friction."""
    proc = service.register_process("Design & Dev", domain=ProcessDomain.PROJECT_DELIVERY)
    case = service.event_store.create_or_get_case(proc.id, "project", "proj_42")

    # Design -> Dev -> Design (Rework)
    service.event_store.ingest_event(proc.id, "UI_DESIGN", case_id=case.id, attributes={"role": "DESIGNER"}, duration_ms=5000)
    service.event_store.ingest_event(proc.id, "DEVELOPMENT", case_id=case.id, attributes={"role": "ENGINEER"}, duration_ms=8000)
    service.event_store.ingest_event(proc.id, "UI_DESIGN", case_id=case.id, attributes={"role": "DESIGNER"}, duration_ms=4000)
    service.event_store.complete_case(case.id)

    rework = service.rework_analyzer.detect_rework(proc.id)
    assert len(rework) == 1
    assert rework[0].activity_name == "UI_DESIGN"
    assert rework[0].repetition_count == 2
    assert rework[0].wasted_duration_seconds == 4.0

    handoffs = service.handoff_analyzer.analyze_handoffs(proc.id)
    assert len(handoffs) >= 2


def test_automation_candidate_8_factor_evaluation(service):
    """Test computing the 8-factor Automation Suitability Score and classification."""
    proc = service.register_process("Support", domain=ProcessDomain.SUPPORT)

    # High frequency, deterministic task -> LOW_RISK_AUTOMATION
    c1 = service.automation_evaluator.evaluate_task(
        process_id=proc.id,
        task_name="Auto-Categorize Ticket",
        frequency_per_month=80,
        average_duration_minutes=5.0,
        error_rate=0.04,
        determinism_score=0.9,
        risk_score=0.1,
        reversibility="HIGH",
    )
    assert c1.suitability_score >= 0.70
    assert c1.classification == AutomationSuitability.LOW_RISK_AUTOMATION
    assert c1.expected_savings_hours_month == round((80 * 5.0) / 60.0, 1)

    # High risk task -> NOT_SUITABLE / HIGH_RISK_AUTOMATION
    c2 = service.automation_evaluator.evaluate_task(
        process_id=proc.id,
        task_name="Sign Commercial Contract",
        frequency_per_month=10,
        average_duration_minutes=30.0,
        error_rate=0.01,
        risk_score=0.95,
        reversibility="IRREVERSIBLE",
    )
    assert c2.classification == AutomationSuitability.NOT_SUITABLE


def test_isolated_what_if_simulation_zero_mutation(service):
    """Test running Monte Carlo what-if simulation with zero production state mutation."""
    proc = service.register_process("Logistics", domain=ProcessDomain.OPERATIONS if hasattr(ProcessDomain, 'OPERATIONS') else ProcessDomain.SALES)

    sim_res = service.simulation_engine.run_simulation(
        process_id=proc.id,
        scenario_type=SimulationScenario.OPTIMIZED,
        baseline_cycle_time_seconds=20000.0,
        automation_efficiency_gain=0.30,
        iterations=500,
    )

    assert sim_res.simulation_code.startswith("SIM-OPTI")
    assert sim_res.iterations == 500
    assert sim_res.predicted_cycle_time_seconds < 20000.0
    assert sim_res.assumptions["isolation_verified"] is True
    assert sim_res.assumptions["production_mutation"] is False


def test_multi_objective_optimization_proposal(service):
    """Test generating multi-objective optimization proposals with trade-off radar."""
    proc = service.register_process("Billing", domain=ProcessDomain.BILLING)

    prop = service.optimization_manager.create_proposal(
        process_id=proc.id,
        title="Async Invoice Reconciliation",
        problem_statement="Manual payment matching creates 4 hour latency.",
        evidence_summary="Simulations show 35% cycle time gain.",
        proposed_changes={"engine": "automated_matching"},
        cycle_time_improvement_pct=35.0,
        cost_savings_pct=20.0,
        quality_score=0.95,
        risk_level="LOW",
        compliance_score=1.0,
        rollback_plan="Revert rule to manual matching.",
    )

    assert prop.proposal_code.startswith("PROP-")
    assert prop.status == OptimizationStatus.DRAFT
    assert prop.tradeoff_scorecard["governance_aligned"] is True


def test_controlled_canary_deployment_and_rollback(service):
    """Test initiating canary deployment, health check degradation, and clean rollback."""
    proc = service.register_process("Contracts", domain=ProcessDomain.CONTRACT)

    dep = service.deployment_governor.initiate_deployment(
        process_id=proc.id,
        target_version=2,
        strategy=DeploymentStrategy.CANARY,
        rollout_percentage=15,
        approved_by="governance_board",
    )
    assert dep["status"] == "ACTIVE"
    assert dep["strategy"] == "CANARY"

    # Normal canary telemetry
    dep = service.deployment_governor.record_canary_telemetry(
        deployment_code=dep["deployment_code"],
        cases_routed=50,
        error_rate=0.01,
        cycle_time_seconds=300.0,
    )
    assert dep["health_status"] == ProcessHealthStatus.HEALTHY.value

    # Degraded error spike
    dep = service.deployment_governor.record_canary_telemetry(
        deployment_code=dep["deployment_code"],
        cases_routed=70,
        error_rate=0.18,  # > 15% error trips CRITICAL
        cycle_time_seconds=450.0,
    )
    assert dep["health_status"] == ProcessHealthStatus.CRITICAL.value

    # Rollback execution preserves history
    rolled_back = service.deployment_governor.rollback_deployment(
        deployment_code=dep["deployment_code"],
        reason="Elevated error rate in canary cohort",
        operator_id="sre_oncall",
    )
    assert rolled_back["status"] == "ROLLED_BACK"
    assert rolled_back["rollback_metadata"]["new_immutable_state_version"] == 3


def test_agent_permissions_and_prohibitions():
    """Test that Phase 49 permissions are valid and prohibited autonomous actions are blocked."""
    allowed_perms = {
        AgentPermission.READ_PROCESS_INTELLIGENCE.value,
        AgentPermission.ANALYZE_PROCESSES.value,
        AgentPermission.RUN_PROCESS_SIMULATION.value,
    }
    assert validate_agent_permissions(allowed_perms) == allowed_perms

    # Autonomous workflow modification must be strictly rejected
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"AUTONOMOUS_WORKFLOW_MUTATION"})

    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"AUTONOMOUS_PROCESS_DEPLOYMENT"})


@pytest.mark.asyncio
async def test_process_intelligence_agents_execution(service):
    """Test running ProcessIntelligenceAgent, ProcessOptimizationAgent, and AutomationCandidateAgent."""
    proc = service.register_process("Sales Demo Flow", domain=ProcessDomain.SALES)

    # 1. ProcessIntelligenceAgent
    disc_agent = ProcessIntelligenceAgent(service)
    ctx = AgentContext(
        workflow_id="wf_101",
        task_id="task_101",
        agent_run_id="run_101",
        metadata={"process_id": proc.id, "tenant_id": "default_tenant"},
    )
    res_disc = await disc_agent.execute(ctx)
    assert res_disc["status"] == "SUCCESS"
    assert res_disc["autonomous_actions_allowed"] is False

    # 2. AutomationCandidateAgent
    auto_agent = AutomationCandidateAgent(service)
    res_auto = await auto_agent.execute(ctx)
    assert res_auto["status"] == "SUCCESS"
    assert res_auto["autonomous_implementation_blocked"] is True

    # 3. ProcessOptimizationAgent
    opt_agent = ProcessOptimizationAgent(service)
    res_opt = await opt_agent.execute(ctx)
    assert res_opt["status"] == "SUCCESS"
