"""Repository layer for Platform Administration, Configurations, Policies and Controls."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.administration import (
    AdminFeatureFlagModel,
    AdministrativeAuditModel,
    ConfigurationChangeRequestModel,
    ConfigurationDefinitionModel,
    ConfigurationDriftModel,
    ConfigurationValueModel,
    ConfigurationVersionModel,
    EnvironmentRecordModel,
    IntegrationRegistryModel,
    MaintenanceWindowModel,
    PlatformPolicyModel,
    PlatformPolicyRuleModel,
    PlatformPolicyVersionModel,
    SecretReferenceModel,
    SystemControlModel,
)


class AdministrationRepository:
    """Database persistence and query layer for Platform Administration entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # --- Configurations ---
    async def create_or_update_config(self, config: ConfigurationDefinitionModel) -> ConfigurationDefinitionModel:
        self.session.add(config)
        await self.session.commit()
        await self.session.refresh(config)
        return config

    async def get_config_by_key(self, key: str) -> Optional[ConfigurationDefinitionModel]:
        stmt = select(ConfigurationDefinitionModel).where(ConfigurationDefinitionModel.key == key)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_configs(self, category: Optional[str] = None) -> List[ConfigurationDefinitionModel]:
        stmt = select(ConfigurationDefinitionModel)
        if category:
            stmt = stmt.where(ConfigurationDefinitionModel.category == category)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_config_version(self, version: ConfigurationVersionModel) -> ConfigurationVersionModel:
        self.session.add(version)
        await self.session.commit()
        await self.session.refresh(version)
        return version

    async def list_config_versions(self, config_key: str) -> List[ConfigurationVersionModel]:
        stmt = select(ConfigurationVersionModel).where(ConfigurationVersionModel.config_key == config_key).order_by(desc(ConfigurationVersionModel.version_number))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Change Requests ---
    async def create_change_request(self, req: ConfigurationChangeRequestModel) -> ConfigurationChangeRequestModel:
        self.session.add(req)
        await self.session.commit()
        await self.session.refresh(req)
        return req

    async def get_change_request(self, change_id: str) -> Optional[ConfigurationChangeRequestModel]:
        stmt = select(ConfigurationChangeRequestModel).where(ConfigurationChangeRequestModel.change_id == change_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_pending_change_requests(self) -> List[ConfigurationChangeRequestModel]:
        stmt = select(ConfigurationChangeRequestModel).where(ConfigurationChangeRequestModel.status == "PENDING_APPROVAL").order_by(desc(ConfigurationChangeRequestModel.created_at))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Policies ---
    async def create_policy(self, policy: PlatformPolicyModel) -> PlatformPolicyModel:
        self.session.add(policy)
        await self.session.commit()
        await self.session.refresh(policy)
        return policy

    async def get_policy(self, policy_id: str) -> Optional[PlatformPolicyModel]:
        stmt = select(PlatformPolicyModel).where(PlatformPolicyModel.policy_id == policy_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_policies(self, domain: Optional[str] = None) -> List[PlatformPolicyModel]:
        stmt = select(PlatformPolicyModel)
        if domain:
            stmt = stmt.where(PlatformPolicyModel.domain == domain)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Feature Flags ---
    async def create_or_update_flag(self, flag: AdminFeatureFlagModel) -> AdminFeatureFlagModel:
        self.session.add(flag)
        await self.session.commit()
        await self.session.refresh(flag)
        return flag

    async def list_flags(self) -> List[AdminFeatureFlagModel]:
        stmt = select(AdminFeatureFlagModel)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Integrations ---
    async def save_provider(self, provider: IntegrationRegistryModel) -> IntegrationRegistryModel:
        self.session.add(provider)
        await self.session.commit()
        await self.session.refresh(provider)
        return provider

    async def list_providers(self) -> List[IntegrationRegistryModel]:
        stmt = select(IntegrationRegistryModel)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Maintenance Windows ---
    async def save_maintenance_window(self, window: MaintenanceWindowModel) -> MaintenanceWindowModel:
        self.session.add(window)
        await self.session.commit()
        await self.session.refresh(window)
        return window

    async def get_active_maintenance_window(self) -> Optional[MaintenanceWindowModel]:
        stmt = select(MaintenanceWindowModel).where(MaintenanceWindowModel.is_active == True)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    # --- System Controls ---
    async def save_system_control(self, control: SystemControlModel) -> SystemControlModel:
        self.session.add(control)
        await self.session.commit()
        await self.session.refresh(control)
        return control

    async def list_system_controls(self) -> List[SystemControlModel]:
        stmt = select(SystemControlModel)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    # --- Audit Log ---
    async def record_audit_event(self, audit: AdministrativeAuditModel) -> AdministrativeAuditModel:
        self.session.add(audit)
        await self.session.commit()
        await self.session.refresh(audit)
        return audit

    async def list_audit_events(self, limit: int = 100) -> List[AdministrativeAuditModel]:
        stmt = select(AdministrativeAuditModel).order_by(desc(AdministrativeAuditModel.timestamp)).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
