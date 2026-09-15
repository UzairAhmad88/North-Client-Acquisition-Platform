"""Solution Repository handling database queries for solution designs."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.solution import (
    SolutionAssumption,
    SolutionDeliverable,
    SolutionDependency,
    SolutionDesign,
    SolutionFeature,
    SolutionIntegration,
    SolutionRequirementLink,
)


class SolutionRepository:
    """Repository methods for solution designs, features, deliverables, and dependencies."""

    @staticmethod
    def get_solution(db: Session, solution_id: uuid.UUID) -> Optional[SolutionDesign]:
        return db.query(SolutionDesign).filter(SolutionDesign.id == solution_id).first()

    @staticmethod
    def list_solutions(
        db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[SolutionDesign]:
        query = db.query(SolutionDesign)
        if status:
            query = query.filter(SolutionDesign.status == status)
        return query.order_by(SolutionDesign.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def create_solution(db: Session, solution_data: dict) -> SolutionDesign:
        sol_obj = SolutionDesign(**solution_data)
        db.add(sol_obj)
        db.commit()
        db.refresh(sol_obj)
        return sol_obj

    @staticmethod
    def create_feature(db: Session, feature_data: dict) -> SolutionFeature:
        feat = SolutionFeature(**feature_data)
        db.add(feat)
        db.commit()
        db.refresh(feat)
        return feat

    @staticmethod
    def create_deliverable(db: Session, deliverable_data: dict) -> SolutionDeliverable:
        deliv = SolutionDeliverable(**deliverable_data)
        db.add(deliv)
        db.commit()
        db.refresh(deliv)
        return deliv

    @staticmethod
    def create_integration(db: Session, integration_data: dict) -> SolutionIntegration:
        integ = SolutionIntegration(**integration_data)
        db.add(integ)
        db.commit()
        db.refresh(integ)
        return integ

    @staticmethod
    def create_assumption(db: Session, assumption_data: dict) -> SolutionAssumption:
        assump = SolutionAssumption(**assumption_data)
        db.add(assump)
        db.commit()
        db.refresh(assump)
        return assump

    @staticmethod
    def create_requirement_link(db: Session, link_data: dict) -> SolutionRequirementLink:
        link = SolutionRequirementLink(**link_data)
        db.add(link)
        db.commit()
        db.refresh(link)
        return link
