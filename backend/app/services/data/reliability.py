"""
Phase 65: Data Reliability & SLO Service
Tracks Service Level Objectives (SLOs) and SLAs for freshness, availability,
completeness, latency, and pipeline success.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataSLOModel, DataSLOHistoryModel


class DataReliabilityService:
    def __init__(self, db: Session):
        self.db = db

    def create_slo(
        self,
        tenant_id: str,
        asset_id: str,
        slo_type: str,  # FRESHNESS, AVAILABILITY, COMPLETENESS, LATENCY, PIPELINE_SUCCESS
        target_percentage: float = 99.9,
        target_value: Optional[float] = None
    ) -> DataSLOModel:
        slo = DataSLOModel(
            tenant_id=tenant_id,
            asset_id=asset_id,
            slo_type=slo_type,
            target_percentage=target_percentage,
            current_percentage=target_percentage,
            is_breached=False,
            last_evaluated=datetime.now(timezone.utc)
        )
        self.db.add(slo)
        self.db.commit()
        self.db.refresh(slo)
        return slo

    def record_slo_evaluation(
        self,
        tenant_id: str,
        slo_id: str,
        actual_percentage: float
    ) -> Optional[DataSLOHistoryModel]:
        slo = self.db.query(DataSLOModel).filter(
            DataSLOModel.id == slo_id,
            DataSLOModel.tenant_id == tenant_id
        ).first()
        if not slo:
            return None

        slo.current_percentage = actual_percentage
        slo.is_breached = actual_percentage < slo.target_percentage
        slo.last_evaluated = datetime.now(timezone.utc)

        history = DataSLOHistoryModel(
            slo_id=slo.id,
            measured_percentage=actual_percentage,
            recorded_at=datetime.now(timezone.utc)
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def list_slos(self, tenant_id: str) -> List[DataSLOModel]:
        return self.db.query(DataSLOModel).filter(
            DataSLOModel.tenant_id == tenant_id
        ).all()
