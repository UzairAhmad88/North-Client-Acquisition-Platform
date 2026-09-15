"""Environment Registry and Configuration Promotion Engine."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.administration.base import EnvironmentType


class EnvironmentDefinition(BaseModel):
    env_id: str
    name: str
    env_type: EnvironmentType
    is_production: bool
    requires_approval_for_changes: bool
    allow_mock_providers: bool
    allow_chaos_testing: bool
    allow_real_financial_execution: bool
    status: str = "ACTIVE"
    active_version: str = "v1.0.0"
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EnvironmentPromotionRequest(BaseModel):
    promotion_id: str
    source_env: EnvironmentType
    target_env: EnvironmentType
    configuration_keys: List[str]
    requested_by: str
    approved_by: Optional[str] = None
    status: str = "PENDING_APPROVAL"
    safety_checks_passed: bool = False
    validation_warnings: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EnvironmentManager:
    """Manages isolated deployment environments and safe configuration promotions."""

    def __init__(self):
        self._environments: Dict[EnvironmentType, EnvironmentDefinition] = {}
        self._promotions: Dict[str, EnvironmentPromotionRequest] = {}
        self._seed_default_environments()

    def _seed_default_environments(self):
        """Seed standard multi-tier deployment environments."""
        envs = [
            EnvironmentDefinition(
                env_id="ENV-DEV",
                name="Development Sandbox",
                env_type=EnvironmentType.DEVELOPMENT,
                is_production=False,
                requires_approval_for_changes=False,
                allow_mock_providers=True,
                allow_chaos_testing=True,
                allow_real_financial_execution=False,
            ),
            EnvironmentDefinition(
                env_id="ENV-TEST",
                name="Automated QA & Integration Test",
                env_type=EnvironmentType.TEST,
                is_production=False,
                requires_approval_for_changes=False,
                allow_mock_providers=True,
                allow_chaos_testing=True,
                allow_real_financial_execution=False,
            ),
            EnvironmentDefinition(
                env_id="ENV-STG",
                name="Staging & Pre-Production",
                env_type=EnvironmentType.STAGING,
                is_production=False,
                requires_approval_for_changes=True,
                allow_mock_providers=False,
                allow_chaos_testing=True,
                allow_real_financial_execution=False,
            ),
            EnvironmentDefinition(
                env_id="ENV-PROD",
                name="Production Primary",
                env_type=EnvironmentType.PRODUCTION,
                is_production=True,
                requires_approval_for_changes=True,
                allow_mock_providers=False,
                allow_chaos_testing=False,
                allow_real_financial_execution=True,
            ),
            EnvironmentDefinition(
                env_id="ENV-DR",
                name="Disaster Recovery Standby",
                env_type=EnvironmentType.DR,
                is_production=True,
                requires_approval_for_changes=True,
                allow_mock_providers=False,
                allow_chaos_testing=False,
                allow_real_financial_execution=True,
            ),
        ]
        for env in envs:
            self._environments[env.env_type] = env

    def list_environments(self) -> List[EnvironmentDefinition]:
        """List all registered deployment environments."""
        return list(self._environments.values())

    def get_environment(self, env_type: EnvironmentType) -> Optional[EnvironmentDefinition]:
        """Retrieve environment parameters."""
        return self._environments.get(env_type)

    def create_promotion_request(
        self,
        source_env: EnvironmentType,
        target_env: EnvironmentType,
        keys: List[str],
        requested_by: str,
    ) -> EnvironmentPromotionRequest:
        """Create a promotion request with rigorous cross-environment safety checks."""
        warnings = []
        target = self.get_environment(target_env)
        if not target:
            raise ValueError(f"Target environment {target_env} does not exist.")

        # Safety Check: Promoting from Dev to Prod without Staging
        if source_env == EnvironmentType.DEVELOPMENT and target_env == EnvironmentType.PRODUCTION:
            warnings.append("Direct promotion from DEVELOPMENT to PRODUCTION is high risk. Promotion via STAGING recommended.")

        # Safety Check: Never promote mock providers or chaos flags to production
        safety_passed = True
        if target.is_production:
            for k in keys:
                if "MOCK" in k.upper() or "CHAOS" in k.upper() or "DEBUG" in k.upper():
                    warnings.append(f"Key '{k}' appears to contain test/debug semantics and should not be promoted to production.")
                    safety_passed = False

        promo_id = f"PROMO-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        promo = EnvironmentPromotionRequest(
            promotion_id=promo_id,
            source_env=source_env,
            target_env=target_env,
            configuration_keys=keys,
            requested_by=requested_by,
            safety_checks_passed=safety_passed,
            validation_warnings=warnings,
            status="PENDING_APPROVAL" if target.requires_approval_for_changes else "AUTO_APPROVED",
        )
        self._promotions[promo_id] = promo
        return promo

    def approve_promotion(self, promo_id: str, approved_by: str) -> EnvironmentPromotionRequest:
        """Approve and apply environment configuration promotion."""
        promo = self._promotions.get(promo_id)
        if not promo:
            raise KeyError(f"Promotion request '{promo_id}' not found.")
        if not promo.safety_checks_passed:
            raise ValueError("Cannot approve promotion request that failed critical production safety checks.")
        promo.status = "APPLIED"
        promo.approved_by = approved_by
        return promo
