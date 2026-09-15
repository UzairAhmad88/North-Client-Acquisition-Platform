"""API Endpoints for Centralized KPI Registry, Snapshot Calculations & Cross-Domain Reconciliation."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.business_os.base import KPICategory
from app.business_os.kpi import KPIDefinition
from app.business_os.service import BusinessOSPlatformService
from app.schemas.business_os import (
    CrossDomainReconciliationRequest,
    KPIDefinitionCreate,
    KPISnapshotResponse,
)

router = APIRouter(prefix="/kpis", tags=["kpi-registry"])

_service_instance = BusinessOSPlatformService()


def get_business_os_service() -> BusinessOSPlatformService:
    return _service_instance


@router.get("", response_model=List[KPISnapshotResponse])
async def list_kpi_snapshots(
    category: Optional[KPICategory] = Query(None),
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """List calculated KPI snapshots across organizational categories."""
    return service.list_kpis(category=category)


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_kpi_definition(
    payload: KPIDefinitionCreate,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Dict[str, Any]:
    """Register or update an authoritative metric definition in the KPI Registry."""
    defn = KPIDefinition(
        kpi_id=payload.kpi_id,
        name=payload.name,
        category=payload.category,
        description=payload.description,
        unit=payload.unit,
        currency=payload.currency,
        source_domain=payload.source_domain,
        formula=payload.formula,
        target_value=payload.target_value,
        warning_threshold=payload.warning_threshold,
        critical_threshold=payload.critical_threshold,
        freshness_max_seconds=payload.freshness_max_seconds,
        is_higher_better=payload.is_higher_better,
    )
    service.kpi_registry.register_or_update(defn)
    return {"status": "registered", "kpi_id": payload.kpi_id, "version": defn.version}


@router.post("/reconcile", response_model=List[Dict[str, Any]])
async def reconcile_cross_domain_metrics(
    payload: CrossDomainReconciliationRequest,
    service: BusinessOSPlatformService = Depends(get_business_os_service),
) -> Any:
    """Verify consistency across Finance, CRM, and Contract baselines."""
    return service.reconcile_metrics(
        finance_revenue=payload.finance_revenue,
        crm_revenue=payload.crm_closed_won_revenue,
        active_contracts=payload.active_contracts_count,
        active_billing_profiles=payload.active_billing_profiles_count,
    )
