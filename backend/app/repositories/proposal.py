"""Proposal Repository handling database queries for commercial proposals."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.proposal import Proposal, ProposalItem, ProposalVersion


class ProposalRepository:
    """Repository methods for proposals, items, and historical versions."""

    @staticmethod
    def get_proposal(db: Session, proposal_id: uuid.UUID) -> Optional[Proposal]:
        return db.query(Proposal).filter(Proposal.id == proposal_id).first()

    @staticmethod
    def list_proposals(
        db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[Proposal]:
        query = db.query(Proposal)
        if status:
            query = query.filter(Proposal.status == status)
        return query.order_by(Proposal.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def create_proposal(db: Session, proposal_data: dict) -> Proposal:
        prop = Proposal(**proposal_data)
        db.add(prop)
        db.commit()
        db.refresh(prop)
        return prop

    @staticmethod
    def create_item(db: Session, item_data: dict) -> ProposalItem:
        item = ProposalItem(**item_data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def create_version(db: Session, version_data: dict) -> ProposalVersion:
        ver = ProposalVersion(**version_data)
        db.add(ver)
        db.commit()
        db.refresh(ver)
        return ver

    @staticmethod
    def get_versions_for_proposal(db: Session, proposal_id: uuid.UUID) -> List[ProposalVersion]:
        return (
            db.query(ProposalVersion)
            .filter(ProposalVersion.proposal_id == proposal_id)
            .order_by(ProposalVersion.version.desc())
            .all()
        )
