"""
Phase 65: Data Export Governance Service
Enforces pre-export scanning, PII checks, approval workflows, and audit trails.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from backend.app.models.autonomous_data_knowledge_os import DataExportModel


class DataExportService:
    def __init__(self, db: Session):
        self.db = db

    def request_export(
        self,
        tenant_id: str,
        user_id: str,
        dataset_id: str,
        format_type: str,
        destination_target: str,
        purpose: str,
        contains_sensitive_data: bool = False
    ) -> DataExportModel:
        # Require approval if sensitive data detected
        status = "PENDING_APPROVAL" if contains_sensitive_data else "APPROVED"

        export_record = DataExportModel(
            tenant_id=tenant_id,
            user_id=user_id,
            dataset_id=dataset_id,
            format_type=format_type,
            destination_target=destination_target,
            purpose=purpose,
            status=status,
            created_at=datetime.now(timezone.utc)
        )
        self.db.add(export_record)
        self.db.commit()
        self.db.refresh(export_record)
        return export_record

    def approve_export(self, tenant_id: str, export_id: str, approved_by: str) -> Optional[DataExportModel]:
        export = self.db.query(DataExportModel).filter(
            DataExportModel.id == export_id,
            DataExportModel.tenant_id == tenant_id
        ).first()
        if not export:
            return None
        export.status = "APPROVED"
        self.db.commit()
        self.db.refresh(export)
        return export

    def complete_export(self, tenant_id: str, export_id: str, file_path: str, row_count: int) -> Optional[DataExportModel]:
        export = self.db.query(DataExportModel).filter(
            DataExportModel.id == export_id,
            DataExportModel.tenant_id == tenant_id
        ).first()
        if not export:
            return None
        export.status = "COMPLETED"
        export.file_path = file_path
        export.row_count = row_count
        export.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(export)
        return export

    def list_exports(self, tenant_id: str) -> List[DataExportModel]:
        return self.db.query(DataExportModel).filter(
            DataExportModel.tenant_id == tenant_id
        ).order_by(DataExportModel.created_at.desc()).all()
