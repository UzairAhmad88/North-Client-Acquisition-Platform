"""Repository layer for Response & Conversation Intelligence persistence."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.response import ConversationAnalysis, ConversationFact, InboundEventLog


class ResponseRepository:
    """Database access repository for conversation analyses, event logs, and facts."""

    @staticmethod
    def log_inbound_event(db: Session, data: Dict[str, Any]) -> InboundEventLog:
        log = InboundEventLog(
            provider=data["provider"],
            provider_event_id=data["provider_event_id"],
            channel=data.get("channel", "EMAIL"),
            sender=data["sender"],
            recipient=data["recipient"],
            payload=data.get("payload", {}),
            status=data.get("status", "PROCESSED"),
            error_message=data.get("error_message"),
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def create_analysis(db: Session, data: Dict[str, Any]) -> ConversationAnalysis:
        analysis = ConversationAnalysis(
            conversation_id=data["conversation_id"],
            latest_message_id=data.get("latest_message_id"),
            agent_run_id=data.get("agent_run_id"),
            primary_intent=data["primary_intent"],
            all_intents=data.get("all_intents", []),
            intent_confidence=data.get("intent_confidence", "HIGH"),
            buying_signal_level=data.get("buying_signal_level", "NONE"),
            objection_type=data.get("objection_type"),
            extracted_requirements=data.get("extracted_requirements", []),
            missing_information=data.get("missing_information", []),
            conversation_stage=data.get("conversation_stage", "NEW_RESPONSE"),
            recommended_next_action=data["recommended_next_action"],
            recommended_next_action_reason=data.get("recommended_next_action_reason"),
            next_action_confidence=data.get("next_action_confidence", "HIGH"),
            sentiment_signal=data.get("sentiment_signal", "NEUTRAL"),
            priority=data.get("priority", "NORMAL"),
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    @staticmethod
    def get_latest_analysis(db: Session, conversation_id: uuid.UUID) -> Optional[ConversationAnalysis]:
        return (
            db.query(ConversationAnalysis)
            .filter(ConversationAnalysis.conversation_id == conversation_id)
            .order_by(ConversationAnalysis.created_at.desc())
            .first()
        )

    @staticmethod
    def record_human_correction(
        db: Session, analysis: ConversationAnalysis, user_id: uuid.UUID, correction_data: Dict[str, Any]
    ) -> ConversationAnalysis:
        analysis.human_correction = correction_data
        analysis.human_correction_by_id = user_id
        analysis.human_correction_at = datetime.utcnow()
        db.commit()
        db.refresh(analysis)
        return analysis
