"""Unit and Integration Tests for Phase 34: Unified Workflow Orchestration, Event Bus & Automation."""

import pytest
import asyncio
from datetime import datetime
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS,
    validate_agent_permissions,
)
from agents.core.errors import AgentPermissionDeniedError
from app.events.base import DomainEvent
from app.events.registry import global_event_registry, EventRegistry, EventDefinition
from app.events.bus import InMemoryEventBus
from app.events.retry import RetryPolicy
from app.events.replay import EventReplayEngine, SENSITIVE_REPLAY_BLOCKS
from app.orchestration.state_machine import WorkflowStateMachine, WORKFLOW_TRANSITIONS, STEP_TRANSITIONS
from app.orchestration.workflow_registry import global_workflow_registry
from app.orchestration.idempotency import IdempotencyEngine
from app.models.orchestration import (
    EventDeliveryStatus,
    EventSensitivity,
    HumanTaskStatus,
    ReplayMode,
    TaskPriority,
    TaskType,
    WorkflowStatus,
    WorkflowStepStatus,
    DLQStatus,
)


# =============================================================================
# 1. Domain Event & Registry Tests
# =============================================================================

def test_domain_event_creation_and_serialization():
    """Verify DomainEvent initializes unique IDs, correlation IDs, and serializes cleanly."""
    evt = DomainEvent(
        event_type="lead.qualified",
        tenant_id="tenant_123",
        aggregate_type="lead",
        aggregate_id="lead_999",
        producer="qualification_service",
        payload={"score": 85.0, "fit_status": "QUALIFIED"},
    )

    assert evt.event_id.startswith("evt_")
    assert evt.correlation_id.startswith("corr_")
    assert evt.event_version == "v1"
    assert evt.payload["score"] == 85.0

    serialized = evt.to_dict()
    assert serialized["event_id"] == evt.event_id
    assert serialized["event_type"] == "lead.qualified"
    assert serialized["tenant_id"] == "tenant_123"


def test_event_registry_lookup_and_validation():
    """Verify central event registry catalogs core events and validates schemas."""
    defn = global_event_registry.get("lead.qualified")
    assert defn is not None
    assert defn.aggregate_type == "lead"
    assert defn.producer == "qualification_service"

    valid_payload = {
        "qualification_id": "qual_1",
        "lead_id": "lead_123",
        "fit_status": "QUALIFIED",
        "score": 92.5,
        "recommended_services": ["service_1"],
    }
    assert global_event_registry.validate_payload("lead.qualified", valid_payload) is True

    invalid_payload = {"fit_status": "QUALIFIED"}  # missing required fields
    assert global_event_registry.validate_payload("lead.qualified", invalid_payload) is False


# =============================================================================
# 2. Event Bus & Subscription Tests
# =============================================================================

@pytest.mark.asyncio
async def test_in_memory_event_bus_publish_and_subscribe():
    """Verify InMemoryEventBus routes published events to registered handlers."""
    bus = InMemoryEventBus()
    received_events = []

    async def sample_handler(evt: DomainEvent):
        received_events.append(evt)

    await bus.subscribe("business.discovered", sample_handler)

    test_evt = DomainEvent(
        event_type="business.discovered",
        tenant_id="tenant_123",
        aggregate_type="business",
        aggregate_id="biz_1",
        producer="discovery_service",
        payload={"company_name": "Nordic Solutions"},
    )

    published = await bus.publish(test_evt)
    assert published is True
    assert len(received_events) == 1
    assert received_events[0].payload["company_name"] == "Nordic Solutions"


# =============================================================================
# 3. Retry Policy & Backoff Tests
# =============================================================================

def test_retry_policy_exponential_backoff_and_jitter():
    """Verify RetryPolicy computes bounded delays and enforces max attempts."""
    policy = RetryPolicy(
        max_attempts=3,
        initial_backoff_seconds=1.0,
        backoff_multiplier=2.0,
        max_backoff_seconds=10.0,
        jitter=False,
    )

    assert policy.should_retry(1) is True
    assert policy.should_retry(2) is True
    assert policy.should_retry(3) is False  # Max reached

    assert policy.compute_backoff_seconds(1) == 1.0
    assert policy.compute_backoff_seconds(2) == 2.0
    assert policy.compute_backoff_seconds(3) == 4.0
    assert policy.compute_backoff_seconds(4) == 8.0
    assert policy.compute_backoff_seconds(5) == 10.0  # Capped at max_backoff


# =============================================================================
# 4. Idempotency & Hashing Tests
# =============================================================================

def test_idempotency_key_generation():
    """Verify deterministic idempotency key computation."""
    key1 = IdempotencyEngine.generate_key("wf_1", "step_research", attempt_group=1)
    key2 = IdempotencyEngine.generate_key("wf_1", "step_research", attempt_group=1)
    key3 = IdempotencyEngine.generate_key("wf_1", "step_research", attempt_group=2)

    assert key1 == key2
    assert key1 != key3
    assert len(key1) == 64  # SHA-256 length


def test_action_hash_verification():
    """Verify approval hash verification prevents payload tampering."""
    approved_text = "Proposal for Nordic Tech: Total $50,000"
    valid_hash = IdempotencyEngine.generate_key("proposal", approved_text)

    # Valid check
    assert IdempotencyEngine.verify_action_hash(approved_text, valid_hash) is False  # different salt
    # Exact text verification
    import hashlib
    correct_hash = hashlib.sha256(approved_text.strip().encode("utf-8")).hexdigest()
    assert IdempotencyEngine.verify_action_hash(approved_text, correct_hash) is True
    assert IdempotencyEngine.verify_action_hash(approved_text + " EXTRA", correct_hash) is False


# =============================================================================
# 5. Workflow State Machine Tests
# =============================================================================

def test_workflow_state_machine_valid_transitions():
    """Verify workflow state machine allows valid progression and blocks illegal skips."""
    sm = WorkflowStateMachine()

    # Valid transitions
    assert sm.can_transition_workflow(WorkflowStatus.CREATED, WorkflowStatus.RUNNING) is True
    assert sm.can_transition_workflow(WorkflowStatus.RUNNING, WorkflowStatus.WAITING) is True
    assert sm.can_transition_workflow(WorkflowStatus.WAITING, WorkflowStatus.RUNNING) is True
    assert sm.can_transition_workflow(WorkflowStatus.RUNNING, WorkflowStatus.COMPLETED) is True

    # Invalid transitions
    assert sm.can_transition_workflow(WorkflowStatus.COMPLETED, WorkflowStatus.RUNNING) is False
    assert sm.can_transition_workflow(WorkflowStatus.CANCELLED, WorkflowStatus.RUNNING) is False
    assert sm.can_transition_workflow(WorkflowStatus.CREATED, WorkflowStatus.COMPLETED) is False


def test_workflow_step_state_machine_transitions():
    """Verify step state machine transitions."""
    sm = WorkflowStateMachine()

    assert sm.can_transition_step(WorkflowStepStatus.PENDING, WorkflowStepStatus.READY) is True
    assert sm.can_transition_step(WorkflowStepStatus.READY, WorkflowStepStatus.RUNNING) is True
    assert sm.can_transition_step(WorkflowStepStatus.RUNNING, WorkflowStepStatus.SUCCEEDED) is True
    assert sm.can_transition_step(WorkflowStepStatus.RUNNING, WorkflowStepStatus.FAILED) is True

    # Terminal state cannot transition
    assert sm.can_transition_step(WorkflowStepStatus.SUCCEEDED, WorkflowStepStatus.RUNNING) is False


# =============================================================================
# 6. Workflow Registry & Built-in Templates Tests
# =============================================================================

def test_workflow_registry_templates():
    """Verify built-in workflow templates are registered with step sequences and transitions."""
    lead_wf = global_workflow_registry.get("lead_acquisition_workflow")
    assert lead_wf is not None
    assert lead_wf.category == "CLIENT_ACQUISITION"
    assert len(lead_wf.steps) == 9

    # Check human approval step
    human_step = lead_wf.get_step("human_approval")
    assert human_step is not None
    assert human_step.step_type == TaskType.HUMAN_TASK

    # Check transitions
    next_steps = lead_wf.get_next_steps("discovery")
    assert next_steps == ["research"]


# =============================================================================
# 7. Replay Safety Safeguard Tests
# =============================================================================

def test_replay_safety_blocks_sensitive_side_effects():
    """Verify that sensitive actions are hard-blocked during event replay."""
    assert "outreach.sent" in SENSITIVE_REPLAY_BLOCKS
    assert "contract.signed" in SENSITIVE_REPLAY_BLOCKS
    assert "change.approved" in SENSITIVE_REPLAY_BLOCKS


# =============================================================================
# 8. Agent Permissions Guard Tests
# =============================================================================

def test_workflow_permissions_guard():
    """Verify that Phase 34 permissions are allowed and prohibited actions are strictly blocked."""
    allowed_perms = {
        AgentPermission.READ_WORKFLOWS.value,
        AgentPermission.READ_EVENTS.value,
        AgentPermission.READ_AUTOMATION.value,
        AgentPermission.CREATE_WORKFLOW_DRAFT.value,
        AgentPermission.CREATE_AUTOMATION_DRAFT.value,
        AgentPermission.EXECUTE_AGENT_TASK.value,
    }
    validated = validate_agent_permissions(allowed_perms)
    assert len(validated) == 6

    # Verify prohibited permissions raise error
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"BYPASS_WORKFLOW_APPROVAL"})

    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"MODIFY_EVENT_HISTORY"})

    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"TRIGGER_UNSAFE_REPLAY"})

    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"EXECUTE_UNAUTHORIZED_AUTOMATION"})

    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"FORCE_COMPLETE_WORKFLOW_STEP"})
