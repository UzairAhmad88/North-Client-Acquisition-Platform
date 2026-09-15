import asyncio
import uuid
from typing import Optional
from sqlalchemy.orm import Session

import agents.qualification  # Ensures QualificationAgent is registered
from agents.core.registry import global_registry
from app.models.lead import Lead
from app.repositories.qualification import QualificationRepository
from app.services.agents import AgentRunRepository, AgentRuntimeService


async def execute_qualification_task(
    db: Session,
    lead_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = None,
) -> None:
    """Asynchronous task worker function running Qualification Agent within Phase 14 runtime."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        return

    # 1. Trigger Qualification Agent Run via AgentRuntimeService
    runtime_service = AgentRuntimeService()
    run = runtime_service.trigger_agent_run(
        db,
        agent_name="qualification_agent",
        business_id=lead.business_id,
        lead_id=lead.id,
        workflow_id=f"wf-qual-{lead.id.hex[:8]}",
        input_data={"lead_id": str(lead.id), "business_id": str(lead.business_id)},
    )

    try:
        # Build least-privilege agent context
        context = runtime_service.build_context(
            db,
            workflow_id=run.workflow_id,
            task_id=run.task_id,
            agent_run_id=run.agent_run_id,
            business_id=lead.business_id,
            lead_id=lead.id,
        )

        # Run Qualification Agent
        agent = global_registry.get("qualification_agent")
        result = await agent.run(context)

        # 2. Persist LeadQualification record
        qual_res = result.result
        qual_data = {
            "lead_id": lead.id,
            "business_id": lead.business_id,
            "user_id": user_id,
            "agent_run_id": run.id,
            "decision": qual_res.get("decision", "INSUFFICIENT_DATA"),
            "confidence": qual_res.get("confidence", "MEDIUM"),
            "summary": qual_res.get("summary", ""),
            "factors": qual_res.get("factors", []),
            "reasons": qual_res.get("reasons", []),
            "evidence": qual_res.get("evidence", []),
            "risks": qual_res.get("risks", []),
            "missing_information": qual_res.get("missing_information", []),
            "limitations": qual_res.get("limitations", []),
            "outreach_readiness": qual_res.get("outreach_readiness", "NOT_READY"),
            "recommended_internal_action": qual_res.get("recommended_internal_action"),
            "qualification_version": "1.0",
        }

        qual = QualificationRepository.create_qualification(db, qual_data)

        # Update lead qualification_status field
        lead.qualification_status = qual.decision
        db.commit()

        # Update Agent Run completion status
        AgentRunRepository.update_run_status(
            db,
            run.id,
            status=result.status,
            output_summary=result.result,
            confidence=result.confidence,
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_COMPLETED", f"Qualification Agent finished with decision {qual.decision}."
        )

    except Exception as e:
        AgentRunRepository.update_run_status(
            db, run.id, status="FAILED", error_message=str(e)
        )
        AgentRunRepository.record_event(
            db, run.id, "AGENT_FAILED", f"Qualification Agent failed: {str(e)}"
        )
        raise e


def run_qualification_task_sync(
    db: Session,
    lead_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = None,
) -> None:
    """Synchronous wrapper for thread/process execution."""
    asyncio.run(execute_qualification_task(db, lead_id, user_id=user_id))
