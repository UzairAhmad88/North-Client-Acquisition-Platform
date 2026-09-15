"""Requirements Repository handling database access for discovery sessions and requirements."""

import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.requirements import (
    ClientRequirement,
    DiscoveryEvent,
    DiscoveryQuestion,
    DiscoverySession,
    RequirementDependency,
    RequirementEvidence,
    RequirementScopeItem,
)


class RequirementsRepository:
    """Repository methods for discovery sessions, requirements, evidence, dependencies, questions, and scope items."""

    @staticmethod
    def get_discovery_session(db: Session, session_id: uuid.UUID) -> Optional[DiscoverySession]:
        return db.query(DiscoverySession).filter(DiscoverySession.id == session_id).first()

    @staticmethod
    def get_discovery_session_by_business(db: Session, business_id: uuid.UUID) -> Optional[DiscoverySession]:
        return (
            db.query(DiscoverySession)
            .filter(DiscoverySession.business_id == business_id)
            .order_by(DiscoverySession.created_at.desc())
            .first()
        )

    @staticmethod
    def list_discovery_sessions(
        db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[DiscoverySession]:
        query = db.query(DiscoverySession)
        if status:
            query = query.filter(DiscoverySession.status == status)
        return query.order_by(DiscoverySession.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def create_discovery_session(db: Session, session_data: dict) -> DiscoverySession:
        session_obj = DiscoverySession(**session_data)
        db.add(session_obj)
        db.commit()
        db.refresh(session_obj)
        return session_obj

    @staticmethod
    def get_requirements_for_session(db: Session, session_id: uuid.UUID) -> List[ClientRequirement]:
        return (
            db.query(ClientRequirement)
            .filter(ClientRequirement.discovery_session_id == session_id)
            .order_by(ClientRequirement.created_at.asc())
            .all()
        )

    @staticmethod
    def get_requirement(db: Session, requirement_id: uuid.UUID) -> Optional[ClientRequirement]:
        return db.query(ClientRequirement).filter(ClientRequirement.id == requirement_id).first()

    @staticmethod
    def create_requirement(db: Session, req_data: dict) -> ClientRequirement:
        req_obj = ClientRequirement(**req_data)
        db.add(req_obj)
        db.commit()
        db.refresh(req_obj)
        return req_obj

    @staticmethod
    def create_evidence(db: Session, evidence_data: dict) -> RequirementEvidence:
        evidence_obj = RequirementEvidence(**evidence_data)
        db.add(evidence_obj)
        db.commit()
        db.refresh(evidence_obj)
        return evidence_obj

    @staticmethod
    def get_questions_for_session(db: Session, session_id: uuid.UUID) -> List[DiscoveryQuestion]:
        return (
            db.query(DiscoveryQuestion)
            .filter(DiscoveryQuestion.discovery_session_id == session_id)
            .order_by(DiscoveryQuestion.priority.asc(), DiscoveryQuestion.created_at.asc())
            .all()
        )

    @staticmethod
    def create_question(db: Session, question_data: dict) -> DiscoveryQuestion:
        q_obj = DiscoveryQuestion(**question_data)
        db.add(q_obj)
        db.commit()
        db.refresh(q_obj)
        return q_obj

    @staticmethod
    def get_scope_items_for_session(db: Session, session_id: uuid.UUID) -> List[RequirementScopeItem]:
        return (
            db.query(RequirementScopeItem)
            .filter(RequirementScopeItem.discovery_session_id == session_id)
            .order_by(RequirementScopeItem.created_at.asc())
            .all()
        )

    @staticmethod
    def create_scope_item(db: Session, scope_data: dict) -> RequirementScopeItem:
        scope_obj = RequirementScopeItem(**scope_data)
        db.add(scope_obj)
        db.commit()
        db.refresh(scope_obj)
        return scope_obj

    @staticmethod
    def log_event(db: Session, session_id: uuid.UUID, event_type: str, payload: dict) -> DiscoveryEvent:
        event = DiscoveryEvent(discovery_session_id=session_id, event_type=event_type, payload=payload)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
