"""
Phase 65: Data Sharing Service
Tracks internal and external data shares, agreements, expiration dates, and access controls.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataShareModel


class DataSharingService:
    def __init__(self, db: Session):
        self.db = db

    def create_share(
        self,
        tenant_id: str,
        name: str,
        shared_by: str,
        recipient_tenant_id: Optional[str],
        recipient_email: Optional[str],
        resource_ids: List[str],
        share_type: str = "INTERNAL",
        expires_days: int = 90
    ) -> DataShareModel:
        share = DataShareModel(
            tenant_id=tenant_id,
            name=name,
            shared_by=shared_by,
            recipient_tenant_id=recipient_tenant_id,
            recipient_email=recipient_email,
            resource_ids=resource_ids,
            share_type=share_type,
            expires_at=datetime.now(timezone.utc) + timedelta(days=expires_days),
            status="ACTIVE",
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        return share

    def revoke_share(self, tenant_id: str, share_id: str) -> bool:
        share = self.db.query(DataShareModel).filter(
            DataShareModel.id == share_id,
            DataShareModel.tenant_id == tenant_id
        ).first()
        if not share:
            return False
        share.status = "REVOKED"
        self.db.commit()
        return True

    def list_shares(self, tenant_id: str) -> List[DataShareModel]:
        return self.db.query(DataShareModel).filter(
            DataShareModel.tenant_id == tenant_id
        ).order_by(DataShareModel.created_at.desc()).all()
