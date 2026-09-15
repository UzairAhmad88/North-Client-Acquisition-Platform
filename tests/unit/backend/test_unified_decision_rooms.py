"""
Unit test suite for Phase 53:
Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
"""

import pytest
from backend.app.services.decision_rooms.service import DecisionRoomPlatformService
from backend.app.services.decision_rooms.base import (
    DecisionType,
    DecisionImportance,
    DecisionStatus,
    EvidenceType,
    StatementCategory,
    SpecialistRole,
    DisagreementCategory,
    ApprovalStatus,
)
from agents.decision import (
    DecisionContextAgent,
    EvidenceAgent,
    OptionGenerationAgent,
    AdversarialReviewAgent,
    DisagreementAgent,
    PostDecisionLearningAgent,
)
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS


@pytest.fixture
def service():
    return DecisionRoomPlatformService()


def test_room_lifecycle_and_recording(service):
    room = service.rooms.create_room(
        title="Migrate to High-Throughput Database",
        question="Should we migrate primary OLTP to a globally distributed database?",
        owner_id="tech_lead",
        decision_type=DecisionType.TECHNICAL,
        importance=DecisionImportance.HIGH,
    )
    assert room["id"].startswith("room_")
    assert room["status"] == "OPEN"

    # Transition
    updated = service.rooms.transition_status(
        room_id=room["id"],
        target_status=DecisionStatus.ANALYSIS,
        actor_id="tech_lead",
        notes="Started specialist analysis phase.",
    )
    assert updated["status"] == "ANALYSIS"
    assert updated["version"] == 2

    # Record decision
    decided = service.rooms.record_decision(
        room_id=room["id"],
        selected_option_id="opt_mig_postgres",
        decision_summary="Adopt PostgreSQL with read-replicas for next 18 months.",
        decided_by="tech_lead",
    )
    assert decided["status"] == "DECIDED"
    assert decided["selected_option_id"] == "opt_mig_postgres"


def test_context_and_evidence_fact_inference_separation(service):
    room = service.rooms.create_room(title="Test Context Room", question="Test?", owner_id="user1")
    r_id = room["id"]

    ctx = service.context_evidence.set_context(
        room_id=r_id,
        background="Evaluating cloud hosting costs.",
        constraints=["Max $5,000 monthly spend"],
    )
    assert ctx["background"] == "Evaluating cloud hosting costs."

    # Fact evidence
    ev1 = service.context_evidence.add_evidence(
        room_id=r_id,
        evidence_type=EvidenceType.DATABASE,
        source="AWS Billing Export",
        claim="Average monthly spend over last 6 months was $3,850.",
        statement_category=StatementCategory.FACT,
        confidence=1.0,
    )
    assert ev1["statement_category"] == "FACT"

    # Inference evidence
    ev2 = service.context_evidence.add_evidence(
        room_id=r_id,
        evidence_type=EvidenceType.FINANCIAL_DATA,
        source="Forecasting Model",
        claim="Traffic growth indicates monthly spend will likely reach $5,400 by Q4.",
        statement_category=StatementCategory.INFERENCE,
        confidence=0.82,
    )
    assert ev2["statement_category"] == "INFERENCE"

    # Classifier helper
    cat = service.context_evidence.classify_statement("We recommend migrating to reserved instances", "AI_ANALYSIS")
    assert cat == StatementCategory.RECOMMENDATION


def test_assumptions_unknowns_and_hypotheses(service):
    room = service.rooms.create_room(title="Test Assumptions Room", question="Test?", owner_id="user1")
    r_id = room["id"]

    asmp = service.assumptions_options.add_assumption(
        room_id=r_id,
        statement="Reserved instance pricing discounts remain at 35%.",
        confidence=0.9,
        impact_if_false="MEDIUM",
    )
    assert asmp["id"].startswith("asmp_")

    unkn = service.assumptions_options.add_unknown(
        room_id=r_id,
        question="Will client traffic increase during black friday by >300%?",
        impact="HIGH",
        resolution_path="Run load testing simulation.",
    )
    assert unkn["impact"] == "HIGH"
    assert len(service.assumptions_options.list_unknowns(r_id)) == 1


def test_option_generation_and_decision_matrix_scoring(service):
    room = service.rooms.create_room(title="Option Matrix Room", question="Test?", owner_id="user1")
    r_id = room["id"]

    opt_a = service.assumptions_options.create_option(
        room_id=r_id,
        name="Option A: In-House GPU Cluster",
        description="Purchase dedicated hardware.",
        benefits=["Zero per-token cloud costs", "Full data privacy"],
        costs=45000.0,
    )
    opt_b = service.assumptions_options.create_option(
        room_id=r_id,
        name="Option B: Serverless Cloud Endpoints",
        description="Pay per invocation.",
        benefits=["Instant elasticity", "Zero maintenance"],
        costs=15000.0,
    )

    c1 = service.assumptions_options.add_criterion(room_id=r_id, name="Upfront Capital Cost", weight=1.5, criterion_type="COST")
    c2 = service.assumptions_options.add_criterion(room_id=r_id, name="Operational Agility", weight=1.0, criterion_type="BENEFIT")

    service.assumptions_options.score_option(r_id, opt_a["id"], c1["id"], 40.0)
    service.assumptions_options.score_option(r_id, opt_a["id"], c2["id"], 60.0)

    service.assumptions_options.score_option(r_id, opt_b["id"], c1["id"], 90.0)
    service.assumptions_options.score_option(r_id, opt_b["id"], c2["id"], 95.0)

    options = service.assumptions_options.list_options(r_id)
    opt_b_updated = next(o for o in options if o["id"] == opt_b["id"])
    assert opt_b_updated["composite_score"] > 0

    tradeoff = service.assumptions_options.generate_tradeoff(r_id, opt_a["id"], opt_b["id"])
    assert "Option A" in tradeoff["tradeoff_summary"]


def test_specialists_adversarial_review_and_disagreements(service):
    room = service.rooms.create_room(title="Specialist Review Room", question="Test?", owner_id="user1")
    r_id = room["id"]

    anls = service.specialists.submit_specialist_analysis(
        room_id=r_id,
        specialist_role=SpecialistRole.SECURITY,
        summary="Zero egress policy strictly maintained.",
        confidence=0.96,
    )
    assert anls["specialist_role"] == "SECURITY"

    rev = service.specialists.submit_adversarial_review(
        room_id=r_id,
        critique_summary="Serverless cold starts could degrade 99th percentile latency by 850ms.",
        weak_assumptions=["Assumes average payload is <100KB."],
        hidden_costs=["High NAT gateway egress bandwidth fees."],
    )
    assert len(rev["weak_assumptions"]) == 1

    disag = service.specialists.register_disagreement(
        room_id=r_id,
        topic="Peak Traffic Volume",
        disagreement_category=DisagreementCategory.ASSUMPTION,
        party_a="Operations",
        view_a="Estimate 10k requests/sec",
        party_b="Finance",
        view_b="Budget sized for 2.5k requests/sec",
    )
    assert disag["disagreement_category"] == "ASSUMPTION"

    consensus = service.specialists.compute_consensus_metrics(r_id)
    assert consensus["total_disagreements"] == 1
    assert consensus["primary_disagreement"] == "Peak Traffic Volume"


def test_approvals_separation_of_duties_and_actions(service):
    room = service.rooms.create_room(title="Approval Gate Room", question="Test?", owner_id="user1")
    r_id = room["id"]

    steps = service.discussions_approvals.configure_approval_steps(
        room_id=r_id,
        steps=[
            {"step_name": "SECURITY_REVIEW", "required_role": "CISO"},
            {"step_name": "EXECUTIVE_APPROVAL", "required_role": "CEO"},
        ]
    )
    assert len(steps) == 2

    appr = service.discussions_approvals.record_approval_action(
        room_id=r_id,
        step_id=steps[0]["id"],
        approver_id="ciso_user",
        status=ApprovalStatus.APPROVED,
        notes="Security requirements verified.",
    )
    assert appr["status"] == "APPROVED"
    assert appr["approver_id"] == "ciso_user"

    action = service.discussions_approvals.create_action_item(
        room_id=r_id,
        title="Deploy Redis Cache Cluster",
        target_system="WORKFORCE_TASK",
    )
    assert action["execution_status"] == "PENDING_APPROVAL"

    authorized = service.discussions_approvals.authorize_action_execution(
        room_id=r_id,
        action_id=action["id"],
        authorizer_id="tech_director",
    )
    assert authorized["execution_status"] == "AUTHORIZED"


def test_outcomes_and_decision_quality_score(service):
    room = service.rooms.create_room(title="Outcome Learning Room", question="Test?", owner_id="user1")
    r_id = room["id"]

    outcome = service.outcomes_journal.record_outcome(
        room_id=r_id,
        metric_name="Monthly Infrastructure Cost",
        expected_value=4000.0,
        actual_value=4200.0,
    )
    assert outcome["variance_pct"] == 5.0

    post_rev = service.outcomes_journal.submit_post_review(
        room_id=r_id,
        reviewed_by="lead_architect",
        outcome_rating="SUCCESSFUL",
        evidence_quality=90.0,
        option_diversity=85.0,
        risk_coverage=90.0,
        lessons_learned=["Pre-warming cache keys prevented latency spikes during rollout."],
    )
    assert post_rev["decision_quality_score"] > 85.0
    assert post_rev["feed_to_organizational_memory"] is True


@pytest.mark.asyncio
async def test_decision_agents_initialization_and_execution(service):
    ctx_agent = DecisionContextAgent(service)
    ev_agent = EvidenceAgent(service)
    opt_agent = OptionGenerationAgent(service)
    adv_agent = AdversarialReviewAgent(service)
    disag_agent = DisagreementAgent(service)
    post_agent = PostDecisionLearningAgent(service)

    assert AgentPermission.READ_DECISION_ROOM in ctx_agent.permissions
    assert AgentPermission.GENERATE_DECISION_OPTIONS in opt_agent.permissions
    assert AgentPermission.RUN_ADVERSARIAL_REVIEW in adv_agent.permissions

    room = service.rooms.create_room(title="Agent Test Room", question="Test?", owner_id="agent_runner")
    r_id = room["id"]

    context = AgentContext(
        workflow_id="wf_123",
        task_id="tsk_123",
        agent_run_id="run_123",
        metadata={"room_id": r_id, "claim": "Market demand is high.", "source": "Survey Q3"},
    )
    ev_res = await ev_agent.execute(context)
    assert ev_res["status"] == "SUCCESS"


def test_collaboration_copilot_queries(service):
    # Test query on pre-seeded room
    rooms = service.rooms.list_rooms()
    r_id = rooms[0]["id"]

    res1 = service.ask_copilot(r_id, "Compare the candidate options.")
    assert res1["requires_human_decision"] is True
    assert "candidate options" in res1["answer"]

    res2 = service.ask_copilot(r_id, "What risks and weak assumptions exist?")
    assert res2["requires_human_decision"] is True
    assert "Adversarial review" in res2["answer"]


def test_prohibited_decision_permissions():
    # Verify autonomous decision making and approval are strictly prohibited
    assert "AUTONOMOUS_DECISION_MAKING" in PROHIBITED_PERMISSIONS
    assert "AUTONOMOUS_DECISION_APPROVAL" in PROHIBITED_PERMISSIONS
    assert "AUTONOMOUS_ACTION_EXECUTION" in PROHIBITED_PERMISSIONS
