"""Repository layer for Phase 28 — Change Request, Scope Change & Commercial Change Management."""

from typing import Any, Dict, List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.change import (
    ChangeApproval,
    ChangeBaselineLink,
    ChangeCommercial,
    ChangeEstimate,
    ChangeEvidence,
    ChangeEvent,
    ChangeImpact,
    ChangeRequest,
    ChangeRequestVersion,
)


class ChangeRepository:
    """Database persistence operations for Change Requests, Versions, Impacts, and Approvals."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, change_id: str) -> Optional[ChangeRequest]:
        stmt = (
            select(ChangeRequest)
            .where(ChangeRequest.id == change_id)
            .options(
                selectinload(ChangeRequest.versions).selectinload(ChangeRequestVersion.impacts),
                selectinload(ChangeRequest.versions).selectinload(ChangeRequestVersion.estimates),
                selectinload(ChangeRequest.versions).selectinload(ChangeRequestVersion.commercials),
                selectinload(ChangeRequest.versions).selectinload(ChangeRequestVersion.approvals),
                selectinload(ChangeRequest.evidences),
                selectinload(ChangeRequest.events),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_number(self, change_number: str) -> Optional[ChangeRequest]:
        stmt = select(ChangeRequest).where(ChangeRequest.change_number == change_number)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_by_project(self, project_id: str) -> List[ChangeRequest]:
        stmt = (
            select(ChangeRequest)
            .where(ChangeRequest.project_id == project_id)
            .options(
                selectinload(ChangeRequest.versions),
                selectinload(ChangeRequest.events),
            )
            .order_by(ChangeRequest.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def generate_next_change_number(self, project_id: str) -> str:
        stmt = select(func.count(ChangeRequest.id)).where(ChangeRequest.project_id == project_id)
        res = await self.session.execute(stmt)
        count = res.scalar() or 0
        return f"CR-{(count + 1):04d}"

    async def create_change_request(self, change_req: ChangeRequest) -> ChangeRequest:
        self.session.add(change_req)
        await self.session.commit()
        await self.session.refresh(change_req)
        return change_req

    async def create_version(self, version: ChangeRequestVersion) -> ChangeRequestVersion:
        self.session.add(version)
        await self.session.commit()
        await self.session.refresh(version)
        return version

    async def add_evidence(self, evidence: ChangeEvidence) -> ChangeEvidence:
        self.session.add(evidence)
        await self.session.commit()
        return evidence

    async def add_impact(self, impact: ChangeImpact) -> ChangeImpact:
        self.session.add(impact)
        await self.session.commit()
        return impact

    async def add_estimate(self, estimate: ChangeEstimate) -> ChangeEstimate:
        self.session.add(estimate)
        await self.session.commit()
        return estimate

    async def add_commercial(self, commercial: ChangeCommercial) -> ChangeCommercial:
        self.session.add(commercial)
        await self.session.commit()
        return commercial

    async def add_approval(self, approval: ChangeApproval) -> ChangeApproval:
        self.session.add(approval)
        await self.session.commit()
        return approval

    async def record_event(self, event: ChangeEvent) -> ChangeEvent:
        self.session.add(event)
        await self.session.commit()
        return event

    async def save_baseline_link(self, link: ChangeBaselineLink) -> ChangeBaselineLink:
        self.session.add(link)
        await self.session.commit()
        return link

    async def update(self, change_req: ChangeRequest) -> ChangeRequest:
        await self.session.commit()
        await self.session.refresh(change_req)
        return change_req
