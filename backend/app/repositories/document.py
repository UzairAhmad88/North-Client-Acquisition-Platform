"""Database repository for Phase 39 document and file management."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import desc, select, update, and_
from sqlalchemy.orm import Session

from app.models.document import (
    FileAccessLogRecord,
    FileMetadataRecord,
    FileRecord,
    FileScanRecord,
    FileVersionRecord,
    FolderRecord,
    ManagedDocumentRecord,
    ManagedDocumentVersionRecord,
    DocumentApprovalRecord,
    DocumentCommentRecord,
    DocumentExtractionRecord,
    DocumentLegalHoldRecord,
    DocumentReviewRecord,
    DocumentShareLinkRecord,
    DocumentShareRecord,
)


class DocumentRepository:
    """Database operations for Files, Managed Documents, Versions, Reviews, Approvals, and Shares."""

    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------------------------
    # Files
    # -------------------------------------------------------------------------
    def create_file(
        self,
        tenant_id: str,
        workspace_id: str,
        name: str,
        extension: str,
        mime_type: str,
        size_bytes: int,
        checksum: str,
        storage_key: str,
        created_by: str,
        storage_provider: str = "LOCAL",
        classification: str = "GENERAL",
        sensitivity: str = "INTERNAL",
        visibility: str = "INTERNAL",
        folder_id: Optional[str] = None,
    ) -> FileRecord:
        record = FileRecord(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            folder_id=folder_id,
            name=name,
            extension=extension,
            mime_type=mime_type,
            size_bytes=size_bytes,
            checksum=checksum,
            storage_provider=storage_provider,
            storage_key=storage_key,
            classification=classification,
            sensitivity=sensitivity,
            visibility=visibility,
            created_by=created_by,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_file_by_id(self, tenant_id: str, file_id: str) -> Optional[FileRecord]:
        stmt = select(FileRecord).where(
            and_(
                FileRecord.tenant_id == tenant_id,
                FileRecord.id == file_id,
                FileRecord.is_deleted.is_(False),
            )
        )
        return self.db.scalars(stmt).first()

    def list_files(
        self,
        tenant_id: str,
        workspace_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        classification: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[FileRecord]:
        conditions = [FileRecord.tenant_id == tenant_id, FileRecord.is_deleted.is_(False)]
        if workspace_id:
            conditions.append(FileRecord.workspace_id == workspace_id)
        if folder_id:
            conditions.append(FileRecord.folder_id == folder_id)
        if classification:
            conditions.append(FileRecord.classification == classification)

        stmt = select(FileRecord).where(and_(*conditions)).order_by(desc(FileRecord.created_at)).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    # -------------------------------------------------------------------------
    # Managed Documents
    # -------------------------------------------------------------------------
    def create_managed_document(
        self,
        tenant_id: str,
        workspace_id: str,
        title: str,
        created_by: str,
        classification: str = "GENERAL",
        sensitivity: str = "INTERNAL",
        visibility: str = "INTERNAL",
        folder_id: Optional[str] = None,
    ) -> ManagedDocumentRecord:
        record = ManagedDocumentRecord(
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            folder_id=folder_id,
            title=title,
            classification=classification,
            sensitivity=sensitivity,
            visibility=visibility,
            created_by=created_by,
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_managed_document(self, tenant_id: str, document_id: str) -> Optional[ManagedDocumentRecord]:
        stmt = select(ManagedDocumentRecord).where(
            and_(
                ManagedDocumentRecord.tenant_id == tenant_id,
                ManagedDocumentRecord.id == document_id,
                ManagedDocumentRecord.is_deleted.is_(False),
            )
        )
        return self.db.scalars(stmt).first()

    def list_managed_documents(
        self,
        tenant_id: str,
        workspace_id: Optional[str] = None,
        classification: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[ManagedDocumentRecord]:
        conditions = [ManagedDocumentRecord.tenant_id == tenant_id, ManagedDocumentRecord.is_deleted.is_(False)]
        if workspace_id:
            conditions.append(ManagedDocumentRecord.workspace_id == workspace_id)
        if classification:
            conditions.append(ManagedDocumentRecord.classification == classification)
        if status:
            conditions.append(ManagedDocumentRecord.status == status)

        stmt = (
            select(ManagedDocumentRecord)
            .where(and_(*conditions))
            .order_by(desc(ManagedDocumentRecord.created_at))
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    # -------------------------------------------------------------------------
    # Versions & Approvals
    # -------------------------------------------------------------------------
    def add_document_version(
        self,
        document_id: str,
        version_number: int,
        checksum: str,
        created_by: str,
        file_id: Optional[str] = None,
        storage_key: Optional[str] = None,
        change_summary: Optional[str] = None,
    ) -> ManagedDocumentVersionRecord:
        version = ManagedDocumentVersionRecord(
            document_id=document_id,
            version_number=version_number,
            file_id=file_id,
            checksum=checksum,
            storage_key=storage_key,
            change_summary=change_summary,
            created_by=created_by,
        )
        self.db.add(version)
        self.db.flush()
        return version

    def record_document_approval(
        self,
        document_id: str,
        version_id: str,
        version_number: int,
        checksum: str,
        approver_id: str,
        approver_role: str,
        decision: str = "APPROVED",
        decision_notes: Optional[str] = None,
    ) -> DocumentApprovalRecord:
        approval = DocumentApprovalRecord(
            document_id=document_id,
            version_id=version_id,
            version_number=version_number,
            checksum=checksum,
            approver_id=approver_id,
            approver_role=approver_role,
            decision=decision,
            decision_notes=decision_notes,
            approved_at=datetime.now(timezone.utc),
        )
        self.db.add(approval)
        self.db.flush()
        return approval

    # -------------------------------------------------------------------------
    # Share Links
    # -------------------------------------------------------------------------
    def create_share_link(
        self,
        tenant_id: str,
        document_id: str,
        token: str,
        permissions_json: List[str],
        expires_at: datetime,
        created_by: str,
        has_passcode: bool = False,
        passcode_hash: Optional[str] = None,
    ) -> DocumentShareLinkRecord:
        link = DocumentShareLinkRecord(
            tenant_id=tenant_id,
            document_id=document_id,
            token=token,
            permissions_json=permissions_json,
            expires_at=expires_at,
            created_by=created_by,
            has_passcode=has_passcode,
            passcode_hash=passcode_hash,
        )
        self.db.add(link)
        self.db.flush()
        return link

    def get_share_link_by_token(self, token: str) -> Optional[DocumentShareLinkRecord]:
        stmt = select(DocumentShareLinkRecord).where(DocumentShareLinkRecord.token == token)
        return self.db.scalars(stmt).first()
