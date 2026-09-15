"""Central Platform Document and File Service."""

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from integrations.security.file_scanner.base import BaseFileScanner
from integrations.security.file_scanner.models import ScanStatus
from integrations.security.file_scanner.providers.mock import MockFileScanner
from integrations.storage.base import BaseStorageProvider
from integrations.storage.service import StorageService

from app.documents.authorization import DocumentAuthorizer
from app.documents.base import (
    DocumentClassification,
    DocumentStatus,
    DocumentVisibility,
    ExtractedChunk,
    FileStatus,
    FileValidationResult,
    RetentionStatus,
    SensitivityLevel,
    SharePermission,
    ShareType,
    WorkspaceType,
)
from app.documents.extraction import DocumentExtractor, OCREngine
from app.documents.preview import PreviewGenerator
from app.documents.retention import DocumentRetentionManager
from app.documents.review import DocumentReviewEngine
from app.documents.sharing import DocumentShareManager
from app.documents.validator import FileValidator


class DocumentPlatformService:
    """Coordinating service for files, documents, digital assets, and lifecycles."""

    def __init__(
        self,
        storage_provider: Optional[BaseStorageProvider] = None,
        scanner_provider: Optional[BaseFileScanner] = None,
    ) -> None:
        self.storage = storage_provider or StorageService.get_instance().provider
        self.scanner = scanner_provider or MockFileScanner()
        self.validator = FileValidator()
        self.extractor = DocumentExtractor()
        self.ocr_engine = OCREngine()
        self.preview_gen = PreviewGenerator()
        self.authorizer = DocumentAuthorizer()
        self.review_engine = DocumentReviewEngine()
        self.share_manager = DocumentShareManager()
        self.retention_manager = DocumentRetentionManager()

    def process_file_upload(
        self,
        tenant_id: str,
        workspace_id: str,
        user_id: str,
        filename: str,
        data: bytes,
        declared_mime_type: Optional[str] = None,
        classification: DocumentClassification = DocumentClassification.GENERAL,
        sensitivity: SensitivityLevel = SensitivityLevel.INTERNAL,
        visibility: DocumentVisibility = DocumentVisibility.INTERNAL,
    ) -> Dict[str, Any]:
        """Full pipeline: validate -> malware scan -> store -> extract -> preview."""
        # 1. Validation
        validation: FileValidationResult = self.validator.validate_file_content(
            filename=filename, data=data, declared_mime_type=declared_mime_type
        )
        if not validation.is_valid:
            return {
                "success": False,
                "status": FileStatus.BLOCKED.value,
                "validation_errors": validation.validation_errors,
                "checksum_sha256": validation.checksum_sha256,
            }

        # 2. Malware Scan
        scan_result = self.scanner.scan_bytes(data, filename=filename)
        if scan_result.status != ScanStatus.CLEAN:
            return {
                "success": False,
                "status": FileStatus.QUARANTINED.value,
                "threat_name": scan_result.threat_name,
                "validation_errors": [f"Security scan detected threat: {scan_result.threat_name}"],
                "checksum_sha256": validation.checksum_sha256,
            }

        # 3. Storage
        file_id = str(uuid4())
        storage_key = f"tenants/{tenant_id}/workspaces/{workspace_id}/{file_id}/{filename}"
        storage_meta = self.storage.upload(
            storage_key=storage_key,
            data=data,
            content_type=validation.mime_type,
            metadata={"tenant_id": tenant_id, "uploaded_by": user_id, "filename": filename},
        )

        # 4. Text Extraction & Chunking
        extracted_text, chunks = self.extractor.extract_text(
            filename=filename, data=data, mime_type=validation.mime_type
        )

        # 5. Preview Generation
        preview = self.preview_gen.generate_preview_payload(
            filename=filename, mime_type=validation.mime_type, data=data, extracted_text=extracted_text
        )

        return {
            "success": True,
            "file_id": file_id,
            "tenant_id": tenant_id,
            "workspace_id": workspace_id,
            "filename": filename,
            "mime_type": validation.mime_type,
            "size_bytes": validation.size_bytes,
            "checksum_sha256": validation.checksum_sha256,
            "storage_key": storage_key,
            "status": FileStatus.AVAILABLE.value,
            "classification": classification.value,
            "sensitivity": sensitivity.value,
            "visibility": visibility.value,
            "extracted_text": extracted_text,
            "chunks_count": len(chunks),
            "preview": preview,
            "uploaded_by": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def create_document_with_version(
        self,
        tenant_id: str,
        workspace_id: str,
        user_id: str,
        title: str,
        file_payload: Dict[str, Any],
        classification: DocumentClassification = DocumentClassification.GENERAL,
        sensitivity: SensitivityLevel = SensitivityLevel.INTERNAL,
        visibility: DocumentVisibility = DocumentVisibility.INTERNAL,
        change_summary: str = "Initial document version",
    ) -> Dict[str, Any]:
        """Create a managed document entity pointing to an initial file version."""
        document_id = str(uuid4())
        version_id = str(uuid4())

        doc = {
            "document_id": document_id,
            "tenant_id": tenant_id,
            "workspace_id": workspace_id,
            "title": title,
            "current_version_id": version_id,
            "current_version_number": 1,
            "status": DocumentStatus.DRAFT.value,
            "classification": classification.value,
            "sensitivity": sensitivity.value,
            "visibility": visibility.value,
            "retention_status": RetentionStatus.ACTIVE.value,
            "legal_hold": False,
            "created_by": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "versions": [
                {
                    "version_id": version_id,
                    "version_number": 1,
                    "file_id": file_payload.get("file_id"),
                    "filename": file_payload.get("filename"),
                    "checksum_sha256": file_payload.get("checksum_sha256"),
                    "storage_key": file_payload.get("storage_key"),
                    "change_summary": change_summary,
                    "status": DocumentStatus.DRAFT.value,
                    "created_by": user_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            ],
        }
        return doc

    def create_new_version(
        self,
        document: Dict[str, Any],
        user_id: str,
        new_file_payload: Dict[str, Any],
        change_summary: str,
    ) -> Dict[str, Any]:
        """Add a new version to an existing document. Any prior approval remains locked to previous version."""
        latest_version = document["current_version_number"]
        new_version_num = latest_version + 1
        new_version_id = str(uuid4())

        new_version_record = {
            "version_id": new_version_id,
            "version_number": new_version_num,
            "file_id": new_file_payload.get("file_id"),
            "filename": new_file_payload.get("filename"),
            "checksum_sha256": new_file_payload.get("checksum_sha256"),
            "storage_key": new_file_payload.get("storage_key"),
            "change_summary": change_summary,
            "status": DocumentStatus.DRAFT.value,  # Draft state; does not inherit approval
            "created_by": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        updated_doc = dict(document)
        updated_doc["current_version_id"] = new_version_id
        updated_doc["current_version_number"] = new_version_num
        updated_doc["status"] = DocumentStatus.DRAFT.value
        updated_doc["versions"] = list(document.get("versions", [])) + [new_version_record]
        updated_doc["updated_at"] = datetime.now(timezone.utc).isoformat()
        return updated_doc
