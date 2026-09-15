"""
Phase 65: Data Retention Service
Manages automated retention periods, archiving policies, and legal holds.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import (
    DataRetentionPolicyModel,
    LegalHoldModel
)


class DataRetentionService:
    def __init__(self, db: Session):
        self.db = db

    def create_retention_policy(
        self,
        tenant_id: str,
        name: str,
        dataset_pattern: str,
        retention_days: int,
        action_after_expiry: str = "ARCHIVE",
        legal_basis: Optional[str] = None
    ) -> DataRetentionPolicyModel:
        policy = DataRetentionPolicyModel(
            tenant_id=tenant_id,
            name=name,
            dataset_pattern=dataset_pattern,
            retention_days=retention_days,
            action_after_expiry=action_after_expiry,
            legal_basis=legal_basis,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def list_policies(self, tenant_id: str) -> List[DataRetentionPolicyModel]:
        return self.db.query(DataRetentionPolicyModel).filter(
            DataRetentionPolicyModel.tenant_id == tenant_id
        ).all()

    def create_legal_hold(
        self,
        tenant_id: str,
        matter_name: str,
        custodian_id: str,
        target_scope: Dict[str, Any],
        placed_by: str,
        reason: str
    ) -> LegalHoldModel:
        hold = LegalHoldModel(
            tenant_id=tenant_id,
            matter_name=matter_name,
            custodian_id=custodian_id,
            target_scope=target_scope,
            placed_by=placed_by,
            reason=reason,
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(hold)
        self.db.commit()
        self.db.refresh(hold)
        return hold

    def list_legal_holds(self, tenant_id: str) -> List[LegalHoldModel]:
        return self.db.query(LegalHoldModel).filter(
            LegalHoldModel.tenant_id == tenant_id,
            LegalHoldModel.is_active == True
        ).all()

    def release_legal_hold(self, tenant_id: str, hold_id: str) -> bool:
        hold = self.db.query(LegalHoldModel).filter(
            LegalHoldModel.id == hold_id,
            LegalHoldModel.tenant_id == tenant_id
        ).first()
        if not hold:
            return False
        hold.is_active = False
        hold.released_at = datetime.now(timezone.utc)
        self.db.commit()
        return True
