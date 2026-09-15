"""Centralized Typed Configuration Engine for Platform Administration."""

import copy
import re
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

from app.administration.base import (
    ConfigItem,
    ConfigScope,
    ConfigStatus,
    ConfigType,
    ChangeRiskLevel,
    AdminChangeRequest,
    ChangeStatus,
)


class ConfigurationValidationError(Exception):
    pass


class ImmutableConfigError(Exception):
    pass


class ConfigurationManager:
    """Manages system configuration registration, validation, scope resolution, versioning, diffs, and rollbacks."""

    def __init__(self):
        self._configs: Dict[str, ConfigItem] = {}
        self._scoped_overrides: Dict[str, Dict[str, Any]] = {
            ConfigScope.GLOBAL.value: {},
            ConfigScope.ORGANIZATION.value: {},
            ConfigScope.ENVIRONMENT.value: {},
            ConfigScope.SERVICE.value: {},
        }
        self._history: Dict[str, List[ConfigItem]] = {}
        self._change_requests: Dict[str, AdminChangeRequest] = {}
        self._seed_default_configs()

    def _seed_default_configs(self):
        """Seed authoritative platform configuration definitions."""
        defaults = [
            ConfigItem(
                key="AI_MAX_DAILY_COST",
                display_name="AI Max Daily Cost ($)",
                description="Maximum allowable AI budget per tenant per day in USD.",
                config_type=ConfigType.DECIMAL,
                category="AI / Cost Governance",
                scope=ConfigScope.ORGANIZATION,
                default_value=50.0,
                current_value=50.0,
                validation_rules={"min": 0.0, "max": 10000.0},
                policy_controlled=True,
            ),
            ConfigItem(
                key="AI_TIMEOUT_SECONDS",
                display_name="AI Model Timeout",
                description="Maximum execution timeout in seconds for agent tool/model invocations.",
                config_type=ConfigType.INTEGER,
                category="AI / Performance",
                scope=ConfigScope.GLOBAL,
                default_value=30,
                current_value=30,
                validation_rules={"min": 1, "max": 300},
            ),
            ConfigItem(
                key="INVOICE_AUTO_APPROVAL_LIMIT",
                display_name="Invoice Auto-Approval Limit ($)",
                description="Threshold under which non-disputed invoices can be processed without manual director sign-off.",
                config_type=ConfigType.DECIMAL,
                category="Finance / Billing",
                scope=ConfigScope.ORGANIZATION,
                default_value=500.0,
                current_value=500.0,
                validation_rules={"min": 0.0, "max": 100000.0},
                policy_controlled=True,
            ),
            ConfigItem(
                key="EXTERNAL_MESSAGING_ENABLED",
                display_name="External Messaging Outbound Dispatch",
                description="Master switch controlling whether email/SMS/WhatsApp dispatchers are operational.",
                config_type=ConfigType.BOOLEAN,
                category="Communication",
                scope=ConfigScope.GLOBAL,
                default_value=True,
                current_value=True,
                policy_controlled=True,
            ),
            ConfigItem(
                key="HUMAN_APPROVAL_REQUIRED_FOR_OUTREACH",
                display_name="Mandatory Human Approval for Outreach",
                description="Enforces human-in-the-loop review before any cold outbound message is dispatched.",
                config_type=ConfigType.BOOLEAN,
                category="Communication / Governance",
                scope=ConfigScope.GLOBAL,
                default_value=True,
                current_value=True,
                policy_controlled=True,
                mutable=False,  # Immutable mandatory platform security policy
            ),
            ConfigItem(
                key="PRIMARY_EMAIL_PROVIDER_SECRET",
                display_name="Email Gateway API Secret Ref",
                description="Reference URI to the encrypted key vault holding email provider credentials.",
                config_type=ConfigType.SECRET_REFERENCE,
                category="Integrations / Security",
                scope=ConfigScope.ENVIRONMENT,
                default_value="secret://production/email/api-key",
                current_value="secret://production/email/api-key",
                sensitive=True,
            ),
            ConfigItem(
                key="SESSION_INACTIVITY_TIMEOUT_MINUTES",
                display_name="Session Inactivity Timeout",
                description="Minutes of idle time before an active user session requires re-authentication.",
                config_type=ConfigType.INTEGER,
                category="Security / Auth",
                scope=ConfigScope.GLOBAL,
                default_value=60,
                current_value=60,
                validation_rules={"min": 5, "max": 1440},
            ),
        ]
        for cfg in defaults:
            self._configs[cfg.key] = cfg
            self._history[cfg.key] = [copy.deepcopy(cfg)]

    def register_config(self, item: ConfigItem) -> ConfigItem:
        """Register a new configuration key with validation and default value."""
        self.validate_value(item.config_type, item.current_value, item.validation_rules)
        self._configs[item.key] = item
        if item.key not in self._history:
            self._history[item.key] = [copy.deepcopy(item)]
        return item

    def get_config(self, key: str) -> Optional[ConfigItem]:
        """Get configuration definition and current value."""
        return self._configs.get(key)

    def list_configs(self, category: Optional[str] = None) -> List[ConfigItem]:
        """List all registered configuration keys, optionally filtered by category."""
        if category:
            return [c for c in self._configs.values() if c.category.lower().startswith(category.lower())]
        return list(self._configs.values())

    def validate_value(self, config_type: ConfigType, value: Any, rules: Optional[Dict[str, Any]] = None) -> bool:
        """Strictly validate value against its declared type and constraints."""
        rules = rules or {}

        if config_type == ConfigType.BOOLEAN:
            if not isinstance(value, bool):
                raise ConfigurationValidationError(f"Expected boolean value, got {type(value).__name__}")

        elif config_type == ConfigType.INTEGER:
            if not isinstance(value, int) or isinstance(value, bool):
                raise ConfigurationValidationError(f"Expected integer value, got {type(value).__name__}")
            if "min" in rules and value < rules["min"]:
                raise ConfigurationValidationError(f"Value {value} is below minimum allowed {rules['min']}")
            if "max" in rules and value > rules["max"]:
                raise ConfigurationValidationError(f"Value {value} exceeds maximum allowed {rules['max']}")

        elif config_type == ConfigType.DECIMAL or config_type == ConfigType.PERCENTAGE or config_type == ConfigType.CURRENCY:
            try:
                dec_val = float(value)
            except (ValueError, TypeError):
                raise ConfigurationValidationError(f"Expected numeric/decimal value, got {value}")
            if "min" in rules and dec_val < rules["min"]:
                raise ConfigurationValidationError(f"Value {dec_val} is below minimum {rules['min']}")
            if "max" in rules and dec_val > rules["max"]:
                raise ConfigurationValidationError(f"Value {dec_val} exceeds maximum {rules['max']}")

        elif config_type == ConfigType.STRING:
            if not isinstance(value, str):
                raise ConfigurationValidationError(f"Expected string value, got {type(value).__name__}")
            if "regex" in rules:
                if not re.match(rules["regex"], value):
                    raise ConfigurationValidationError(f"Value '{value}' does not match pattern {rules['regex']}")

        elif config_type == ConfigType.ENUM:
            allowed = rules.get("allowed_values", [])
            if value not in allowed:
                raise ConfigurationValidationError(f"Value '{value}' is not among allowed enum values: {allowed}")

        elif config_type == ConfigType.SECRET_REFERENCE:
            if not isinstance(value, str) or not value.startswith("secret://"):
                raise ConfigurationValidationError("Secret reference must be a URI formatted as 'secret://path/key'")

        elif config_type == ConfigType.JSON or config_type == ConfigType.LIST:
            if not isinstance(value, (dict, list)):
                raise ConfigurationValidationError("Expected JSON dictionary or list")

        return True

    def resolve_value(
        self,
        key: str,
        service: Optional[str] = None,
        environment: Optional[str] = None,
        organization: Optional[str] = None,
    ) -> Any:
        """Resolve effective configuration with priority: Service -> Environment -> Organization -> Global."""
        cfg = self.get_config(key)
        if not cfg:
            raise KeyError(f"Configuration key '{key}' not found.")

        # Check Service scope override
        if service:
            service_key = f"{service}:{key}"
            if service_key in self._scoped_overrides[ConfigScope.SERVICE.value]:
                return self._scoped_overrides[ConfigScope.SERVICE.value][service_key]

        # Check Environment scope override
        if environment:
            env_key = f"{environment}:{key}"
            if env_key in self._scoped_overrides[ConfigScope.ENVIRONMENT.value]:
                return self._scoped_overrides[ConfigScope.ENVIRONMENT.value][env_key]

        # Check Organization scope override
        if organization:
            org_key = f"{organization}:{key}"
            if org_key in self._scoped_overrides[ConfigScope.ORGANIZATION.value]:
                return self._scoped_overrides[ConfigScope.ORGANIZATION.value][org_key]

        # Global default current_value
        return cfg.current_value

    def set_scoped_override(self, scope: ConfigScope, scope_identifier: str, key: str, value: Any) -> None:
        """Set a scoped override with security baseline check."""
        cfg = self.get_config(key)
        if not cfg:
            raise KeyError(f"Configuration key '{key}' not found.")

        if not cfg.mutable:
            raise ImmutableConfigError(f"Configuration '{key}' is immutable and cannot be overridden.")

        self.validate_value(cfg.config_type, value, cfg.validation_rules)
        scoped_key = f"{scope_identifier}:{key}"
        self._scoped_overrides[scope.value][scoped_key] = value

    def create_change_request(
        self,
        key: str,
        new_value: Any,
        reason: str,
        requested_by: str,
        risk_level: ChangeRiskLevel = ChangeRiskLevel.MEDIUM,
    ) -> AdminChangeRequest:
        """Create a validated configuration change request requiring authorization."""
        cfg = self.get_config(key)
        if not cfg:
            raise KeyError(f"Configuration key '{key}' not found.")

        if not cfg.mutable:
            raise ImmutableConfigError(f"Configuration key '{key}' is locked as an immutable security guardrail.")

        self.validate_value(cfg.config_type, new_value, cfg.validation_rules)

        change_id = f"CHG-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{key}"
        change = AdminChangeRequest(
            change_id=change_id,
            key=key,
            old_value=cfg.current_value,
            new_value=new_value,
            reason=reason,
            requested_by=requested_by,
            risk_level=risk_level,
            status=ChangeStatus.PENDING_APPROVAL,
        )
        self._change_requests[change_id] = change
        return change

    def approve_and_apply_change(self, change_id: str, approved_by: str) -> ConfigItem:
        """Approve and apply a pending configuration change with versioning."""
        change = self._change_requests.get(change_id)
        if not change:
            raise KeyError(f"Change request '{change_id}' not found.")

        if change.status != ChangeStatus.PENDING_APPROVAL:
            raise ValueError(f"Change request '{change_id}' is in state {change.status}, cannot approve.")

        cfg = self.get_config(change.key)
        if not cfg:
            raise KeyError(f"Configuration '{change.key}' no longer exists.")

        # Update change record
        change.status = ChangeStatus.APPLIED
        change.approved_by = approved_by
        change.effective_at = datetime.now(timezone.utc)

        # Update configuration version
        cfg.version += 1
        cfg.current_value = change.new_value
        cfg.updated_at = datetime.now(timezone.utc)

        # Append to historical version audit
        self._history[cfg.key].append(copy.deepcopy(cfg))
        return cfg

    def compute_diff(self, key: str, v_from: int, v_to: int) -> Dict[str, Any]:
        """Compute visual diff between two configuration versions."""
        versions = self._history.get(key, [])
        v1_item = next((v for v in versions if v.version == v_from), None)
        v2_item = next((v for v in versions if v.version == v_to), None)

        if not v1_item or not v2_item:
            raise ValueError(f"One or both versions ({v_from}, {v_to}) not found for key '{key}'")

        return {
            "key": key,
            "version_from": v_from,
            "version_to": v_to,
            "old_value": v1_item.current_value,
            "new_value": v2_item.current_value,
            "changed_at": v2_item.updated_at.isoformat(),
            "has_drift": v1_item.current_value != v2_item.current_value,
        }

    def rollback_to_version(self, key: str, target_version: int, rolled_back_by: str, reason: str) -> ConfigItem:
        """Rollback configuration to a historical version by creating a new version with the old value."""
        versions = self._history.get(key, [])
        target_item = next((v for v in versions if v.version == target_version), None)
        if not target_item:
            raise ValueError(f"Target version {target_version} for key '{key}' not found.")

        cfg = self.get_config(key)
        if not cfg:
            raise KeyError(f"Configuration '{key}' not found.")

        # Generate change request for rollback
        change_id = f"ROLLBACK-{key}-v{target_version}"
        cfg.version += 1
        cfg.current_value = target_item.current_value
        cfg.status = ConfigStatus.ROLLED_BACK
        cfg.updated_at = datetime.now(timezone.utc)

        self._history[cfg.key].append(copy.deepcopy(cfg))
        return cfg
