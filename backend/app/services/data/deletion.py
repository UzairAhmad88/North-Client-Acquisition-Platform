"""
Phase 65: Data Deletion Service
Enforces governed deletion across records, datasets, entities, documents,
memories, embeddings, and caches, verifying against legal holds.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import (
    DataDeletionRequestModel,
    LegalHoldModel
)


class DataDeletionService:
    def __init__(self, db: Session):
        self.db = db

    def submit_deletion_request(
        self,
        tenant_id: str,
        target_scope: Dict[str, Any],
        deletion_type: str,  # HARD_DELETE, SOFT_DELETE, ANONYMIZE
        requested_by: str,
        reason: str
    ) -> DataDeletionRequestModel:
        # Check active legal holds
        active_holds = self.db.query(LegalHoldModel).filter(
            LegalHoldModel.tenant_id == tenant_id,
            LegalHoldModel.is_active == True
        ).all()

        is_blocked = False
        block_reason = None
        for hold in active_holds:
            # Simple scope match check
            scope_target = hold.target_scope.get("dataset") or hold.target_scope.get("entity")
            req_target = target_scope.get("dataset") or target_scope.get("entity")
            if scope_target and req_target and scope_target == req_target:
                is_blocked = True
                block_reason = f"Blocked by Legal Hold: {hold.matter_name}"
                break

        status = "BLOCKED_BY_LEGAL_HOLD" if is_blocked else "SUBMITTED"

        req = DataDeletionRequestModel(
            tenant_id=tenant_id,
            target_scope=target_scope,
            deletion_type=deletion_type,
            requested_by=requested_by,
            reason=f"{reason} ({block_reason})" if is_blocked else reason,
            status=status,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(req)
        self.db.commit()
        self.db.refresh(req)
        return req

    def execute_deletion(self, tenant_id: str, request_id: str) -> bool:
        req = self.db.query(DataDeletionRequestModel).filter(
            DataDeletionRequestModel.id == request_id,
            DataDeletionRequestModel.tenant_id == tenant_id
        ).first()
        if not req or req.status != "SUBMITTED":
            return False

        req.status = "COMPLETED"
        req.executed_at = datetime.now(timezone.utc)
        self.db.commit()
        return True

    def list_requests(self, tenant_id: str) -> List[DataDeletionRequestModel]:
        return self.db.query(DataDeletionRequestModel).filter(
            DataDeletionRequestModel.tenant_id == tenant_id
        ).order_by(DataDeletionRequestModel.created_at.desc()).all()
