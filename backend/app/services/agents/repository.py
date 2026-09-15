"""Repository for database operations on Agent Runs, Events, and AI Usage."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, cast

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent import AIUsage, AgentEvent, AgentRun


class AgentRunRepository:
    """DB Repository for Agent Runs, Events, and AI Usage logging."""

    @staticmethod
    def create_run(
        db: Session,
        workflow_id: str,
        task_id: str,
        agent_name: str,
        agent_version: str = "1.0",
        user_id: Optional[uuid.UUID] = None,
        lead_id: Optional[uuid.UUID] = None,
        business_id: Optional[uuid.UUID] = None,
        input_summary: Optional[Dict[str, Any]] = None,
    ) -> AgentRun:
        now = datetime.now(timezone.utc)
        run_id = str(uuid.uuid4())
        run = AgentRun(
            id=uuid.uuid4(),
            workflow_id=workflow_id,
            task_id=task_id,
            agent_run_id=run_id,
            agent_name=agent_name,
            agent_version=agent_version,
            user_id=user_id,
            lead_id=lead_id,
            business_id=business_id,
            status="CREATED",
            input_summary=input_summary or {},
            output_summary={},
            confidence="MEDIUM",
            started_at=now,
            created_at=now,
            updated_at=now,
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def get_run(db: Session, run_id: uuid.UUID) -> Optional[AgentRun]:
        return db.scalar(select(AgentRun).where(AgentRun.id == run_id))

    @staticmethod
    def list_runs(
        db: Session,
        lead_id: Optional[uuid.UUID] = None,
        status: Optional[str] = None,
        limit: int = 50,
        page: int = 1,
    ) -> Tuple[List[AgentRun], int]:
        query = select(AgentRun)
        if lead_id:
            query = query.where(AgentRun.lead_id == lead_id)
        if status:
            query = query.where(AgentRun.status == status)

        total_query = select(AgentRun.id)
        if lead_id:
            total_query = total_query.where(AgentRun.lead_id == lead_id)
        if status:
            total_query = total_query.where(AgentRun.status == status)

        total_count = len(db.scalars(total_query).all())

        offset = (page - 1) * limit
        query = query.order_by(AgentRun.created_at.desc()).offset(offset).limit(limit)
        results = db.scalars(query).all()
        return list(results), total_count

    @staticmethod
    def update_run_status(
        db: Session,
        run_id: uuid.UUID,
        status: str,
        output_summary: Optional[Dict[str, Any]] = None,
        confidence: Optional[str] = None,
        error_message: Optional[str] = None,
        tool_calls_delta: int = 0,
        steps_delta: int = 0,
    ) -> AgentRun:
        run = AgentRunRepository.get_run(db, run_id)
        if not run:
            raise ValueError(f"AgentRun {run_id} not found.")

        now = datetime.now(timezone.utc)
        run.status = status
        run.updated_at = now

        if output_summary is not None:
            run.output_summary = output_summary
        if confidence is not None:
            run.confidence = confidence
        if error_message is not None:
            run.error_message = error_message

        run.tool_calls_count += tool_calls_delta
        run.steps_count += steps_delta

        if status in ("COMPLETED", "FAILED", "CANCELLED"):
            run.completed_at = now

        db.commit()
        db.refresh(run)
        return run

    @staticmethod
    def record_event(
        db: Session,
        agent_run_id: uuid.UUID,
        event_type: str,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> AgentEvent:
        event = AgentEvent(
            id=uuid.uuid4(),
            agent_run_id=agent_run_id,
            event_type=event_type,
            message=message,
            payload=payload or {},
            timestamp=datetime.now(timezone.utc),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def record_ai_usage(
        db: Session,
        provider: str,
        model: str,
        agent_name: str,
        agent_run_id: Optional[uuid.UUID] = None,
        user_id: Optional[uuid.UUID] = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        total_tokens: int = 0,
        estimated_cost: float = 0.0,
        latency_ms: int = 0,
        status: str = "SUCCESS",
    ) -> AIUsage:
        usage = AIUsage(
            id=uuid.uuid4(),
            provider=provider,
            model=model,
            agent_name=agent_name,
            agent_run_id=agent_run_id,
            user_id=user_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
            latency_ms=latency_ms,
            status=status,
            created_at=datetime.now(timezone.utc),
        )
        db.add(usage)
        db.commit()
        db.refresh(usage)
        return usage
