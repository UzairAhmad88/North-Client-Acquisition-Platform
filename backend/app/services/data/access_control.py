"""
Phase 65: Data Access Control Service
Handles RBAC, ABAC, row-level security (RLS), column-level security (CLS),
and purpose-based data access requests and grants.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import (
    DataAccessPolicyModel,
    DataAccessRequestModel,
    DataAccessGrantModel
)


class DataAccessControlService:
    def __init__(self, db: Session):
        self.db = db

    def create_policy(
        self,
        tenant_id: str,
        name: str,
        policy_type: str,
        resource_pattern: str,
        rules: Dict[str, Any],
        row_level_filters: Optional[Dict[str, Any]] = None,
        column_masks: Optional[Dict[str, Any]] = None,
        is_active: bool = True
    ) -> DataAccessPolicyModel:
        policy = DataAccessPolicyModel(
            tenant_id=tenant_id,
            name=name,
            policy_type=policy_type,
            resource_pattern=resource_pattern,
            rules=rules,
            row_level_filters=row_level_filters or {},
            column_masks=column_masks or {},
            is_active=is_active,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(policy)
        self.db.commit()
        self.db.refresh(policy)
        return policy

    def list_policies(self, tenant_id: str) -> List[DataAccessPolicyModel]:
        return self.db.query(DataAccessPolicyModel).filter(
            DataAccessPolicyModel.tenant_id == tenant_id
        ).all()

    def create_request(
        self,
        tenant_id: str,
        requester_id: str,
        requester_type: str,
        target_resource: str,
        access_level: str,
        business_justification: str,
        intended_purpose: str,
        duration_hours: int = 72
    ) -> DataAccessRequestModel:
        request = DataAccessRequestModel(
            tenant_id=tenant_id,
            requester_id=requester_id,
            requester_type=requester_type,
            target_resource=target_resource,
            access_level=access_level,
            business_justification=business_justification,
            intended_purpose=intended_purpose,
            status="PENDING",
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(request)
        self.db.commit()
        self.db.refresh(request)
        return request

    def approve_request(
        self,
        tenant_id: str,
        request_id: str,
        approver_id: str,
        duration_days: int = 30
    ) -> Optional[DataAccessGrantModel]:
        request = self.db.query(DataAccessRequestModel).filter(
            DataAccessRequestModel.id == request_id,
            DataAccessRequestModel.tenant_id == tenant_id
        ).first()
        if not request:
            return None

        request.status = "APPROVED"
        request.reviewed_by = approver_id
        request.reviewed_at = datetime.now(timezone.utc)

        grant = DataAccessGrantModel(
            tenant_id=tenant_id,
            request_id=request.id,
            grantee_id=request.requester_id,
            grantee_type=request.requester_type,
            resource_uri=request.target_resource,
            access_level=request.access_level,
            valid_until=datetime.now(timezone.utc) + timedelta(days=duration_days),
            granted_by=approver_id,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(grant)
        self.db.commit()
        self.db.refresh(grant)
        return grant

    def list_requests(self, tenant_id: str, status: Optional[str] = None) -> List[DataAccessRequestModel]:
        if not self.db:
            return []
        query = self.db.query(DataAccessRequestModel).filter(DataAccessRequestModel.tenant_id == tenant_id)
        if status:
            query = query.filter(DataAccessRequestModel.status == status)
        return query.order_by(DataAccessRequestModel.created_at.desc()).all()

    def list_grants(self, tenant_id: str) -> List[DataAccessGrantModel]:
        if not self.db:
            return []
        return self.db.query(DataAccessGrantModel).filter(
            DataAccessGrantModel.tenant_id == tenant_id
        ).all()
