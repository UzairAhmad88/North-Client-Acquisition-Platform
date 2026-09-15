"""Do-Not-Contact (DNC) checker and registry management service."""

import uuid
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.dnc import DoNotContact


class DncService:
    """Service enforcing DNC registry lookups and entry management."""

    @staticmethod
    def is_blocked(
        db: Session,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        contact_id: Optional[uuid.UUID] = None,
        business_id: Optional[uuid.UUID] = None,
        lead_id: Optional[uuid.UUID] = None,
    ) -> Tuple[bool, str]:
        """Check if target email, phone, contact, business, or lead is listed in active DNC registry."""
        query = db.query(DoNotContact).filter(DoNotContact.is_active == True)

        targets = []
        if email:
            targets.append(("EMAIL", email.strip().lower()))
        if phone:
            targets.append(("PHONE", phone.strip()))
        if contact_id:
            targets.append(("CONTACT", str(contact_id)))
        if business_id:
            targets.append(("BUSINESS", str(business_id)))
        if lead_id:
            targets.append(("LEAD", str(lead_id)))

        for scope, val in targets:
            match = query.filter(
                (DoNotContact.scope == scope) & (DoNotContact.target_value == val)
            ).first()
            if match:
                return True, f"Blocked by DNC entry ({scope}: {val}). Reason: {match.reason or 'Unspecified'}"

        # Global DNC check
        global_match = query.filter(DoNotContact.scope == "GLOBAL").first()
        if global_match:
            return True, f"Blocked by GLOBAL DNC record. Reason: {global_match.reason}"

        return False, ""

    @staticmethod
    def add_dnc_entry(
        db: Session,
        scope: str,
        target_value: str,
        reason: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None,
    ) -> DoNotContact:
        entry = DoNotContact(
            scope=scope.upper(),
            target_value=target_value.strip().lower() if scope.upper() == "EMAIL" else target_value.strip(),
            reason=reason,
            created_by_user_id=user_id,
            is_active=True,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
