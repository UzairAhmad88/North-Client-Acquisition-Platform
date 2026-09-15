"""
Phase 65: Data Security Monitoring & Audit Service
Monitors unusual queries, large exports, sensitive data access, and logs comprehensive audits.
"""

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import (
    DataSecurityEventModel,
    DataAuditEventModel
)


class DataSecurityService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self._security_events: List[DataSecurityEventModel] = []
        self._audit_events: List[DataAuditEventModel] = []

    def record_security_event(
        self,
        tenant_id: str,
        event_type: str,
        severity: str,
        description: str,
        actor_id: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> DataSecurityEventModel:
        event = DataSecurityEventModel(
            id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            user_or_agent=actor_id,
            action=event_type,
            dataset_name=description,
            result="ALLOWED" if severity not in ["CRITICAL", "HIGH"] else "BLOCKED",
            risk_score=0.9 if severity == "CRITICAL" else 0.5,
            timestamp=datetime.now(timezone.utc)
        )
        if self.db:
            self.db.add(event)
            self.db.commit()
            self.db.refresh(event)
        else:
            self._security_events.append(event)
        return event

    def log_audit(
        self,
        tenant_id: str,
        actor_id: str,
        actor_type: str,
        action: str,
        target_resource: str,
        query_text: Optional[str] = None,
        purpose: Optional[str] = None,
        result_status: str = "SUCCESS",
        metadata_context: Optional[Dict[str, Any]] = None
    ) -> DataAuditEventModel:
        audit = DataAuditEventModel(
            id=f"audit_{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            target_resource=target_resource,
            query_text=query_text,
            purpose=purpose,
            result_status=result_status,
            metadata_context=metadata_context or {},
            timestamp=datetime.now(timezone.utc)
        )
        if self.db:
            self.db.add(audit)
            self.db.commit()
            self.db.refresh(audit)
        else:
            self._audit_events.append(audit)
        return audit

    def list_security_events(self, tenant_id: str, severity: Optional[str] = None) -> List[DataSecurityEventModel]:
        if self.db:
            query = self.db.query(DataSecurityEventModel).filter(DataSecurityEventModel.tenant_id == tenant_id)
            if severity:
                query = query.filter(DataSecurityEventModel.severity == severity)
            return query.order_by(DataSecurityEventModel.created_at.desc()).all()
        return [e for e in self._security_events if e.tenant_id == tenant_id and (severity is None or e.severity == severity)]

    def list_audit_events(self, tenant_id: str, limit: int = 100) -> List[DataAuditEventModel]:
        if self.db:
            return self.db.query(DataAuditEventModel).filter(
                DataAuditEventModel.tenant_id == tenant_id
            ).order_by(DataAuditEventModel.timestamp.desc()).limit(limit).all()
        return [e for e in self._audit_events if e.tenant_id == tenant_id][:limit]
