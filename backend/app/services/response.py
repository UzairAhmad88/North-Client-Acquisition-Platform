"""Service layer orchestrating inbound response processing and Response Agent analysis."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.orm import Session

from agents.core.context import AgentContext
from agents.response import response_agent
from agents.response.context import BoundedContextBuilder
from app.core.exceptions import AppError
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.outreach import OutreachDraft
from app.models.response import ConversationAnalysis
from app.repositories.outreach import OutreachDraftRepository
from app.repositories.response import ResponseRepository
from app.services.conversation_resolution import ConversationResolver
from app.services.risk import RiskService
from integrations.inbound.models import InboundMessagePayload
from integrations.inbound.opt_out import DeterministicOptOutDetector
from integrations.inbound.security import WebhookSecurityGuard


class ResponseService:
    """Central service handling inbound communication workflows and response intelligence."""

    @staticmethod
    async def process_inbound_message(
        db: Session, payload: InboundMessagePayload
    ) -> Tuple[Message, Conversation, Optional[ConversationAnalysis]]:
        """
        Inbound Processing Flow:
        1. Check idempotency deduplication
        2. Resolve Conversation/Business/Lead/Contact
        3. Persist Message & log event
        4. Check deterministic Opt-Out -> Update DNC & Conversation status
        5. Execute ResponseAgent analysis if active
        """
        # 1. Idempotency Check
        is_dup, dup_err = WebhookSecurityGuard.is_duplicate_event(db, payload.provider, payload.provider_event_id)
        if is_dup:
            ResponseRepository.log_inbound_event(
                db,
                {
                    "provider": payload.provider,
                    "provider_event_id": payload.provider_event_id,
                    "channel": payload.channel,
                    "sender": payload.sender_email or payload.sender_phone or "unknown",
                    "recipient": payload.recipient_address,
                    "payload": payload.model_dump(),
                    "status": "DUPLICATE",
                    "error_message": dup_err,
                },
            )
            raise AppError(code="DUPLICATE_EVENT", message=dup_err, status_code=409)

        # 2. Resolve Conversation
        conv, biz, lead, contact = ConversationResolver.resolve_conversation(
            db,
            channel=payload.channel,
            sender_email=payload.sender_email,
            sender_phone=payload.sender_phone,
        )

        if not conv:
            ResponseRepository.log_inbound_event(
                db,
                {
                    "provider": payload.provider,
                    "provider_event_id": payload.provider_event_id,
                    "channel": payload.channel,
                    "sender": payload.sender_email or payload.sender_phone or "unknown",
                    "recipient": payload.recipient_address,
                    "payload": payload.model_dump(),
                    "status": "UNRESOLVED",
                    "error_message": "Could not resolve message to existing business or lead entity",
                },
            )
            raise AppError(code="CONVERSATION_UNRESOLVED", message="Unresolved conversation target", status_code=404)

        # 3. Persist Inbound Message
        msg = Message(
            conversation_id=conv.id,
            direction="INBOUND",
            channel=payload.channel,
            subject=payload.subject,
            body=payload.body,
            status="DELIVERED",
            provider_message_id=payload.provider_event_id,
            sent_at=payload.received_at,
        )
        db.add(msg)

        conv.last_inbound_at = datetime.utcnow()
        db.commit()
        db.refresh(msg)
        db.refresh(conv)

        # Log inbound event
        ResponseRepository.log_inbound_event(
            db,
            {
                "provider": payload.provider,
                "provider_event_id": payload.provider_event_id,
                "channel": payload.channel,
                "sender": payload.sender_email or payload.sender_phone or "unknown",
                "recipient": payload.recipient_address,
                "payload": payload.model_dump(mode="json"),
                "status": "PROCESSED",
            },
        )

        # 4. Deterministic Opt-Out Check
        is_opt_out, opt_reason = DeterministicOptOutDetector.process_opt_out_if_present(
            db,
            text=payload.body,
            sender_email=payload.sender_email,
            sender_phone=payload.sender_phone,
            business_id=conv.business_id,
        )
        if is_opt_out:
            conv.status = "OPTED_OUT"
            conv.current_intent = "OPT_OUT"
            conv.conversation_stage = "OPTED_OUT"
            conv.next_action = "MARK_DO_NOT_CONTACT"
            db.commit()

            # Record Opt-Out Analysis record
            analysis_data = {
                "conversation_id": conv.id,
                "latest_message_id": msg.id,
                "primary_intent": "OPT_OUT",
                "all_intents": ["OPT_OUT"],
                "intent_confidence": "HIGH",
                "buying_signal_level": "NONE",
                "conversation_stage": "OPTED_OUT",
                "recommended_next_action": "MARK_DO_NOT_CONTACT",
                "recommended_next_action_reason": opt_reason,
            }
            analysis = ResponseRepository.create_analysis(db, analysis_data)
            return msg, conv, analysis

        # 5. Run Response Agent Analysis
        analysis = await ResponseService.analyze_conversation(db, conv.id)
        return msg, conv, analysis

    @staticmethod
    async def analyze_conversation(db: Session, conversation_id: uuid.UUID) -> ConversationAnalysis:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise AppError(code="CONVERSATION_NOT_FOUND", message="Conversation not found", status_code=404)

        context_data = BoundedContextBuilder.build_context(db, conversation_id)
        if not context_data:
            raise AppError(code="CONTEXT_EMPTY", message="Failed to build conversation context", status_code=400)

        agent_ctx = AgentContext(
            workflow_id=f"wf-resp-{conv.id.hex[:8]}",
            task_id=f"task-resp-{conv.id.hex[:8]}",
            agent_run_id=str(uuid.uuid4()),
            lead_id=conv.lead_id,
            business_id=conv.business_id,
            metadata=context_data,
        )

        agent_res = await response_agent.run(agent_ctx)
        payload = agent_res.result or {}

        latest_msg = context_data.get("latest_message")
        latest_msg_id = uuid.UUID(latest_msg["id"]) if latest_msg else None

        analysis_data = {
            "conversation_id": conv.id,
            "latest_message_id": latest_msg_id,
            "agent_run_id": uuid.UUID(agent_ctx.agent_run_id),
            "primary_intent": payload.get("primary_intent", "AMBIGUOUS"),
            "all_intents": payload.get("all_intents", []),
            "intent_confidence": payload.get("intent_confidence", "HIGH"),
            "buying_signal_level": payload.get("buying_signal", {}).get("level", "NONE"),
            "objection_type": payload.get("objection", {}).get("type") if payload.get("objection") else None,
            "extracted_requirements": [r if isinstance(r, dict) else r.dict() for r in payload.get("extracted_requirements", [])],
            "missing_information": payload.get("missing_information", []),
            "conversation_stage": payload.get("conversation_stage", "NEW_RESPONSE"),
            "recommended_next_action": payload.get("recommended_next_action", "ESCALATE_TO_HUMAN"),
            "recommended_next_action_reason": payload.get("recommended_next_action_reason"),
            "next_action_confidence": payload.get("next_action_confidence", "HIGH"),
            "sentiment_signal": payload.get("sentiment_signal", "NEUTRAL"),
            "priority": payload.get("priority", "NORMAL"),
        }

        analysis = ResponseRepository.create_analysis(db, analysis_data)

        # Update Conversation Intelligence State
        conv.current_intent = analysis.primary_intent
        conv.conversation_stage = analysis.conversation_stage
        conv.next_action = analysis.recommended_next_action
        conv.priority = analysis.priority
        db.commit()

        # If draft generated by agent, create OutreachDraft & evaluate Risk Engine
        draft_sub = payload.get("draft_subject")
        draft_body = payload.get("draft_body")
        if draft_body:
            draft_data = {
                "lead_id": conv.lead_id,
                "business_id": conv.business_id,
                "channel": conv.channel,
                "subject": draft_sub,
                "body": draft_body,
                "approval_status": "PENDING_APPROVAL",
                "version": 1,
            }
            draft = OutreachDraftRepository.create_draft(db, draft_data)
            await RiskService.evaluate_outreach_draft(db, draft.id)

        return analysis

    @staticmethod
    def get_conversation_detail(db: Session, conversation_id: uuid.UUID) -> Conversation:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            raise AppError(code="CONVERSATION_NOT_FOUND", message="Conversation not found", status_code=404)
        return conv

    @staticmethod
    def list_conversations(
        db: Session, limit: int = 20, offset: int = 0, status_filter: Optional[str] = None
    ) -> List[Conversation]:
        query = db.query(Conversation)
        if status_filter:
            query = query.filter(Conversation.status == status_filter.upper())
        return query.order_by(Conversation.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def record_human_correction(
        db: Session, conversation_id: uuid.UUID, user_id: uuid.UUID, correction: Dict[str, Any]
    ) -> ConversationAnalysis:
        analysis = ResponseRepository.get_latest_analysis(db, conversation_id)
        if not analysis:
            raise AppError(code="ANALYSIS_NOT_FOUND", message="No conversation analysis found", status_code=404)

        updated = ResponseRepository.record_human_correction(db, analysis, user_id, correction)

        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conv:
            if correction.get("corrected_intent"):
                conv.current_intent = correction["corrected_intent"]
            if correction.get("corrected_next_action"):
                conv.next_action = correction["corrected_next_action"]
            db.commit()

        return updated
