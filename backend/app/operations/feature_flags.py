"""Tenant-aware and tier-gated feature flags, kill-switches, and canary rollouts."""

import hashlib
from typing import Any, Dict, List, Optional


class FeatureFlagManager:
    """Manages feature flags, kill switches, percentage-based canaries, and tenant override rules."""

    def __init__(self) -> None:
        self._flags: Dict[str, Dict[str, Any]] = {
            "ai_predictive_forecasting": {
                "name": "ai_predictive_forecasting",
                "description": "Enable autonomous predictive forecasting agent pipeline",
                "enabled": True,
                "percentage_rollout": 100,
                "allowed_tiers": ["ENTERPRISE", "SCALE", "PRO"],
                "tenant_whitelist": [],
                "tenant_blacklist": [],
            },
            "deep_data_reconciliation": {
                "name": "deep_data_reconciliation",
                "description": "Cross-table SHA-256 financial & ledger reconciliation checks",
                "enabled": True,
                "percentage_rollout": 100,
                "allowed_tiers": ["ENTERPRISE"],
                "tenant_whitelist": [],
                "tenant_blacklist": [],
            },
            "automated_dr_failover": {
                "name": "automated_dr_failover",
                "description": "Enable zero-touch multi-region replica failovers",
                "enabled": False,
                "percentage_rollout": 0,
                "allowed_tiers": ["ENTERPRISE"],
                "tenant_whitelist": [],
                "tenant_blacklist": [],
            },
            "circuit_breaker_strict_mode": {
                "name": "circuit_breaker_strict_mode",
                "description": "Fast fail on non-critical background jobs upon single error spike",
                "enabled": True,
                "percentage_rollout": 100,
                "allowed_tiers": ["ENTERPRISE", "SCALE", "PRO", "STARTER"],
                "tenant_whitelist": [],
                "tenant_blacklist": [],
            },
        }

    def is_enabled(
        self,
        flag_name: str,
        tenant_id: Optional[str] = None,
        tenant_tier: Optional[str] = None,
        default: bool = False,
    ) -> bool:
        """Determines if a feature flag is active for a given tenant context."""
        flag = self._flags.get(flag_name)
        if not flag:
            return default

        # 1. Global kill switch
        if not flag.get("enabled", False):
            return False

        # 2. Blacklist check
        if tenant_id and tenant_id in flag.get("tenant_blacklist", []):
            return False

        # 3. Whitelist check (overrides tier & rollout)
        if tenant_id and tenant_id in flag.get("tenant_whitelist", []):
            return True

        # 4. Tier gating
        allowed_tiers = flag.get("allowed_tiers", [])
        if allowed_tiers and tenant_tier:
            if tenant_tier.upper() not in [t.upper() for t in allowed_tiers]:
                return False

        # 5. Canary / Percentage rollout
        percentage = flag.get("percentage_rollout", 100)
        if percentage >= 100:
            return True
        if percentage <= 0:
            return False
        if not tenant_id:
            return percentage == 100

        # Deterministic hash bucket (0-99)
        hash_val = int(hashlib.sha256(f"{flag_name}:{tenant_id}".encode("utf-8")).hexdigest()[:8], 16)
        bucket = hash_val % 100
        return bucket < percentage

    def set_flag(
        self,
        flag_name: str,
        enabled: bool,
        percentage_rollout: int = 100,
        allowed_tiers: Optional[List[str]] = None,
        tenant_whitelist: Optional[List[str]] = None,
        tenant_blacklist: Optional[List[str]] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates or updates a feature flag configuration."""
        existing = self._flags.get(flag_name, {})
        flag_data = {
            "name": flag_name,
            "description": description or existing.get("description", ""),
            "enabled": enabled,
            "percentage_rollout": max(0, min(100, percentage_rollout)),
            "allowed_tiers": allowed_tiers if allowed_tiers is not None else existing.get("allowed_tiers", []),
            "tenant_whitelist": tenant_whitelist if tenant_whitelist is not None else existing.get("tenant_whitelist", []),
            "tenant_blacklist": tenant_blacklist if tenant_blacklist is not None else existing.get("tenant_blacklist", []),
        }
        self._flags[flag_name] = flag_data
        return flag_data

    def list_flags(self) -> List[Dict[str, Any]]:
        """Returns all configured feature flags."""
        return list(self._flags.values())

    def get_flag(self, flag_name: str) -> Optional[Dict[str, Any]]:
        """Gets single flag configuration."""
        return self._flags.get(flag_name)
