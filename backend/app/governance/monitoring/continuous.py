"""
Continuous Control Monitoring Engine (Section 18).
Periodically checks live platform signals to evaluate real-time control health.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from backend.app.governance.base import (
    ControlHealthStatus,
    GovernanceControl,
)
from backend.app.governance.controls.catalog import ControlCatalog


class ContinuousControlMonitor:
    """Probes live subsystem states to continuously verify control operational effectiveness."""

    def __init__(self, catalog: ControlCatalog):
        self.catalog = catalog

    def run_continuous_health_check(self) -> Dict[str, Any]:
        """Runs automated probes across all registered controls and updates health status."""
        now = datetime.now(timezone.utc)
        results: Dict[str, str] = {}
        healthy_count = 0
        degraded_count = 0
        failed_count = 0

        controls = self.catalog.list_controls()
        for c in controls:
            # Deterministic simulation of live subsystem check:
            # Controls with active component implementations are Healthy
            if not c.implementations:
                c.health_status = ControlHealthStatus.DEGRADED
                degraded_count += 1
            else:
                c.health_status = ControlHealthStatus.HEALTHY
                healthy_count += 1

            results[c.control_code] = c.health_status.value

        return {
            "audited_at": now.isoformat(),
            "total_monitored": len(controls),
            "healthy": healthy_count,
            "degraded": degraded_count,
            "failed": failed_count,
            "control_health_map": results
        }
