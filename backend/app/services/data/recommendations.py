"""
Phase 65: Data Optimization Recommendations Service
Generates actionable recommendations for partitioning, indexing, caching, compression,
and storage tiering with measurable evidence.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataRecommendationModel


class DataRecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def create_recommendation(
        self,
        tenant_id: str,
        asset_id: str,
        recommendation_type: str,  # PARTITIONING, INDEXING, CACHING, COMPRESSION, ARCHIVE
        description: str,
        potential_savings_usd: float,
        evidence: Dict[str, Any]
    ) -> DataRecommendationModel:
        rec = DataRecommendationModel(
            tenant_id=tenant_id,
            asset_id=asset_id,
            recommendation_type=recommendation_type,
            description=description,
            potential_savings_usd=potential_savings_usd,
            evidence=evidence,
            status="PENDING",
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def apply_recommendation(self, tenant_id: str, rec_id: str) -> bool:
        rec = self.db.query(DataRecommendationModel).filter(
            DataRecommendationModel.id == rec_id,
            DataRecommendationModel.tenant_id == tenant_id
        ).first()
        if not rec:
            return False
        rec.status = "APPLIED"
        self.db.commit()
        return True

    def list_recommendations(self, tenant_id: str, status: Optional[str] = None) -> List[DataRecommendationModel]:
        query = self.db.query(DataRecommendationModel).filter(DataRecommendationModel.tenant_id == tenant_id)
        if status:
            query = query.filter(DataRecommendationModel.status == status)
        return query.order_by(DataRecommendationModel.created_at.desc()).all()
