"""
SQLAlchemy Async Repository for Phase 47 GRC Models.
"""

from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.grc import (
    GovernanceAttestationModel,
    GovernanceAuditModel,
    GovernanceControlModel,
    GovernanceEvidenceModel,
    GovernanceExceptionModel,
    GovernanceFindingModel,
    GovernanceFrameworkModel,
    GovernancePostureSnapshotModel,
    GovernanceRequirementModel,
    GovernanceRiskModel,
    PrivacyProcessingActivityModel,
    PrivacyRequestModel,
    VendorProfileModel,
)


class GRCRepository:
    """Persistence repository for governance, risk, compliance and privacy models."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_frameworks(self, tenant_id: str = "default_tenant") -> List[GovernanceFrameworkModel]:
        stmt = select(GovernanceFrameworkModel).where(GovernanceFrameworkModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_framework(self, framework_code: str, tenant_id: str = "default_tenant") -> Optional[GovernanceFrameworkModel]:
        stmt = select(GovernanceFrameworkModel).where(
            GovernanceFrameworkModel.framework_code == framework_code,
            GovernanceFrameworkModel.tenant_id == tenant_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_controls(self, tenant_id: str = "default_tenant") -> List[GovernanceControlModel]:
        stmt = select(GovernanceControlModel).where(GovernanceControlModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_control(self, control_code: str, tenant_id: str = "default_tenant") -> Optional[GovernanceControlModel]:
        stmt = select(GovernanceControlModel).where(
            GovernanceControlModel.control_code == control_code,
            GovernanceControlModel.tenant_id == tenant_id
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_risks(self, tenant_id: str = "default_tenant") -> List[GovernanceRiskModel]:
        stmt = select(GovernanceRiskModel).where(GovernanceRiskModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_findings(self, tenant_id: str = "default_tenant") -> List[GovernanceFindingModel]:
        stmt = select(GovernanceFindingModel).where(GovernanceFindingModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_exceptions(self, tenant_id: str = "default_tenant") -> List[GovernanceExceptionModel]:
        stmt = select(GovernanceExceptionModel).where(GovernanceExceptionModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_evidence(self, tenant_id: str = "default_tenant") -> List[GovernanceEvidenceModel]:
        stmt = select(GovernanceEvidenceModel).where(GovernanceEvidenceModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_privacy_requests(self, tenant_id: str = "default_tenant") -> List[PrivacyRequestModel]:
        stmt = select(PrivacyRequestModel).where(PrivacyRequestModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def list_vendors(self, tenant_id: str = "default_tenant") -> List[VendorProfileModel]:
        stmt = select(VendorProfileModel).where(VendorProfileModel.tenant_id == tenant_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
