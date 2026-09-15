"""Agent Runtime Service Layer."""

import uuid
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.core.errors import AgentNotFoundError, AgentPermissionDeniedError
from agents.core.registry import global_registry
from agents.core.state import validate_state_transition
from app.core.exceptions import NotFoundError, ValidationError
from app.models.agent import AgentRun
from app.models.business import Business
from app.models.lead import Lead
from app.services.agents.repository import AgentRunRepository


class AgentRuntimeService:
    """High-level service for agent runtime execution, observability, and cancellation."""

    def build_context(
        self,
        db: Session,
        workflow_id: str,
        task_id: str,
        agent_run_id: str,
        user_id: Optional[uuid.UUID] = None,
        lead_id: Optional[uuid.UUID] = None,
        business_id: Optional[uuid.UUID] = None,
    ) -> AgentContext:
        """Gather context with least-privilege scoping."""
        business_profile: Dict[str, Any] = {}
        lead_profile: Dict[str, Any] = {}

        if lead_id:
            lead = db.scalar(select(Lead).where(Lead.id == lead_id))
            if lead:
                lead_profile = {
                    "id": str(lead.id),
                    "title": lead.title,
                    "status": lead.status,
                    "priority": lead.priority,
                }
                if not business_id:
                    business_id = lead.business_id

        if business_id:
            biz = db.scalar(select(Business).where(Business.id == business_id))
            if biz:
                business_profile = {
                    "id": str(biz.id),
                    "name": biz.name,
                    "category": biz.category,
                    "city": biz.city,
                    "status": biz.status,
                }

        return AgentContext(
            workflow_id=workflow_id,
            task_id=task_id,
            agent_run_id=agent_run_id,
            user_id=user_id,
            lead_id=lead_id,
            business_id=business_id,
            business_profile=business_profile,
            lead_profile=lead_profile,
        )

    def trigger_agent_run(
        self,
        db: Session,
        agent_name: str,
        user_id: Optional[uuid.UUID] = None,
        lead_id: Optional[uuid.UUID] = None,
        business_id: Optional[uuid.UUID] = None,
        workflow_id: Optional[str] = None,
        input_data: Optional[Dict[str, Any]] = None,
    ) -> AgentRun:
        """Create and trigger agent execution run."""
        # 1. Verify Agent in Registry
        agent = global_registry.get(agent_name)

        w_id = workflow_id or f"wf-{uuid.uuid4().hex[:8]}"
        t_id = f"task-{uuid.uuid4().hex[:8]}"

        # 2. Create AgentRun record
        run = AgentRunRepository.create_run(
            db,
            workflow_id=w_id,
            task_id=t_id,
            agent_name=agent.name,
            agent_version=agent.version,
            user_id=user_id,
            lead_id=lead_id,
            business_id=business_id,
            input_summary=input_data or {},
        )

        AgentRunRepository.record_event(
            db, run.id, "AGENT_STARTED", f"Agent '{agent.name}' (v{agent.version}) run initiated."
        )

        # Transition status to RUNNING
        AgentRunRepository.update_run_status(db, run.id, "RUNNING")

        return run

    def list_runs(
        self,
        db: Session,
        lead_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
        limit: int = 50,
        page: int = 1,
    ) -> Tuple[List[AgentRun], int]:
        """List agent runs."""
        return AgentRunRepository.list_runs(db, lead_id=lead_id, status=status, limit=limit, page=page)

    def get_run(self, db: Session, run_id: uuid.UUID) -> AgentRun:
        """Get agent run by ID."""
        run = AgentRunRepository.get_run(db, run_id)
        if not run:
            raise NotFoundError(f"Agent run with ID {run_id} not found.")
        return run

    def cancel_run(self, db: Session, run_id: uuid.UUID) -> AgentRun:
        """Cancel active agent run."""
        run = self.get_run(db, run_id)
        if run.status in ("COMPLETED", "FAILED", "CANCELLED"):
            return run

        validate_state_transition(run.status, "CANCELLED")
        updated = AgentRunRepository.update_run_status(
            db, run_id, "CANCELLED", error_message="Run cancelled by user request."
        )
        AgentRunRepository.record_event(
            db, run_id, "AGENT_CANCELLED", "Agent run was manually cancelled by user."
        )
        return updated
