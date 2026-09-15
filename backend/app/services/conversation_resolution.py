"""Conversation, Business, Lead, and Contact resolution service for inbound messages."""

import uuid
from typing import Optional, Tuple
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.lead import Lead


class ConversationResolver:
    """Deterministically resolves inbound messages to Business, Lead, Contact, and Conversation entities."""

    @staticmethod
    def resolve_conversation(
        db: Session,
        channel: str,
        sender_email: Optional[str] = None,
        sender_phone: Optional[str] = None,
    ) -> Tuple[Optional[Conversation], Optional[Business], Optional[Lead], Optional[Contact]]:
        """
        Resolution Priority:
        1. Contact email / phone match -> Lead -> Business -> Conversation
        2. Business email / phone match -> Lead -> Conversation
        3. Lead notes / title email match -> Business -> Conversation
        """
        contact: Optional[Contact] = None
        lead: Optional[Lead] = None
        business: Optional[Business] = None
        conversation: Optional[Conversation] = None

        # 1. Contact Match
        if sender_email:
            contact = db.query(Contact).filter(Contact.email == sender_email.strip().lower()).first()
        elif sender_phone:
            contact = db.query(Contact).filter(Contact.phone == sender_phone.strip()).first()

        if contact and contact.lead_id:
            lead = db.query(Lead).filter(Lead.id == contact.lead_id).first()
            if lead and lead.business_id:
                business = db.query(Business).filter(Business.id == lead.business_id).first()

        # 2. Business Match
        if not business and sender_email:
            business = db.query(Business).filter(Business.email == sender_email.strip().lower()).first()
        if not business and sender_phone:
            business = db.query(Business).filter(Business.phone == sender_phone.strip()).first()

        if business and not lead:
            lead = db.query(Lead).filter(Lead.business_id == business.id).first()

        # If lead exists but no business
        if lead and not business and lead.business_id:
            business = db.query(Business).filter(Business.id == lead.business_id).first()

        if not lead or not business:
            return None, business, lead, contact

        # 4. Conversation Match or Auto-Create
        conversation = (
            db.query(Conversation)
            .filter((Conversation.lead_id == lead.id) & (Conversation.business_id == business.id))
            .first()
        )

        if not conversation:
            conversation = Conversation(
                lead_id=lead.id,
                business_id=business.id,
                contact_id=contact.id if contact else None,
                channel=channel.upper(),
                status="ACTIVE",
                conversation_stage="NEW_RESPONSE",
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        return conversation, business, lead, contact
