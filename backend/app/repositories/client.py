"""Repository layer for Client Collaboration, Communication & Delivery Workspace."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import select, update, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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


class ClientRepository:
    """Repository handling client workspace entities and visibility filtering."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_client_account(self, account: ClientAccount) -> ClientAccount:
        self.db.add(account)
        await self.db.flush()
        await self.db.refresh(account)
        return account

    async def get_client_account_by_id(self, account_id: uuid.UUID) -> Optional[ClientAccount]:
        stmt = (
            select(ClientAccount)
            .where(ClientAccount.id == account_id)
            .options(
                selectinload(ClientAccount.members),
                selectinload(ClientAccount.project_accesses),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_client_member(self, member: ClientMember) -> ClientMember:
        self.db.add(member)
        await self.db.flush()
        await self.db.refresh(member)
        return member

    async def get_client_member(self, account_id: uuid.UUID, user_id: uuid.UUID) -> Optional[ClientMember]:
        stmt = select(ClientMember).where(
            ClientMember.client_account_id == account_id, ClientMember.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_invitation(self, invitation: ClientInvitation) -> ClientInvitation:
        self.db.add(invitation)
        await self.db.flush()
        await self.db.refresh(invitation)
        return invitation

    async def get_invitation_by_token_hash(self, token_hash: str) -> Optional[ClientInvitation]:
        stmt = select(ClientInvitation).where(ClientInvitation.token_hash == token_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def grant_project_access(self, access: ClientProjectAccess) -> ClientProjectAccess:
        self.db.add(access)
        await self.db.flush()
        await self.db.refresh(access)
        return access

    async def check_project_access(self, account_id: uuid.UUID, project_id: uuid.UUID) -> bool:
        stmt = select(ClientProjectAccess).where(
            ClientProjectAccess.client_account_id == account_id,
            ClientProjectAccess.project_id == project_id,
            ClientProjectAccess.status == "ACTIVE",
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def create_thread(self, thread: DiscussionThread) -> DiscussionThread:
        self.db.add(thread)
        await self.db.flush()
        await self.db.refresh(thread)
        return thread

    async def list_project_threads(
        self, project_id: uuid.UUID, is_client_view: bool = True
    ) -> List[DiscussionThread]:
        query = select(DiscussionThread).where(DiscussionThread.project_id == project_id)
        if is_client_view:
            query = query.where(DiscussionThread.visibility == "CLIENT_VISIBLE")
        query = query.options(selectinload(DiscussionThread.messages)).order_by(DiscussionThread.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_message(self, message: ThreadMessage) -> ThreadMessage:
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def create_question(self, question: ClientQuestion) -> ClientQuestion:
        self.db.add(question)
        await self.db.flush()
        await self.db.refresh(question)
        return question

    async def list_project_questions(self, project_id: uuid.UUID) -> List[ClientQuestion]:
        stmt = select(ClientQuestion).where(ClientQuestion.project_id == project_id).order_by(ClientQuestion.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_request(self, req: ClientRequest) -> ClientRequest:
        self.db.add(req)
        await self.db.flush()
        await self.db.refresh(req)
        return req

    async def list_project_requests(self, project_id: uuid.UUID) -> List[ClientRequest]:
        stmt = select(ClientRequest).where(ClientRequest.project_id == project_id).order_by(ClientRequest.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_feedback(self, fb: ClientFeedback) -> ClientFeedback:
        self.db.add(fb)
        await self.db.flush()
        await self.db.refresh(fb)
        return fb

    async def create_deliverable_review(self, review: DeliverableReview) -> DeliverableReview:
        self.db.add(review)
        await self.db.flush()
        await self.db.refresh(review)
        return review

    async def create_deliverable_approval(self, approval: DeliverableApproval) -> DeliverableApproval:
        self.db.add(approval)
        await self.db.flush()
        await self.db.refresh(approval)
        return approval

    async def create_project_file(self, file_asset: ProjectFile) -> ProjectFile:
        self.db.add(file_asset)
        await self.db.flush()
        await self.db.refresh(file_asset)
        return file_asset

    async def list_project_files(self, project_id: uuid.UUID, is_client_view: bool = True) -> List[ProjectFile]:
        query = select(ProjectFile).where(ProjectFile.project_id == project_id)
        if is_client_view:
            query = query.where(ProjectFile.visibility == "CLIENT_VISIBLE")
        query = query.order_by(ProjectFile.created_at.desc())
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create_action_item(self, item: ClientActionItem) -> ClientActionItem:
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item)
        return item

    async def list_client_action_items(self, project_id: uuid.UUID) -> List[ClientActionItem]:
        stmt = select(ClientActionItem).where(ClientActionItem.project_id == project_id).order_by(ClientActionItem.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_announcement(self, ann: ProjectAnnouncement) -> ProjectAnnouncement:
        self.db.add(ann)
        await self.db.flush()
        await self.db.refresh(ann)
        return ann

    async def list_announcements(self, project_id: uuid.UUID) -> List[ProjectAnnouncement]:
        stmt = select(ProjectAnnouncement).where(ProjectAnnouncement.project_id == project_id).order_by(ProjectAnnouncement.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_client_activity(self, act: ClientActivity) -> ClientActivity:
        self.db.add(act)
        await self.db.flush()
        await self.db.refresh(act)
        return act

    async def list_client_activity(self, project_id: uuid.UUID) -> List[ClientActivity]:
        stmt = select(ClientActivity).where(
            ClientActivity.project_id == project_id, ClientActivity.visibility == "CLIENT_VISIBLE"
        ).order_by(ClientActivity.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
