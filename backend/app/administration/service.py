"""Unified Platform Administration and Governance Service Facade."""

from typing import Any, Dict, List, Optional

from app.administration.base import (
    AdminHealthReport,
    AdminHealthStatus,
    ConfigItem,
    ConfigScope,
    ConfigType,
    ChangeRiskLevel,
    AdminChangeRequest,
    EnvironmentType,
    FeatureFlagItem,
    FlagStatus,
    KillSwitchItem,
    MaintenanceMode,
    PolicyDomain,
    PolicyEvaluationResult,
    PolicyItem,
    RolloutType,
)
from app.administration.configuration import ConfigurationManager
from app.administration.drift import ConfigurationDriftDetector
from app.administration.environments import EnvironmentManager
from app.administration.feature_flags import AdminFeatureFlagManager
from app.administration.health import AdminHealthEngine
from app.administration.integrations import IntegrationManager
from app.administration.maintenance import MaintenanceManager
from app.administration.policies import PolicyEngine
from app.administration.system_controls import SystemControlManager


class PlatformAdministrationService:
    """Enterprise Control Plane aggregating all administrative governance capabilities."""

    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.policy_engine = PolicyEngine()
        self.feature_flag_manager = AdminFeatureFlagManager()
        self.environment_manager = EnvironmentManager()
        self.integration_manager = IntegrationManager()
        self.system_controls = SystemControlManager()
        self.maintenance_manager = MaintenanceManager()
        self.drift_detector = ConfigurationDriftDetector(self.config_manager)
        self.health_engine = AdminHealthEngine(
            self.config_manager,
            self.policy_engine,
            self.integration_manager,
            self.system_controls,
            self.maintenance_manager,
            self.drift_detector,
        )

    def get_overview(self) -> Dict[str, Any]:
        """Aggregate administrative control plane overview."""
        health = self.health_engine.compute_health_report()
        return {
            "health": health.model_dump(),
            "configs_count": len(self.config_manager.list_configs()),
            "policies_count": len(self.policy_engine.list_policies()),
            "feature_flags_count": len(self.feature_flag_manager.list_flags()),
            "providers_count": len(self.integration_manager.list_providers()),
            "environments_count": len(self.environment_manager.list_environments()),
            "kill_switches_count": len(self.system_controls.list_switches()),
            "maintenance_mode": self.maintenance_manager.get_current_mode().value,
        }
