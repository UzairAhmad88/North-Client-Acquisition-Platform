import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.contact import Contact


class ContactRepository:
    @staticmethod
    def get_by_id(db: Session, contact_id: uuid.UUID) -> Optional[Contact]:
        return db.query(Contact).filter(Contact.id == contact_id).first()

    @staticmethod
    def create(db: Session, contact_data: Dict[str, Any]) -> Contact:
        if contact_data.get("is_primary"):
            # Unset existing primary contact for the same business
            db.query(Contact).filter(
                Contact.business_id == contact_data["business_id"],
                Contact.is_primary == True,  # noqa: E712
            ).update({"is_primary": False})

        contact = Contact(**contact_data)
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact

    @staticmethod
    def list_by_business(db: Session, business_id: uuid.UUID) -> List[Contact]:
        return db.query(Contact).filter(Contact.business_id == business_id).all()

    @staticmethod
    def list_by_lead(db: Session, lead_id: uuid.UUID) -> List[Contact]:
        return db.query(Contact).filter(Contact.lead_id == lead_id).all()

    @staticmethod
    def update(db: Session, contact: Contact, update_data: Dict[str, Any]) -> Contact:
        if update_data.get("is_primary"):
            # Unset other primary contacts for the same business
            db.query(Contact).filter(
                Contact.business_id == contact.business_id,
                Contact.id != contact.id,
                Contact.is_primary == True,  # noqa: E712
            ).update({"is_primary": False})

        for key, value in update_data.items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
        return contact

    @staticmethod
    def delete(db: Session, contact: Contact) -> None:
        db.delete(contact)
        db.commit()
