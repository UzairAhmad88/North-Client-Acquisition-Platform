"""FastAPI endpoints for Managed Documents, Reviews, Approvals, Shares, and AI Insights."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.documents.service import DocumentPlatformService
from app.models.user import User
from app.repositories.document import DocumentRepository
from app.schemas.document import (
    DocumentApprovalRequestSchema,
    DocumentCreateRequestSchema,
    DocumentReviewRequestSchema,
    ManagedDocumentResponseSchema,
    ShareLinkCreateRequestSchema,
    ShareLinkResponseSchema,
)

router = APIRouter(prefix="/documents", tags=["Documents & Lifecycles"])
_doc_service = DocumentPlatformService()


@router.post("", response_model=ManagedDocumentResponseSchema, summary="Create a managed document")
def create_document(
    payload: DocumentCreateRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    user_id = str(current_user.id)

    record = repo.create_managed_document(
        tenant_id=tenant_id,
        workspace_id=payload.workspace_id,
        title=payload.title,
        created_by=user_id,
        classification=payload.classification or "GENERAL",
        sensitivity=payload.sensitivity or "INTERNAL",
        visibility=payload.visibility or "INTERNAL",
        folder_id=payload.folder_id,
    )
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=List[ManagedDocumentResponseSchema], summary="List managed documents")
def list_documents(
    workspace_id: Optional[str] = Query(None),
    classification: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    return repo.list_managed_documents(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        classification=classification,
        status=status_filter,
        limit=limit,
        offset=offset,
    )


@router.get("/{id}", response_model=ManagedDocumentResponseSchema, summary="Get document details")
def get_document(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    record = repo.get_managed_document(tenant_id=tenant_id, document_id=id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return record


@router.post("/{id}/review", summary="Submit document for review")
def submit_for_review(
    id: str,
    payload: DocumentReviewRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    doc = repo.get_managed_document(tenant_id=tenant_id, document_id=id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    doc.status = "SUBMITTED_FOR_REVIEW"
    db.commit()
    return {"status": "SUBMITTED_FOR_REVIEW", "document_id": id}


@router.post("/{id}/approve", summary="Approve document version")
def approve_document(
    id: str,
    payload: DocumentApprovalRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    doc = repo.get_managed_document(tenant_id=tenant_id, document_id=id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    role = getattr(current_user, "role", "USER")
    is_client = getattr(current_user, "is_client", False) or role == "client"
    can_approve = _doc_service.authorizer.authorize_action(
        action=SharePermission.APPROVE,
        user_role=role,
        is_client_user=is_client,
    )
    if not can_approve:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Approver role required")

    approval = repo.record_document_approval(
        document_id=id,
        version_id=payload.version_id,
        version_number=payload.version_number,
        checksum=payload.checksum,
        approver_id=str(current_user.id),
        approver_role=role,
        decision="APPROVED",
        decision_notes=payload.decision_notes,
    )
    doc.status = "APPROVED"
    db.commit()
    return {"status": "APPROVED", "approval_id": str(approval.id)}


@router.post("/{id}/links", response_model=ShareLinkResponseSchema, summary="Generate secure expiring share link")
def create_share_link(
    id: str,
    payload: ShareLinkCreateRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    repo = DocumentRepository(db)
    tenant_id = str(current_user.tenant_id)
    doc = repo.get_managed_document(tenant_id=tenant_id, document_id=id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    link_data = _doc_service.share_manager.generate_secure_share_link(
        tenant_id=tenant_id,
        document_id=id,
        created_by=str(current_user.id),
        expires_in_hours=payload.expires_in_hours,
        allow_download=payload.allow_download,
        passcode=payload.passcode,
    )

    from datetime import datetime
    expires_dt = datetime.fromisoformat(link_data["expires_at"])

    link_record = repo.create_share_link(
        tenant_id=tenant_id,
        document_id=id,
        token=link_data["token"],
        permissions_json=link_data["permissions"],
        expires_at=expires_dt,
        created_by=str(current_user.id),
        has_passcode=link_data["has_passcode"],
    )
    db.commit()

    return ShareLinkResponseSchema(
        link_id=link_data["link_id"],
        token=link_data["token"],
        document_id=id,
        permissions=link_data["permissions"],
        expires_at=expires_dt,
        created_by=str(current_user.id),
        access_url=f"/documents/shared/{link_data['token']}",
    )
