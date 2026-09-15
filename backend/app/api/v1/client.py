"""REST API Endpoints for Client Collaboration, Communication & Delivery Workspace."""

import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.client import (
    ClientActionItemCreateSchema,
    ClientFeedbackCreateSchema,
    ClientRequestCreateSchema,
    DeliverableApprovalResponseSchema,
    DeliverableApprovalSchema,
    InvitationAcceptSchema,
    InvitationCreateSchema,
    MessageCreateSchema,
    MessageResponseSchema,
    ProjectFileResponseSchema,
    ThreadCreateSchema,
    ThreadResponseSchema,
)
from app.services.client import ClientService
from agents.client_collaboration.agent import ClientCollaborationAgent
from agents.core.context import AgentContext

router = APIRouter(prefix="/client", tags=["Client Collaboration"])


@router.post("/invitations", status_code=status.HTTP_201_CREATED)
async def create_invitation(
    payload: InvitationCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate secure single-use invitation token for client user."""
    service = ClientService(db)
    invitation, raw_token = await service.generate_invitation(
        client_account_id=payload.client_account_id,
        email=payload.email,
        role=payload.role,
        created_by_id=current_user.id,
    )
    return {"status": "SUCCESS", "invitation_id": invitation.id, "raw_token": raw_token, "expires_at": invitation.expires_at}


@router.post("/invitations/accept")
async def accept_invitation(
    payload: InvitationAcceptSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Accept invitation token and link active user as client member."""
    service = ClientService(db)
    try:
        member = await service.accept_invitation(payload.raw_token, current_user)
        return {"status": "SUCCESS", "client_member_id": member.id, "role": member.role}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/threads", response_model=List[ThreadResponseSchema])
async def list_threads(
    project_id: uuid.UUID,
    is_client_view: bool = Query(True, description="Filter for client-visible threads"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List discussion threads for project workspace."""
    service = ClientService(db)
    threads = await service.repo.list_project_threads(project_id, is_client_view=is_client_view)
    return threads


@router.post("/projects/{project_id}/threads", response_model=ThreadResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_thread(
    project_id: uuid.UUID,
    payload: ThreadCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new discussion thread."""
    service = ClientService(db)
    thread = await service.create_thread(
        project_id=project_id,
        title=payload.title,
        thread_type=payload.thread_type,
        visibility=payload.visibility,
        created_by_id=current_user.id,
        deliverable_id=payload.deliverable_id,
    )
    return thread


@router.post("/threads/{thread_id}/messages", response_model=MessageResponseSchema, status_code=status.HTTP_201_CREATED)
async def post_message(
    thread_id: uuid.UUID,
    payload: MessageCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Post message to discussion thread."""
    service = ClientService(db)
    message = await service.post_message(
        thread_id=thread_id,
        sender_id=current_user.id,
        sender_type="CLIENT",
        content=payload.content,
        visibility=payload.visibility,
        attachments=payload.attachments,
    )
    return message


@router.post("/deliverables/{deliverable_id}/approve", response_model=DeliverableApprovalResponseSchema)
async def approve_deliverable(
    deliverable_id: uuid.UUID,
    payload: DeliverableApprovalSchema,
    user_agent: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Explicitly record formal client deliverable approval with SHA-256 content verification."""
    service = ClientService(db)
    try:
        approval = await service.approve_deliverable(
            deliverable_id=deliverable_id,
            version_number=payload.version_number,
            approval_statement=payload.approval_statement,
            signer_name=current_user.contact_name if hasattr(current_user, "contact_name") else current_user.email,
            signer_email=current_user.email,
            ip_address="127.0.0.1",
            user_agent=user_agent or "Unknown Browser",
            content_payload=payload.content_payload,
        )
        return approval
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/files", response_model=List[ProjectFileResponseSchema])
async def list_project_files(
    project_id: uuid.UUID,
    is_client_view: bool = Query(True, description="Filter for client-visible files"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List project files."""
    service = ClientService(db)
    files = await service.repo.list_project_files(project_id, is_client_view=is_client_view)
    return files


@router.post("/projects/{project_id}/run-agent")
async def run_client_collaboration_agent(
    project_id: uuid.UUID,
    action: str = Query("CLASSIFY_REQUEST", description="Action: CLASSIFY_REQUEST, SUMMARIZE_FEEDBACK, EXTRACT_ACTIONS, EVALUATE_SCOPE"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Trigger Client Collaboration AI Assistant analysis."""
    agent = ClientCollaborationAgent()
    context = AgentContext(
        workflow_id="wf_client_collaboration",
        task_id="t_client_collaboration",
        agent_run_id=str(uuid.uuid4()),
        metadata={
            "action": action,
            "project_id": str(project_id),
            "title": "Client Feature Request",
            "description": "Can we also add a custom mobile app for iOS?",
        },
    )

    res = await agent.execute(context)
    return res
