"""Administrative Health Score and Governance Telemetry Engine."""

from datetime import datetime, timezone
from typing import Dict, List

from app.administration.base import (
    AdminHealthReport,
    AdminHealthStatus,
    DriftSeverity,
    KillSwitchState,
    MaintenanceMode,
)
from app.administration.configuration import ConfigurationManager
from app.administration.drift import ConfigurationDriftDetector
from app.administration.integrations import IntegrationManager
from app.administration.maintenance import MaintenanceManager
from app.administration.policies import PolicyEngine
from app.administration.system_controls import SystemControlManager


class AdminHealthEngine:
    """Computes comprehensive health score and operational readiness across all control planes."""

    def __init__(
        self,
        config_manager: ConfigurationManager,
        policy_engine: PolicyEngine,
        integration_manager: IntegrationManager,
        system_controls: SystemControlManager,
        maintenance_manager: MaintenanceManager,
        drift_detector: ConfigurationDriftDetector,
    ):
        self._config_manager = config_manager
        self._policy_engine = policy_engine
        self._integration_manager = integration_manager
        self._system_controls = system_controls
        self._maintenance_manager = maintenance_manager
        self._drift_detector = drift_detector

    def compute_health_report(self) -> AdminHealthReport:
        """Compute holistic administration control plane health."""
        # 1. Configuration validity (all registered configs pass validation rules)
        configs = self._config_manager.list_configs()
        valid_configs = sum(1 for c in configs if self._config_manager.validate_value(c.config_type, c.current_value, c.validation_rules))
        cfg_score = (valid_configs / len(configs) * 100.0) if configs else 100.0

        # 2. Policy consistency
        policies = self._policy_engine.list_policies()
        policy_score = 100.0 if policies else 90.0

        # 3. Integration health
        providers = self._integration_manager.list_providers()
        healthy_providers = sum(1 for p in providers if p.health_status == "HEALTHY")
        integration_score = (healthy_providers / len(providers) * 100.0) if providers else 100.0

        # 4. Drift count
        unresolved_drifts = self._drift_detector.list_unresolved_drifts()
        drift_count = len(unresolved_drifts)
        critical_drift_count = sum(1 for d in unresolved_drifts if d.severity == DriftSeverity.CRITICAL)

        # 5. Kill switches active
        switches = self._system_controls.list_switches()
        active_switches = sum(1 for s in switches if s.state == KillSwitchState.ACTIVE)

        # 6. Maintenance mode
        mode = self._maintenance_manager.get_current_mode()

        # Composite status determination
        if mode == MaintenanceMode.EMERGENCY or critical_drift_count > 0:
            status = AdminHealthStatus.CRITICAL
        elif active_switches > 0 or integration_score < 70.0 or drift_count > 3:
            status = AdminHealthStatus.AT_RISK
        elif mode != MaintenanceMode.NORMAL or integration_score < 90.0:
            status = AdminHealthStatus.STABLE
        else:
            status = AdminHealthStatus.HEALTHY

        return AdminHealthReport(
            status=status,
            configuration_validity_score=round(cfg_score, 1),
            policy_consistency_score=round(policy_score, 1),
            integration_health_score=round(integration_score, 1),
            drift_count=drift_count,
            pending_approvals_count=0,
            active_kill_switches_count=active_switches,
            active_maintenance_mode=mode,
            details={
                "total_configs": len(configs),
                "total_policies": len(policies),
                "total_providers": len(providers),
                "healthy_providers": healthy_providers,
                "critical_drifts": critical_drift_count,
            },
        )
