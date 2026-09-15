"""Technical Debt, Team Capacity, DORA Metrics, and Cloud FinOps Service.

Manages technical debt items, aggregate team capacity allocations, DORA performance benchmarks,
and FinOps cloud cost allocation and waste reduction.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.engineering_os.base import (
        AttrDict,
        generate_engineering_id,
    )
except ImportError:
    from app.services.engineering_os.base import (
        AttrDict,
        generate_engineering_id,
    )

logger = logging.getLogger(__name__)


class TechDebtCapacityDoraFinopsService:
    """Manages tech debt, capacity planning, DORA performance metrics, and FinOps costs."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._tech_debt: Dict[str, Dict[str, Any]] = {}
        self._cloud_costs: Dict[str, Dict[str, Any]] = {}

    def log_technical_debt_item(
        self,
        tenant_id: str = "default_tenant",
        title: str = "Legacy monolith sync worker bottleneck",
        area: str = "ARCHITECTURE",
        severity: str = "HIGH",
        effort_person_days: float = 8.0,
        remediation_strategy: str = "Decouple synchronous REST calls into Kafka pub/sub events.",
    ) -> AttrDict:
        debt_id = generate_engineering_id("debt")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "debt_id": debt_id,
            "id": debt_id,
            "tenant_id": tenant_id,
            "title": title,
            "area": area,
            "severity": severity,
            "effort_person_days": effort_person_days,
            "remediation_strategy": remediation_strategy,
            "status": "LOGGED",
            "created_at": now,
        }
        self._tech_debt[debt_id] = record
        return AttrDict(record)

    def calculate_dora_metrics(
        self,
        tenant_id: str = "default_tenant",
        timeframe_days: int = 30,
        deployment_frequency_per_day: float = 4.5,
        lead_time_for_changes_hours: float = 2.4,
        change_failure_rate_pct: float = 1.8,
        time_to_restore_service_minutes: float = 22.0,
    ) -> AttrDict:
        """Calculate standard 4 DORA performance metrics and classification tier."""
        dora_id = generate_engineering_id("dora")
        now = datetime.now(timezone.utc).isoformat()

        # DORA Tier Classification: ELITE, HIGH, MEDIUM, LOW
        if (
            deployment_frequency_per_day >= 1.0
            and lead_time_for_changes_hours < 24.0
            and change_failure_rate_pct < 5.0
            and time_to_restore_service_minutes < 60.0
        ):
            dora_tier = "ELITE"
        elif deployment_frequency_per_day >= 0.2:
            dora_tier = "HIGH"
        else:
            dora_tier = "MEDIUM"

        record = {
            "dora_id": dora_id,
            "id": dora_id,
            "tenant_id": tenant_id,
            "timeframe_days": timeframe_days,
            "deployment_frequency_per_day": deployment_frequency_per_day,
            "lead_time_for_changes_hours": lead_time_for_changes_hours,
            "change_failure_rate_pct": change_failure_rate_pct,
            "time_to_restore_service_minutes": time_to_restore_service_minutes,
            "dora_performance_tier": dora_tier,
            "evaluated_at": now,
        }
        return AttrDict(record)

    def record_cloud_finops_cost(
        self,
        tenant_id: str = "default_tenant",
        service_name: str = "decision-room-cluster",
        environment: str = "PRODUCTION",
        monthly_cost_usd: float = 14500.0,
        waste_estimate_usd: float = 1800.0,
        cost_trend_pct: float = -4.2,
    ) -> AttrDict:
        cost_id = generate_engineering_id("cost")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "cost_id": cost_id,
            "id": cost_id,
            "tenant_id": tenant_id,
            "service_name": service_name,
            "environment": environment,
            "monthly_cost_usd": monthly_cost_usd,
            "waste_estimate_usd": waste_estimate_usd,
            "cost_trend_pct": cost_trend_pct,
            "optimization_opportunity": "Right-size underutilized compute nodes and convert on-demand to savings plans.",
            "recorded_at": now,
        }
        self._cloud_costs[cost_id] = record
        return AttrDict(record)
