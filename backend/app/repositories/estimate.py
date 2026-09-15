"""Estimate Repository handling database queries for project estimates."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.estimate import (
    EstimateCostItem,
    EstimateScenario,
    EstimateVersion,
    EstimateWorkItem,
    ProjectEstimate,
)


class EstimateRepository:
    """Repository methods for project estimates, work items, costs, scenarios, and versions."""

    @staticmethod
    def get_estimate(db: Session, estimate_id: uuid.UUID) -> Optional[ProjectEstimate]:
        return db.query(ProjectEstimate).filter(ProjectEstimate.id == estimate_id).first()

    @staticmethod
    def list_estimates(
        db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> List[ProjectEstimate]:
        query = db.query(ProjectEstimate)
        if status:
            query = query.filter(ProjectEstimate.status == status)
        return query.order_by(ProjectEstimate.updated_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def create_estimate(db: Session, estimate_data: dict) -> ProjectEstimate:
        est = ProjectEstimate(**estimate_data)
        db.add(est)
        db.commit()
        db.refresh(est)
        return est

    @staticmethod
    def create_work_item(db: Session, work_item_data: dict) -> EstimateWorkItem:
        item = EstimateWorkItem(**work_item_data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def create_cost_item(db: Session, cost_data: dict) -> EstimateCostItem:
        cost = EstimateCostItem(**cost_data)
        db.add(cost)
        db.commit()
        db.refresh(cost)
        return cost

    @staticmethod
    def create_scenario(db: Session, scenario_data: dict) -> EstimateScenario:
        scen = EstimateScenario(**scenario_data)
        db.add(scen)
        db.commit()
        db.refresh(scen)
        return scen

    @staticmethod
    def create_version(db: Session, version_data: dict) -> EstimateVersion:
        ver = EstimateVersion(**version_data)
        db.add(ver)
        db.commit()
        db.refresh(ver)
        return ver
