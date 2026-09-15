"""Worker task executing Personalization Agent within Phase 14 Agent Core runtime."""

import asyncio
import uuid
from typing import Optional
from sqlalchemy.orm import Session

import agents.personalization  # Ensures PersonalizationAgent is registered
from agents.core.registry import global_registry
from app.models.lead import Lead
from app.services.agents import AgentRunRepository, AgentRuntimeService
from app.services.outreach import OutreachDraftService


async def execute_personalization_task(
    db: Session,
    lead_id: uuid.UUID,
    channel: str = "EMAIL",
    tone: str = "PROFESSIONAL",
    language: str = "en",
    personalization_depth: str = "STANDARD",
    objective: str = "INTRODUCE_SERVICE",
    user_id: Optional[uuid.UUID] = None,
) -> None:
    """Asynchronous worker function executing Personalization Agent and saving draft."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return

    runtime_service = AgentRuntimeService()
    run = runtime_service.trigger_agent_run(
        db,
        agent_name="personalization_agent",
        business_id=lead.business_id,
        lead_id=lead.id,
        workflow_id=f"wf-pers-{lead.id.hex[:8]}",
        input_data={"lead_id": str(lead.id), "channel": channel, "tone": tone},
    )

    try:
        draft = await OutreachDraftService.run_personalization(
            db=db,
            lead_id=lead.id,
            channel=channel,
            tone=tone,
            language=language,
            personalization_depth=personalization_depth,
            objective=objective,
            user_id=user_id,
        )

        AgentRunRepository.update_run_status(
            db,
            run.id,
            status="COMPLETED",
            output_summary={"draft_id": str(draft.id), "subject": draft.subject, "readiness": draft.outreach_readiness},
            confidence="HIGH",
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_COMPLETED", f"Personalization Agent generated draft v{draft.version} ({draft.approval_status})."
        )
    except Exception as e:
        AgentRunRepository.update_run_status(db, run.id, status="FAILED", error_message=str(e))
        AgentRunRepository.record_event(db, run.id, "AGENT_FAILED", f"Personalization Agent failed: {str(e)}")
        raise e


def run_personalization_task_sync(
    db: Session,
    lead_id: uuid.UUID,
    channel: str = "EMAIL",
    user_id: Optional[uuid.UUID] = None,
) -> None:
    asyncio.run(execute_personalization_task(db, lead_id, channel=channel, user_id=user_id))
