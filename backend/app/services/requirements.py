"""Requirements Service managing discovery workflows, agent runs, human confirmation, and Risk Engine integration."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.requirements.agent import requirements_agent
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.requirements import ClientRequirement, DiscoveryQuestion, DiscoverySession, RequirementScopeItem
from app.repositories.requirements import RequirementsRepository


class RequirementsService:
    """Service layer for discovery session lifecycle, requirements management, and human confirmation."""

    @staticmethod
    def create_discovery_session(
        db: Session, business_id: uuid.UUID, lead_id: Optional[uuid.UUID] = None, conversation_id: Optional[uuid.UUID] = None, user_id: Optional[uuid.UUID] = None, notes: Optional[str] = None
    ) -> DiscoverySession:
        session_data = {
            "business_id": business_id,
            "lead_id": lead_id,
            "conversation_id": conversation_id,
            "created_by_id": user_id,
            "status": "OPEN",
            "readiness_stage": "NOT_READY",
            "readiness_score": 0.0,
            "completeness_score": 0.0,
            "scope_complexity": "UNKNOWN",
            "notes": notes,
        }
        session_obj = RequirementsRepository.create_discovery_session(db, session_data)
        RequirementsRepository.log_event(db, session_obj.id, "DISCOVERY_STARTED", {"created_by_id": str(user_id) if user_id else None})
        return session_obj

    @staticmethod
    def get_discovery_session(db: Session, session_id: uuid.UUID) -> Optional[DiscoverySession]:
        return RequirementsRepository.get_discovery_session(db, session_id)

    @staticmethod
    def list_discovery_sessions(db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[DiscoverySession]:
        return RequirementsRepository.list_discovery_sessions(db, status=status, limit=limit, offset=offset)

    @staticmethod
    async def analyze_discovery_session(db: Session, session_id: uuid.UUID) -> DiscoverySession:
        session_obj = RequirementsRepository.get_discovery_session(db, session_id)
        if not session_obj:
            raise ValueError(f"DiscoverySession {session_id} not found")

        # Fetch latest message text from conversation if linked
        message_body = "Client requested business web application and booking system."
        message_id = None
        if session_obj.conversation_id:
            latest_msg = (
                db.query(Message)
                .filter(Message.conversation_id == session_obj.conversation_id, Message.direction == "INBOUND")
                .order_by(Message.sent_at.desc())
                .first()
            )
            if latest_msg:
                message_body = latest_msg.body
                message_id = str(latest_msg.id)

        # Build agent context
        context = AgentContext(
            workflow_id=f"wf-req-{str(session_id)[:8]}",
            task_id=f"task-req-{str(session_id)[:8]}",
            agent_run_id=str(uuid.uuid4()),
            business_profile={"id": str(session_obj.business_id)},
            metadata={"latest_message": {"body": message_body, "id": message_id}},
        )

        agent_result = await requirements_agent.run(context)
        res_data = agent_result.result

        # Save extracted requirements
        for req_dict in res_data.get("requirements", []):
            req_obj = RequirementsRepository.create_requirement(
                db,
                {
                    "discovery_session_id": session_obj.id,
                    "business_id": session_obj.business_id,
                    "lead_id": session_obj.lead_id,
                    "category": req_dict["category"],
                    "title": req_dict["title"],
                    "description": req_dict["description"],
                    "source_type": req_dict["source_type"],
                    "source_reference": req_dict.get("source_reference"),
                    "explicit": req_dict["explicit"],
                    "confidence": req_dict["confidence"],
                    "status": req_dict["status"],
                    "priority": req_dict["priority"],
                },
            )
            if req_dict.get("evidence_text"):
                RequirementsRepository.create_evidence(
                    db,
                    {
                        "requirement_id": req_obj.id,
                        "source_type": req_dict["source_type"],
                        "source_id": req_dict.get("source_reference"),
                        "evidence_text": req_dict["evidence_text"],
                        "confidence": req_dict["confidence"],
                    },
                )

        # Save questions
        for q_dict in res_data.get("questions", []):
            RequirementsRepository.create_question(
                db,
                {
                    "discovery_session_id": session_obj.id,
                    "question": q_dict["question"],
                    "category": q_dict.get("category", "SCOPE"),
                    "priority": q_dict.get("priority", "HIGH"),
                    "reason": q_dict.get("reason"),
                    "status": "PROPOSED",
                },
            )

        # Save scope items
        for s_dict in res_data.get("scope_items", []):
            RequirementsRepository.create_scope_item(
                db,
                {
                    "discovery_session_id": session_obj.id,
                    "description": s_dict["description"],
                    "scope_status": s_dict.get("scope_status", "UNKNOWN"),
                    "priority": s_dict.get("priority", "MEDIUM"),
                    "confirmed": s_dict.get("confirmed", False),
                },
            )

        # Update session readiness and status
        readiness = res_data.get("readiness", {})
        session_obj.readiness_stage = readiness.get("readiness_stage", "NOT_READY")
        session_obj.readiness_score = readiness.get("readiness_score", 0.0)
        session_obj.completeness_score = readiness.get("completeness_score", 0.0)
        session_obj.scope_complexity = readiness.get("scope_complexity", "UNKNOWN")
        session_obj.status = "IN_PROGRESS"
        session_obj.version += 1

        db.commit()
        db.refresh(session_obj)

        RequirementsRepository.log_event(
            db, session_obj.id, "REQUIREMENT_ANALYSIS_COMPLETED", {"requirements_count": len(res_data.get("requirements", []))}
        )

        return session_obj

    @staticmethod
    def confirm_requirement(db: Session, requirement_id: uuid.UUID, user_id: uuid.UUID) -> ClientRequirement:
        req = RequirementsRepository.get_requirement(db, requirement_id)
        if not req:
            raise ValueError(f"Requirement {requirement_id} not found")

        req.status = "CONFIRMED"
        req.confirmed_by_id = user_id
        req.confirmed_at = datetime.utcnow()
        req.version += 1

        db.commit()
        db.refresh(req)

        RequirementsRepository.log_event(
            db, req.discovery_session_id, "REQUIREMENT_CONFIRMED", {"requirement_id": str(req.id), "user_id": str(user_id)}
        )
        return req

    @staticmethod
    def answer_question(db: Session, question_id: uuid.UUID, answer_text: str) -> DiscoveryQuestion:
        q = db.query(DiscoveryQuestion).filter(DiscoveryQuestion.id == question_id).first()
        if not q:
            raise ValueError(f"DiscoveryQuestion {question_id} not found")

        q.answer_text = answer_text
        q.status = "ANSWERED"
        q.answered_at = datetime.utcnow()

        db.commit()
        db.refresh(q)

        RequirementsRepository.log_event(
            db, q.discovery_session_id, "QUESTION_ANSWERED", {"question_id": str(q.id)}
        )
        return q
