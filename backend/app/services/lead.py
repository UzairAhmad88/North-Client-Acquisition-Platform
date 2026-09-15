import re
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.core.exceptions import AppError
from app.models.lead import Lead
from app.repositories.business import BusinessRepository
from app.repositories.contact import ContactRepository
from app.repositories.lead import LeadRepository
from app.schemas.lead import (
    LeadCreate,
    LeadDataQuality,
    LeadDuplicateCheckResponse,
    LeadDuplicateMatch,
    LeadStatus,
    LeadUpdate,
)


class LeadService:
    @staticmethod
    def normalize_title(title: str) -> str:
        if not title:
            return ""
        cleaned = re.sub(r"[^\w\s]", "", title.lower())
        return re.sub(r"\s+", " ", cleaned).strip()

    @classmethod
    def calculate_data_quality(cls, db: Session, lead: Lead) -> LeadDataQuality:
        score = 100
        missing_fields: List[str] = []
        warnings: List[str] = []

        if not lead.description or not lead.description.strip():
            score -= 15
            missing_fields.append("description")

        if lead.estimated_value is None or lead.estimated_value <= 0:
            score -= 15
            missing_fields.append("estimated_value")
            warnings.append("No estimated opportunity value specified.")

        if not lead.next_action or not lead.next_action.strip():
            score -= 15
            missing_fields.append("next_action")
            warnings.append("No next action plan recorded.")

        contacts = ContactRepository.list_by_lead(db, lead.id)
        has_primary = any(c.is_primary for c in contacts)
        if not contacts:
            score -= 25
            missing_fields.append("contacts")
            warnings.append("No contacts linked to this lead.")
        elif not has_primary:
            score -= 10
            warnings.append("No primary contact designated.")

        if lead.qualification_status == "UNQUALIFIED":
            score -= 10
            warnings.append("Lead is unqualified.")

        if lead.contactability_status == "UNKNOWN":
            score -= 10
            warnings.append("Contactability status is unknown.")

        return LeadDataQuality(
            score=max(0, score),
            missing_fields=missing_fields,
            warnings=warnings,
        )

    @classmethod
    def check_duplicates(
        cls,
        db: Session,
        business_id: uuid.UUID,
        title: str,
        exclude_id: Optional[uuid.UUID] = None,
    ) -> LeadDuplicateCheckResponse:
        norm_title = cls.normalize_title(title)
        candidates = LeadRepository.find_candidate_duplicates(
            db, business_id=business_id, title=title, exclude_id=exclude_id
        )

        matches: List[LeadDuplicateMatch] = []
        all_signals: set[str] = set()
        max_confidence = 0.0

        for candidate in candidates:
            cand_norm = cls.normalize_title(candidate.title)
            signals: List[str] = []
            cand_confidence = 0.0

            if cand_norm == norm_title:
                signals.append("same_business_and_title")
                cand_confidence = max(cand_confidence, 0.95)

            if candidate.status in ["NEW", "RESEARCHING", "QUALIFIED", "CONTACTED", "INTERESTED"]:
                signals.append("same_business_active_lead")
                cand_confidence = max(cand_confidence, 0.75)

            if signals:
                all_signals.update(signals)
                max_confidence = max(max_confidence, cand_confidence)
                matches.append(
                    LeadDuplicateMatch(
                        lead_id=candidate.id,
                        title=candidate.title,
                        status=candidate.status,
                        confidence=round(cand_confidence, 2),
                        signals=signals,
                    )
                )

        possible_duplicate = max_confidence >= 0.70
        return LeadDuplicateCheckResponse(
            possible_duplicate=possible_duplicate,
            confidence=round(max_confidence, 2),
            signals=sorted(list(all_signals)),
            matches=matches,
        )

    @classmethod
    def create_lead(
        cls,
        db: Session,
        lead_in: LeadCreate,
        creator_user_id: Optional[uuid.UUID] = None,
    ) -> Lead:
        # Validate business exists
        business = BusinessRepository.get_by_id(db, lead_in.business_id)
        if not business:
            raise AppError(
                code="BUSINESS_NOT_FOUND",
                message="Referenced Business does not exist.",
                status_code=404,
            )

        lead_data = lead_in.model_dump()
        if not lead_data.get("owner_user_id") and creator_user_id:
            lead_data["owner_user_id"] = creator_user_id

        lead_data["status"] = "NEW"
        if isinstance(lead_data.get("priority"), Enum):
            lead_data["priority"] = lead_data["priority"].value
        if isinstance(lead_data.get("qualification_status"), Enum):
            lead_data["qualification_status"] = lead_data["qualification_status"].value
        if isinstance(lead_data.get("contactability_status"), Enum):
            lead_data["contactability_status"] = lead_data["contactability_status"].value

        lead = LeadRepository.create(db, lead_data)
        return lead

    @classmethod
    def get_lead(cls, db: Session, lead_id: uuid.UUID) -> Lead:
        lead = LeadRepository.get_by_id(db, lead_id)
        if not lead:
            raise AppError(
                code="LEAD_NOT_FOUND",
                message="Lead record not found.",
                status_code=404,
            )
        return lead

    @classmethod
    def list_leads(
        cls,
        db: Session,
        page: int = 1,
        page_size: int = 25,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        qualification_status: Optional[str] = None,
        contactability_status: Optional[str] = None,
        source: Optional[str] = None,
        owner_user_id: Optional[uuid.UUID] = None,
        business_id: Optional[uuid.UUID] = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> Tuple[List[Lead], int]:
        return LeadRepository.list_leads(
            db=db,
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            priority=priority,
            qualification_status=qualification_status,
            contactability_status=contactability_status,
            source=source,
            owner_user_id=owner_user_id,
            business_id=business_id,
            sort=sort,
            order=order,
        )

    @classmethod
    def update_lead(cls, db: Session, lead_id: uuid.UUID, lead_in: LeadUpdate) -> Lead:
        lead = cls.get_lead(db, lead_id)
        update_dict = lead_in.model_dump(exclude_unset=True)

        for enum_field in ["status", "priority", "qualification_status", "contactability_status"]:
            if enum_field in update_dict and hasattr(update_dict[enum_field], "value"):
                update_dict[enum_field] = update_dict[enum_field].value

        if "status" in update_dict:
            cls._apply_status_timestamps(lead, update_dict["status"])

        return LeadRepository.update(db, lead, update_dict)

    @classmethod
    def transition_lead_status(
        cls,
        db: Session,
        lead_id: uuid.UUID,
        target_status: LeadStatus,
        loss_reason: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Lead:
        lead = cls.get_lead(db, lead_id)
        status_val = target_status.value if isinstance(target_status, Enum) else str(target_status)

        update_dict: Dict[str, Any] = {"status": status_val}
        if loss_reason:
            update_dict["loss_reason"] = loss_reason
        if notes:
            ts = datetime.now(timezone.utc).isoformat()
            update_dict["notes"] = (
                lead.notes or ""
            ) + f"\n[{ts}] Status changed to {status_val}: {notes}"

        cls._apply_status_timestamps(lead, status_val)
        return LeadRepository.update(db, lead, update_dict)

    @classmethod
    def assign_lead(
        cls, db: Session, lead_id: uuid.UUID, owner_user_id: Optional[uuid.UUID]
    ) -> Lead:
        lead = cls.get_lead(db, lead_id)
        return LeadRepository.update(db, lead, {"owner_user_id": owner_user_id})

    @classmethod
    def archive_lead(cls, db: Session, lead_id: uuid.UUID) -> Lead:
        lead = cls.get_lead(db, lead_id)
        if lead.status == "ARCHIVED":
            return lead
        return LeadRepository.archive(db, lead)

    @classmethod
    def restore_lead(cls, db: Session, lead_id: uuid.UUID) -> Lead:
        lead = cls.get_lead(db, lead_id)
        if lead.status != "ARCHIVED":
            return lead
        return LeadRepository.restore(db, lead)

    @staticmethod
    def _apply_status_timestamps(lead: Lead, new_status: str) -> None:
        now = datetime.now(timezone.utc)
        if new_status in ["CONTACTED", "RESPONDED", "INTERESTED", "MEETING", "PROPOSAL"]:
            if not lead.first_contacted_at:
                lead.first_contacted_at = now
            lead.last_contacted_at = now
        elif new_status == "WON":
            lead.converted_at = now
        elif new_status == "LOST":
            lead.lost_at = now
