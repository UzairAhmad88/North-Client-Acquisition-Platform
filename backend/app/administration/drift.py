"""Configuration Drift Detection and Reconciliation Engine."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.administration.base import DriftItem, DriftSeverity, EnvironmentType
from app.administration.configuration import ConfigurationManager


class ConfigurationDriftDetector:
    """Detects and reconciles divergence between expected version-controlled baseline and runtime state."""

    def __init__(self, config_manager: ConfigurationManager):
        self._config_manager = config_manager
        self._detected_drifts: Dict[str, DriftItem] = {}

    def scan_for_drift(self, runtime_state: Dict[str, Any], env: EnvironmentType = EnvironmentType.PRODUCTION) -> List[DriftItem]:
        """Compare actual runtime values against authoritative registered configuration."""
        drifts = []
        for key, actual_val in runtime_state.items():
            cfg = self._config_manager.get_config(key)
            if not cfg:
                # Unexpected configuration exists in runtime
                drift_id = f"DRIFT-UNREG-{key}"
                item = DriftItem(
                    drift_id=drift_id,
                    key=key,
                    expected_value=None,
                    actual_value=actual_val,
                    severity=DriftSeverity.WARNING,
                    environment=env,
                )
                self._detected_drifts[drift_id] = item
                drifts.append(item)
            elif cfg.current_value != actual_val:
                # Value mismatch
                severity = DriftSeverity.CRITICAL if not cfg.mutable or cfg.policy_controlled else DriftSeverity.WARNING
                drift_id = f"DRIFT-DIFF-{key}"
                item = DriftItem(
                    drift_id=drift_id,
                    key=key,
                    expected_value=cfg.current_value,
                    actual_value=actual_val,
                    severity=severity,
                    environment=env,
                )
                self._detected_drifts[drift_id] = item
                drifts.append(item)

        return drifts

    def list_unresolved_drifts(self) -> List[DriftItem]:
        """List active un-reconciled configuration drifts."""
        return [d for d in self._detected_drifts.values() if not d.resolved]

    def resolve_drift(self, drift_id: str, resolved_by: str) -> DriftItem:
        """Mark a configuration drift item as reconciled."""
        d = self._detected_drifts.get(drift_id)
        if not d:
            raise KeyError(f"Drift record '{drift_id}' not found.")
        d.resolved = True
        return d
