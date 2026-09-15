"""Deterministic Workflow and Step State Machine Transitions for Phase 34."""

from typing import Dict, List, Set
from app.models.orchestration import WorkflowStatus, WorkflowStepStatus


# Allowed transitions for top-level WorkflowRun
WORKFLOW_TRANSITIONS: Dict[WorkflowStatus, Set[WorkflowStatus]] = {
    WorkflowStatus.CREATED: {WorkflowStatus.RUNNING, WorkflowStatus.CANCELLED},
    WorkflowStatus.RUNNING: {
        WorkflowStatus.WAITING,
        WorkflowStatus.PAUSED,
        WorkflowStatus.BLOCKED,
        WorkflowStatus.FAILED,
        WorkflowStatus.COMPLETED,
        WorkflowStatus.CANCELLED,
    },
    WorkflowStatus.WAITING: {
        WorkflowStatus.RUNNING,
        WorkflowStatus.BLOCKED,
        WorkflowStatus.CANCELLED,
        WorkflowStatus.EXPIRED,
    },
    WorkflowStatus.PAUSED: {WorkflowStatus.RUNNING, WorkflowStatus.CANCELLED},
    WorkflowStatus.BLOCKED: {WorkflowStatus.RUNNING, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED},
    WorkflowStatus.FAILED: {WorkflowStatus.RUNNING, WorkflowStatus.CANCELLED},  # Retry re-enters RUNNING
    WorkflowStatus.COMPLETED: set(),  # Terminal state
    WorkflowStatus.CANCELLED: set(),  # Terminal state
    WorkflowStatus.EXPIRED: set(),    # Terminal state
}


# Allowed transitions for individual WorkflowRunStep
STEP_TRANSITIONS: Dict[WorkflowStepStatus, Set[WorkflowStepStatus]] = {
    WorkflowStepStatus.PENDING: {WorkflowStepStatus.READY, WorkflowStepStatus.SKIPPED, WorkflowStepStatus.CANCELLED},
    WorkflowStepStatus.READY: {WorkflowStepStatus.RUNNING, WorkflowStepStatus.BLOCKED, WorkflowStepStatus.CANCELLED},
    WorkflowStepStatus.RUNNING: {
        WorkflowStepStatus.WAITING,
        WorkflowStepStatus.SUCCEEDED,
        WorkflowStepStatus.FAILED,
        WorkflowStepStatus.BLOCKED,
        WorkflowStepStatus.CANCELLED,
    },
    WorkflowStepStatus.WAITING: {
        WorkflowStepStatus.RUNNING,
        WorkflowStepStatus.SUCCEEDED,
        WorkflowStepStatus.FAILED,
        WorkflowStepStatus.CANCELLED,
    },
    WorkflowStepStatus.SUCCEEDED: set(),  # Terminal step state
    WorkflowStepStatus.FAILED: {WorkflowStepStatus.RUNNING, WorkflowStepStatus.SKIPPED},  # Retry re-enters RUNNING
    WorkflowStepStatus.SKIPPED: set(),   # Terminal step state
    WorkflowStepStatus.CANCELLED: set(), # Terminal step state
    WorkflowStepStatus.BLOCKED: {WorkflowStepStatus.READY, WorkflowStepStatus.FAILED, WorkflowStepStatus.CANCELLED},
}


class WorkflowStateMachine:
    """Validates and enforces valid state transitions."""

    @staticmethod
    def can_transition_workflow(current_status: WorkflowStatus, next_status: WorkflowStatus) -> bool:
        """Check if workflow transition is valid."""
        allowed = WORKFLOW_TRANSITIONS.get(current_status, set())
        return next_status in allowed

    @staticmethod
    def can_transition_step(current_status: WorkflowStepStatus, next_status: WorkflowStepStatus) -> bool:
        """Check if step transition is valid."""
        allowed = STEP_TRANSITIONS.get(current_status, set())
        return next_status in allowed
