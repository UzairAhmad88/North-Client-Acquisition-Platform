"""Phase 64 — Observability, Service Catalog & SRE SLO Error Budget Service."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.services.autonomous_engineering_os.base import (
    BaseAutonomousEngineeringOsService,
    AttrDict,
    ServiceCatalogEntryModel,
)


class ObservabilitySreSloService(BaseAutonomousEngineeringOsService):
    """Service managing production service catalog, SLO targets, latency tracking, and error budgets."""

    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self._services: Dict[str, Any] = {}

    def register_service_catalog_entry(
        self,
        tenant_id: str,
        name: str,
        owner_team: str,
        repository_id: Optional[str] = None,
        slo_target_availability_pct: float = 99.95,
        current_availability_pct: float = 99.98,
        error_budget_remaining_pct: float = 85.0,
        p95_latency_ms: float = 32.0,
    ) -> Any:
        """Register service into production catalog with SLO definitions."""
        status = "HEALTHY"
        if error_budget_remaining_pct < 10.0 or current_availability_pct < slo_target_availability_pct:
            status = "BREACHED"
        elif error_budget_remaining_pct < 30.0:
            status = "DEGRADED"

        srv_id = self.generate_id("eng_srv")
        now = datetime.utcnow()

        if self.db is not None and ServiceCatalogEntryModel is not None:
            entry = ServiceCatalogEntryModel(
                id=srv_id,
                tenant_id=tenant_id,
                name=name,
                owner_team=owner_team,
                repository_id=repository_id,
                slo_target_availability_pct=slo_target_availability_pct,
                current_availability_pct=current_availability_pct,
                error_budget_remaining_pct=error_budget_remaining_pct,
                p95_latency_ms=p95_latency_ms,
                status=status,
                created_at=now,
            )
            self.db.add(entry)
            self.db.commit()
            self.db.refresh(entry)
            return entry
        else:
            entry = AttrDict({
                "id": srv_id,
                "tenant_id": tenant_id,
                "name": name,
                "owner_team": owner_team,
                "repository_id": repository_id,
                "slo_target_availability_pct": slo_target_availability_pct,
                "current_availability_pct": current_availability_pct,
                "error_budget_remaining_pct": error_budget_remaining_pct,
                "p95_latency_ms": p95_latency_ms,
                "status": status,
                "created_at": now,
            })
            self._services[srv_id] = entry
            return entry

    def list_service_catalog(self, tenant_id: str) -> List[Any]:
        """List all registered services."""
        if self.db is not None and ServiceCatalogEntryModel is not None:
            return (
                self.db.query(ServiceCatalogEntryModel)
                .filter(ServiceCatalogEntryModel.tenant_id == tenant_id)
                .all()
            )
        return [s for s in self._services.values() if s.tenant_id == tenant_id]

    def calculate_error_budget_burn_rate(
        self,
        tenant_id: str,
        service_id: str,
        time_window_hours: int = 24,
    ) -> Dict[str, Any]:
        """Calculate SLO error budget burn rate and release readiness recommendation."""
        srv = None
        if self.db is not None and ServiceCatalogEntryModel is not None:
            srv = (
                self.db.query(ServiceCatalogEntryModel)
                .filter(
                    ServiceCatalogEntryModel.tenant_id == tenant_id,
                    ServiceCatalogEntryModel.id == service_id,
                )
                .first()
            )
        else:
            srv = self._services.get(service_id)

        if not srv:
            raise ValueError(f"Service '{service_id}' not found.")

        burn_rate = 1.0 - (srv.error_budget_remaining_pct / 100.0)
        release_permitted = srv.error_budget_remaining_pct > 20.0

        return {
            "service_id": srv.id,
            "service_name": srv.name,
            "target_availability_pct": srv.slo_target_availability_pct,
            "current_availability_pct": srv.current_availability_pct,
            "error_budget_remaining_pct": srv.error_budget_remaining_pct,
            "burn_rate_index": round(burn_rate, 3),
            "release_policy_decision": "ALLOWED" if release_permitted else "BLOCKED_BY_ERROR_BUDGET_EXHAUSTION",
            "evaluated_at": datetime.utcnow().isoformat(),
        }
