"""Centralized Feature Flag Management Engine for Platform Administration."""

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.administration.base import EnvironmentType, FeatureFlagItem, FlagStatus, RolloutType


class AdminFeatureFlagManager:
    """Manages enterprise feature flag definitions, percentage rollouts, and tenant tier gating."""

    def __init__(self):
        self._flags: Dict[str, FeatureFlagItem] = {}
        self._seed_default_flags()

    def _seed_default_flags(self):
        """Seed default operational and product feature flags."""
        defaults = [
            FeatureFlagItem(
                key="AI_EXECUTIVE_COPILOT",
                name="Executive AI Decision Copilot",
                description="Enables the natural-language strategic briefing and scenario copilot for executive users.",
                status=FlagStatus.ENABLED,
                rollout_type=RolloutType.TENANT_TIER,
                allowed_tiers=["ENTERPRISE", "PRO"],
                environment=EnvironmentType.PRODUCTION,
            ),
            FeatureFlagItem(
                key="ADVANCED_VECTOR_SEARCH",
                name="Hybrid Dense Vector Search Engine",
                description="Routes search queries through Qdrant/pgvector embedding stores.",
                status=FlagStatus.CANARY,
                rollout_type=RolloutType.PERCENTAGE,
                rollout_percentage=25,
                environment=EnvironmentType.PRODUCTION,
            ),
            FeatureFlagItem(
                key="AUTONOMOUS_RESEARCH_DISCOVERY",
                name="Autonomous Lead Discovery & Enrichment",
                description="Enables asynchronous research agent pipelines for prospect qualification.",
                status=FlagStatus.ENABLED,
                rollout_type=RolloutType.BOOLEAN,
                environment=EnvironmentType.PRODUCTION,
            ),
            FeatureFlagItem(
                key="REAL_TIME_STRIPE_PAYMENTS",
                name="Direct Stripe Gateway Processing",
                description="Switches invoice checkout from manual wire instructions to real-time card capture.",
                status=FlagStatus.DISABLED,
                rollout_type=RolloutType.BOOLEAN,
                environment=EnvironmentType.PRODUCTION,
            ),
        ]
        for f in defaults:
            self._flags[f.key] = f

    def register_flag(self, flag: FeatureFlagItem) -> FeatureFlagItem:
        """Register a new feature flag."""
        self._flags[flag.key] = flag
        return flag

    def get_flag(self, key: str) -> Optional[FeatureFlagItem]:
        """Get flag definition."""
        return self._flags.get(key)

    def list_flags(self, environment: Optional[EnvironmentType] = None) -> List[FeatureFlagItem]:
        """List flags, optionally filtered by environment."""
        if environment:
            return [f for f in self._flags.values() if f.environment == environment]
        return list(self._flags.values())

    def set_flag_status(self, key: str, status: FlagStatus, updated_by: str = "admin") -> FeatureFlagItem:
        """Update flag status with audit version bump."""
        flag = self.get_flag(key)
        if not flag:
            raise KeyError(f"Feature flag '{key}' not found.")
        flag.status = status
        flag.version += 1
        flag.owner = updated_by
        flag.updated_at = datetime.now(timezone.utc)
        return flag

    def update_rollout(
        self,
        key: str,
        rollout_type: RolloutType,
        percentage: int = 0,
        allowed_tiers: Optional[List[str]] = None,
    ) -> FeatureFlagItem:
        """Update flag rollout parameters."""
        flag = self.get_flag(key)
        if not flag:
            raise KeyError(f"Feature flag '{key}' not found.")
        flag.rollout_type = rollout_type
        flag.rollout_percentage = max(0, min(100, percentage))
        if allowed_tiers is not None:
            flag.allowed_tiers = allowed_tiers
        flag.version += 1
        flag.updated_at = datetime.now(timezone.utc)
        return flag

    def is_enabled(
        self,
        key: str,
        user_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        tenant_tier: Optional[str] = None,
    ) -> bool:
        """Evaluate if feature flag is active for the specific user/tenant context."""
        flag = self.get_flag(key)
        if not flag:
            return False

        if flag.status == FlagStatus.DISABLED:
            return False

        if flag.status == FlagStatus.ENABLED:
            if flag.rollout_type == RolloutType.BOOLEAN:
                return True
            if flag.rollout_type == RolloutType.TENANT_TIER:
                return (tenant_tier or "").upper() in [t.upper() for t in flag.allowed_tiers]

        if flag.status in [FlagStatus.CANARY, FlagStatus.ENABLED] and flag.rollout_type == RolloutType.PERCENTAGE:
            # Deterministic hash of entity ID to assign bucket 0-99
            entity = user_id or tenant_id or "default"
            hash_val = int(hashlib.sha256(f"{key}:{entity}".encode("utf-8")).hexdigest()[:8], 16)
            bucket = hash_val % 100
            return bucket < flag.rollout_percentage

        return False
