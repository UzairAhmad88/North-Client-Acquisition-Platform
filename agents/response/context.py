"""Bounded conversation context builder for Response Agent."""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.conversation import Conversation
from app.models.lead import Lead
from app.models.message import Message


class BoundedContextBuilder:
    """Builds authoritative, bounded context for Response Agent evaluation."""

    @staticmethod
    def build_context(
        db: Session, conversation_id: uuid.UUID, max_messages: int = 20
    ) -> Dict[str, Any]:
        conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            return {}

        lead = db.query(Lead).filter(Lead.id == conv.lead_id).first()
        business = db.query(Business).filter(Business.id == conv.business_id).first()

        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.created_at.desc())
            .limit(max_messages)
            .all()
        )
        messages.reverse()  # Chronological order

        msg_history = [
            {
                "id": str(m.id),
                "direction": m.direction,
                "channel": m.channel,
                "subject": m.subject,
                "body": m.body,
                "sent_at": str(m.sent_at or m.created_at),
            }
            for m in messages
        ]

        latest_msg = messages[-1] if messages else None

        return {
            "conversation_id": str(conv.id),
            "lead_id": str(conv.lead_id),
            "business_id": str(conv.business_id),
            "business_name": business.name if business else "Unknown",
            "business_domain": business.website_url if business else None,
            "business_email": business.email if business else None,
            "lead_title": lead.title if lead else "Unknown",
            "messages": msg_history,
            "latest_message": {
                "id": str(latest_msg.id),
                "direction": latest_msg.direction,
                "body": latest_msg.body,
                "subject": latest_msg.subject,
            }
            if latest_msg
            else None,
        }
