"""FastAPI endpoints for Unified File Management, Upload, Preview, and Download."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.documents.base import DocumentClassification, DocumentVisibility, SensitivityLevel, SharePermission
from app.documents.service import DocumentPlatformService
from app.models.user import User
from app.repositories.document import DocumentRepository
from app.schemas.document import FileResponseSchema, FileUploadResponseSchema

router = APIRouter(prefix="/files", tags=["Files & Storage"])
_doc_service = DocumentPlatformService()


@router.post("/upload", response_model=FileUploadResponseSchema, summary="Upload a binary file")
async def upload_file(
    file: UploadFile = File(...),
    workspace_id: str = Form("default_workspace"),
    classification: str = Form("GENERAL"),
    sensitivity: str = Form("INTERNAL"),
    visibility: str = Form("INTERNAL"),
    folder_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Upload a file through validation, malware scan, storage, preview, and extraction pipeline."""
    content = await file.read()
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    try:
        class_enum = DocumentClassification(classification.upper())
    except ValueError:
        class_enum = DocumentClassification.GENERAL

    try:
        sens_enum = SensitivityLevel(sensitivity.upper())
    except ValueError:
        sens_enum = SensitivityLevel.INTERNAL

    try:
        vis_enum = DocumentVisibility(visibility.upper())
    except ValueError:
        vis_enum = DocumentVisibility.INTERNAL

    result = _doc_service.process_file_upload(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        user_id=user_id,
        filename=file.filename or "uploaded_file",
        data=content,
        declared_mime_type=file.content_type,
        classification=class_enum,
        sensitivity=sens_enum,
        visibility=vis_enum,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"errors": result.get("validation_errors"), "threat": result.get("threat_name")},
        )

    # Persist in DB
    repo = DocumentRepository(db)
    file_record = repo.create_file(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        name=result["filename"],
        extension=result.get("detected_extension", ""),
        mime_type=result["mime_type"],
        size_bytes=result["size_bytes"],
        checksum=result["checksum_sha256"],
        storage_key=result["storage_key"],
        created_by=user_id,
        classification=result["classification"],
        sensitivity=result["sensitivity"],
        visibility=result["visibility"],
        folder_id=folder_id,
    )
    db.commit()

    return FileUploadResponseSchema(
        success=True,
        file_id=str(file_record.id),
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        filename=result["filename"],
        mime_type=result["mime_type"],
        size_bytes=result["size_bytes"],
        checksum_sha256=result["checksum_sha256"],
        storage_key=result["storage_key"],
        status=result["status"],
        classification=result["classification"],
        sensitivity=result["sensitivity"],
        visibility=result["visibility"],
        extracted_text=result.get("extracted_text"),
        chunks_count=result.get("chunks_count", 0),
        preview=result.get("preview"),
        validation_errors=[],
    )


@router.get("", response_model=List[FileResponseSchema], summary="List stored files")
def list_files(
    workspace_id: Optional[str] = Query(None),
    folder_id: Optional[str] = Query(None),
    classification: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_files(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        folder_id=folder_id,
        classification=classification,
        limit=limit,
        offset=offset,
    )


@router.get("/{id}", response_model=FileResponseSchema, summary="Get file metadata")
def get_file(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    record = repo.get_file_by_id(tenant_id=tenant_id, file_id=id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return record


@router.get("/{id}/download", summary="Download file binary")
def download_file(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    record = repo.get_file_by_id(tenant_id=tenant_id, file_id=id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    is_client = getattr(current_user, "is_client", False) or getattr(current_user, "role", "") == "client"
    can_read = _doc_service.authorizer.authorize_read(
        tenant_id=record.tenant_id,
        user_tenant_id=tenant_id,
        user_role=getattr(current_user, "role", "USER"),
        visibility=record.visibility,
        sensitivity=record.sensitivity,
        is_client_user=is_client,
    )
    if not can_read:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    data = _doc_service.storage.download(record.storage_key)
    return Response(
        content=data,
        media_type=record.mime_type,
        headers={"Content-Disposition": f'attachment; filename="{record.name}"'},
    )
