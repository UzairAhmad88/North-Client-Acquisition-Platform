"""Service layer for Client Collaboration, Communication & Delivery Workspace."""

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import (
    ClientAccount,
    ClientActionItem,
    ClientActivity,
    ClientFeedback,
    ClientInvitation,
    ClientMember,
    ClientProjectAccess,
    ClientQuestion,
    ClientRequest,
    DeliverableApproval,
    DeliverableReview,
    DiscussionThread,
    ProjectAnnouncement,
    ProjectFile,
    ThreadMessage,
)
from app.models.project import Project, ProjectDeliverable
from app.models.user import User
from app.repositories.client import ClientRepository
from app.repositories.project import ProjectRepository


ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/svg+xml",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/csv",
    "application/json",
}

MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB limit


class ClientService:
    """Service layer managing client onboarding, deliverable approvals, file safety, and visibility policy."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ClientRepository(db)
        self.project_repo = ProjectRepository(db)

    async def create_client_account(self, business_id: uuid.UUID, name: str) -> ClientAccount:
        account = ClientAccount(business_id=business_id, name=name, status="ACTIVE")
        return await self.repo.create_client_account(account)

    async def generate_invitation(
        self, client_account_id: uuid.UUID, email: str, role: str, created_by_id: uuid.UUID
    ) -> Tuple[ClientInvitation, str]:
        """Generate secure single-use invitation token with 48-hour expiration."""
        raw_token = f"inv-{uuid.uuid4().hex}"
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(hours=48)

        invitation = ClientInvitation(
            client_account_id=client_account_id,
            email=email.lower().strip(),
            role=role,
            token_hash=token_hash,
            expires_at=expires_at,
            is_used=False,
            created_by_id=created_by_id,
        )

        invitation = await self.repo.create_invitation(invitation)
        return invitation, raw_token

    async def accept_invitation(self, raw_token: str, user: User) -> ClientMember:
        """Accept single-use invitation token and link user as ClientMember."""
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        invitation = await self.repo.get_invitation_by_token_hash(token_hash)

        if not invitation or invitation.is_used:
            raise ValueError("Invitation token is invalid or has already been used.")

        if invitation.expires_at < datetime.now(timezone.utc):
            raise ValueError("Invitation token has expired.")

        invitation.is_used = True
        await self.db.flush()

        member = ClientMember(
            client_account_id=invitation.client_account_id,
            user_id=user.id,
            role=invitation.role,
            status="ACTIVE",
            joined_at=datetime.now(timezone.utc),
        )

        return await self.repo.create_client_member(member)

    async def grant_project_access(self, client_account_id: uuid.UUID, project_id: uuid.UUID) -> ClientProjectAccess:
        access = ClientProjectAccess(
            client_account_id=client_account_id,
            project_id=project_id,
            access_level="COLLABORATE",
            status="ACTIVE",
        )
        return await self.repo.grant_project_access(access)

    async def create_thread(
        self,
        project_id: uuid.UUID,
        title: str,
        thread_type: str = "GENERAL",
        visibility: str = "CLIENT_VISIBLE",
        created_by_id: uuid.UUID = None,
        deliverable_id: Optional[uuid.UUID] = None,
    ) -> DiscussionThread:
        thread = DiscussionThread(
            project_id=project_id,
            deliverable_id=deliverable_id,
            type=thread_type,
            title=title,
            status="OPEN",
            visibility=visibility,
            created_by_id=created_by_id,
        )
        return await self.repo.create_thread(thread)

    async def post_message(
        self,
        thread_id: uuid.UUID,
        sender_id: uuid.UUID,
        sender_type: str,
        content: str,
        visibility: str = "CLIENT_VISIBLE",
        attachments: List[Dict[str, Any]] = None,
    ) -> ThreadMessage:
        msg = ThreadMessage(
            thread_id=thread_id,
            sender_id=sender_id,
            sender_type=sender_type,
            content=content,
            visibility=visibility,
            attachments=attachments or [],
        )
        return await self.repo.create_message(msg)

    async def approve_deliverable(
        self,
        deliverable_id: uuid.UUID,
        version_number: int,
        approval_statement: str,
        signer_name: str,
        signer_email: str,
        ip_address: str,
        user_agent: str,
        content_payload: str,
    ) -> DeliverableApproval:
        """Record explicit client deliverable approval with SHA-256 content verification."""
        deliverable = await self.db.get(ProjectDeliverable, deliverable_id)
        if not deliverable:
            raise ValueError(f"Deliverable '{deliverable_id}' not found.")

        content_hash = hashlib.sha256(content_payload.encode("utf-8")).hexdigest()

        approval = DeliverableApproval(
            deliverable_id=deliverable_id,
            version_number=version_number,
            content_hash=content_hash,
            approval_statement=approval_statement,
            signer_name=signer_name,
            signer_email=signer_email,
            ip_address=ip_address,
            user_agent=user_agent,
            approved_at=datetime.now(timezone.utc),
        )

        approval = await self.repo.create_deliverable_approval(approval)
        deliverable.status = "ACCEPTED"
        await self.db.flush()

        # Log client activity
        act = ClientActivity(
            project_id=deliverable.project_id,
            event_type="DELIVERABLE_APPROVED",
            description=f"Client approved deliverable '{deliverable.name}' (Version {version_number}).",
            actor_id=deliverable.project_id,  # System reference
            visibility="CLIENT_VISIBLE",
        )
        await self.repo.create_client_activity(act)

        return approval

    async def upload_file(
        self,
        project_id: uuid.UUID,
        uploaded_by_id: uuid.UUID,
        filename: str,
        mime_type: str,
        file_bytes: bytes,
        visibility: str = "INTERNAL_ONLY",
    ) -> ProjectFile:
        """Validate and store project file asset."""
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValueError(f"File type '{mime_type}' is not in the security allowlist.")

        if len(file_bytes) > MAX_FILE_SIZE_BYTES:
            raise ValueError("File size exceeds maximum allowed limit (25 MB).")

        content_hash = hashlib.sha256(file_bytes).hexdigest()
        storage_key = f"files/{project_id}/{content_hash[:16]}_{filename}"

        file_asset = ProjectFile(
            project_id=project_id,
            uploaded_by_id=uploaded_by_id,
            filename=filename,
            storage_key=storage_key,
            mime_type=mime_type,
            size_bytes=len(file_bytes),
            content_hash=content_hash,
            visibility=visibility,
            status="READY",
        )

        return await self.repo.create_project_file(file_asset)

    async def publish_file_to_client(self, file_id: uuid.UUID) -> ProjectFile:
        """Explicitly make an internal project file visible to the client."""
        file_asset = await self.db.get(ProjectFile, file_id)
        if not file_asset:
            raise ValueError(f"Project file '{file_id}' not found.")

        file_asset.visibility = "CLIENT_VISIBLE"
        await self.db.flush()
        return file_asset
