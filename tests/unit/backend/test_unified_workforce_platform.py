"""
Unit tests for Phase 52: Unified Autonomous Knowledge Worker & Multi-Agent Workforce Platform.
Tests worker registry, capability enforcement, tool policy limits, task DAG decomposition,
multi-criteria assignment, supervision levels, human review queue, handoffs, consensus,
adversarial review, budget tracking, kill switches, and platform service facade.
"""

import pytest
import uuid
from datetime import datetime, timezone

try:
    from backend.app.services.workforce.base import (
        AIHandoff,
        AIReviewResult,
        AIWorker,
        AIWorkTask,
        CollaborationPattern,
        KillSwitchTarget,
        SensitiveCapability,
        SupervisionLevel,
        TaskPriority,
        TaskStatus,
        WorkerCapability,
        WorkerStatus,
    )
    from backend.app.services.workforce.service import WorkforcePlatformService
except ImportError:
    from app.services.workforce.base import (
        AIHandoff,
        AIReviewResult,
        AIWorker,
        AIWorkTask,
        CollaborationPattern,
        KillSwitchTarget,
        SensitiveCapability,
        SupervisionLevel,
        TaskPriority,
        TaskStatus,
        WorkerCapability,
        WorkerStatus,
    )
    from app.services.workforce.service import WorkforcePlatformService

from agents.workforce import (
    WorkforceManagerAgent,
    TaskPlannerAgent,
    SupervisionAgent,
    HandoffAgent,
    ConsensusReviewerAgent,
    WorkforcePerformanceAgent,
)
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission


@pytest.fixture
def workforce_service():
    return WorkforcePlatformService()


# ============================================================================
# 1. WORKER REGISTRY & LIFECYCLE TESTS
# ============================================================================

def test_worker_registry_and_templates(workforce_service):
    workers = workforce_service.list_workers()
    assert len(workers) >= 20

    research_worker = workforce_service.get_worker("WRK-RESEARCH-01")
    assert research_worker is not None
    assert research_worker.specialization == "RESEARCH"
    assert research_worker.status == WorkerStatus.ACTIVE

    # Register custom worker
    custom = workforce_service.register_worker(
        name="Autonomous Dental Lead Specialist",
        role="Domain Specialist",
        specialization="DENTAL_INTELLIGENCE",
        description="Specialized in dental enterprise practice audits",
        supervision_level=SupervisionLevel.DRAFT_GEN_2,
    )
    assert custom.worker_code.startswith("WRK-")
    assert custom.status == WorkerStatus.APPROVED


# ============================================================================
# 2. CAPABILITY & TOOL POLICY ENFORCEMENT TESTS
# ============================================================================

def test_capability_and_sensitive_blocking(workforce_service):
    worker = workforce_service.get_worker("WRK-RESEARCH-01")

    # Authorized capability
    auth_res = workforce_service.capability_manager.validate_capability_access(
        worker, WorkerCapability.READ.value
    )
    assert auth_res["is_authorized"] is True

    # Sensitive capability blocked by default
    sens_res = workforce_service.capability_manager.validate_capability_access(
        worker, SensitiveCapability.EXECUTE_PAYMENT.value
    )
    assert sens_res["is_authorized"] is False
    assert sens_res["requires_human_approval"] is True

    # Tool policy limits
    tool_ok = workforce_service.tool_policy_manager.authorize_tool_call(
        worker, "search_web", current_calls_count=5
    )
    assert tool_ok["is_allowed"] is True

    tool_exceeded = workforce_service.tool_policy_manager.authorize_tool_call(
        worker, "search_web", current_calls_count=15
    )
    assert tool_exceeded["is_allowed"] is False


# ============================================================================
# 3. DEPARTMENTS & SQUADS TESTS
# ============================================================================

def test_departments_and_teams(workforce_service):
    depts = workforce_service.list_departments()
    assert len(depts) >= 5

    teams = workforce_service.list_teams("DEPT-SALES")
    assert len(teams) >= 1
    assert "TEAM-DISCOVERY-01" in [t.team_code for t in teams]


# ============================================================================
# 4. TASK GRAPH & DAG DECOMPOSITION TESTS
# ============================================================================

def test_task_graph_decomposition_and_dag(workforce_service):
    tasks = workforce_service.plan_and_decompose_objective(
        objective="Scale qualified healthcare practice outreach in Texas",
        domain="GROWTH_EXPANSION",
    )
    assert len(tasks) == 3
    assert tasks[0].status in [TaskStatus.QUEUED, TaskStatus.ASSIGNED]
    assert tasks[0].worker_code is not None

    # Verify DAG validity (no cycles)
    valid, err = workforce_service.task_graph_engine.validate_task_dag(tasks)
    assert valid is True
    assert err is None


# ============================================================================
# 5. SUPERVISION & HUMAN REVIEW QUEUE TESTS
# ============================================================================

def test_supervision_levels_and_review_queue(workforce_service):
    low_risk_task = AIWorkTask(
        objective="Read public company website",
        supervision_level=SupervisionLevel.READ_ONLY_1,
        risk_level="LOW",
    )
    sup_ok = workforce_service.evaluate_supervision(low_risk_task, confidence=0.95, risk=0.1)
    assert sup_ok["can_execute_autonomously"] is True

    high_risk_task = AIWorkTask(
        objective="Deploy outreach messaging to 2,000 corporate leads",
        supervision_level=SupervisionLevel.REVIEW_REQUIRED_4,
        risk_level="HIGH",
    )
    sup_gate = workforce_service.evaluate_supervision(high_risk_task, confidence=0.70, risk=0.55)
    assert sup_gate["can_execute_autonomously"] is False
    assert "review_id" in sup_gate

    pending = workforce_service.list_pending_reviews()
    assert len(pending) >= 1

    # Resolve review
    resolved = workforce_service.resolve_human_review(
        review_id=sup_gate["review_id"],
        approved=True,
        reviewer_id="Chief Revenue Officer",
        rationale="Outreach copy matches enterprise compliance guidelines.",
    )
    assert resolved["status"] == "APPROVED"


# ============================================================================
# 6. STRUCTURED HANDOFFS & ARTIFACT TRANSFERS
# ============================================================================

def test_structured_handoff_engine(workforce_service):
    handoff = workforce_service.execute_handoff(
        from_worker_code="WRK-RESEARCH-01",
        to_worker_code="WRK-LEAD_QUALIFICATION-01",
        task_code="TSK-DEMO-01",
        context_summary="Researched 50 prospects with verified tech stack.",
        artifacts=[{"type": "RESEARCH_DATASET", "items_count": 50}],
        expected_next_action="Calculate opportunity score and recommend packages.",
    )
    assert isinstance(handoff, AIHandoff)
    assert handoff.handoff_code.startswith("HND-")
    assert handoff.status == "DELIVERED"


# ============================================================================
# 7. MULTI-WORKER CONSENSUS & ADVERSARIAL REVIEW
# ============================================================================

def test_consensus_and_adversarial_review(workforce_service):
    opinions = [
        {"worker_code": "WRK-RESEARCH-01", "recommendation": "EXPAND", "confidence": 0.95},
        {"worker_code": "WRK-SALES_INTELLIGENCE-01", "recommendation": "EXPAND", "confidence": 0.90},
        {"worker_code": "WRK-FINANCE-01", "recommendation": "EXPAND", "confidence": 0.92},
    ]
    consensus = workforce_service.evaluate_multi_worker_consensus("Target Sector Expansion", opinions)
    assert consensus.consensus_score >= 0.90
    assert consensus.has_conflicts is False

    # Adversarial critic check
    review = workforce_service.conduct_adversarial_review(
        task_code="TSK-DRAFT-01",
        author_code="WRK-OUTREACH_DRAFTING-01",
        critic_code="WRK-QA-01",
        draft_text="We offer high-value automation tools tailored to your practice workflow.",
    )
    assert isinstance(review, AIReviewResult)
    assert review.is_approved_by_critic is True


# ============================================================================
# 8. BUDGETS, ROI ECONOMICS & EVALUATION SCORECARDS
# ============================================================================

def test_budgets_and_workforce_economics(workforce_service):
    spend = workforce_service.budget_engine.track_task_spend(
        worker_code="WRK-RESEARCH-01",
        cost_usd=1.25,
        daily_limit_usd=15.0,
    )
    assert spend["total_daily_spend_usd"] == 1.25
    assert spend["is_budget_exceeded"] is False

    econ = workforce_service.get_workforce_economics()
    assert econ["roi_multiple"] > 0.0
    assert econ["human_hours_saved"] > 0.0

    scorecard = workforce_service.get_worker_scorecard("WRK-RESEARCH-01")
    assert scorecard["task_success_rate"] >= 90.0
    assert scorecard["health_grade"] in ["A+", "A", "B"]


# ============================================================================
# 9. EMERGENCY KILL SWITCHES
# ============================================================================

def test_emergency_kill_switches(workforce_service):
    ks = workforce_service.activate_kill_switch(
        target_type=KillSwitchTarget.WORKER,
        target_id="WRK-SUSPECT-01",
        reason="Security audit investigation active.",
        operator_id="secops_lead",
    )
    assert ks["status"] == "ACTIVE"

    blocked, reason = workforce_service.security_manager.is_blocked_by_kill_switch(worker_code="WRK-SUSPECT-01")
    assert blocked is True
    assert "suspended" in reason


# ============================================================================
# 10. WORKFORCE AGENTS & COPILOT
# ============================================================================

@pytest.mark.asyncio
async def test_workforce_agents_initialization():
    context = AgentContext(
        workflow_id="wf-wf-01",
        task_id="task-wf-01",
        agent_run_id="run-wf-01",
        metadata={"objective": "Test workforce execution"},
    )

    manager = WorkforceManagerAgent()
    assert "Workforce Manager" in manager.name

    planner = TaskPlannerAgent()
    assert "Task Planner" in planner.name

    supervision = SupervisionAgent()
    assert "Supervision" in supervision.name

    handoff = HandoffAgent()
    assert "Handoff" in handoff.name

    consensus = ConsensusReviewerAgent()
    assert "Consensus" in consensus.name

    perf = WorkforcePerformanceAgent()
    assert "Performance" in perf.name


def test_workforce_copilot(workforce_service):
    res = workforce_service.query_workforce_copilot("What is our current workforce ROI?")
    assert "ROI" in res["answer"] or "roi" in res["answer"]
    assert len(res["evidence"]) > 0
