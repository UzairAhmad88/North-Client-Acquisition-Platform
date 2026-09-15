"""
API Router for Phase 68 — Autonomous Infrastructure, Cloud Operating System,
Kubernetes Intelligence, FinOps, Capacity Planning & Self-Optimizing Platform.
Mounted at /infrastructure-cloud-os.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from backend.app.core.database import get_db
except ImportError:
    from app.core.database import get_db

from backend.app.services.infrastructure.service import AutonomousInfrastructureCloudOsService
from backend.app.schemas.autonomous_infrastructure_cloud_os import (
    InfraCloudAccountCreate,
    InfraCloudAccountResponse,
    InfraRegionResponse,
    InfraResourceInventoryCreate,
    InfraResourceInventoryResponse,
    InfraResourceRelationshipCreate,
    InfraResourceRelationshipResponse,
    InfraKubernetesClusterCreate,
    InfraKubernetesClusterResponse,
    InfraKubernetesNodeResponse,
    InfraKubernetesWorkloadResponse,
    InfraScalingPolicyCreate,
    InfraScalingPolicyResponse,
    InfraCapacityForecastRequest,
    InfraCapacityForecastResponse,
    InfraBudgetCreate,
    InfraBudgetResponse,
    InfraCostAnomalyResponse,
    InfraSavingsOpportunityResponse,
    InfraGpuWorkloadCreate,
    InfraGpuWorkloadResponse,
    InfraConfigurationDriftResponse,
    InfraBlastRadiusSimulationRequest,
    InfraBlastRadiusSimulationResponse,
    InfraChangeRequestCreate,
    InfraChangeRequestResponse,
    InfraBackupValidationResponse,
    InfraDisasterRecoveryPlanResponse,
    InfraAgentApprovalRequest,
    InfraOptimizationCycleRequest,
    InfraOptimizationCycleResponse,
)

router = APIRouter(
    prefix="/infrastructure-cloud-os",
    tags=["Phase 68 — Autonomous Infrastructure & Cloud OS"]
)


def get_infra_service(db: Session = Depends(get_db)) -> AutonomousInfrastructureCloudOsService:
    return AutonomousInfrastructureCloudOsService(db)


# 1. Health & Command Center Summary
@router.get("/health", response_model=Dict[str, Any])
def get_infrastructure_health(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    summary = service.get_command_center_summary(tenant_id)
    return {
        "status": "HEALTHY",
        "platform": "Autonomous Infrastructure, Cloud Operating System & Kubernetes Intelligence",
        "telemetry": summary,
    }


@router.get("/command-center/summary", response_model=Dict[str, Any])
def get_command_center_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.get_command_center_summary(tenant_id)


# 2. Cloud Accounts & Regions
@router.post("/accounts", response_model=Dict[str, Any])
def register_cloud_account(
    req: InfraCloudAccountCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.accounts.register_account(
        provider=req.provider,
        account_identifier=req.account_identifier,
        organization=req.organization,
        environment=req.environment,
        default_region=req.default_region,
        tenant_id=tenant_id
    )


@router.get("/accounts", response_model=List[Dict[str, Any]])
def list_cloud_accounts(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.accounts.list_accounts(tenant_id)


@router.get("/regions", response_model=List[Dict[str, Any]])
def list_regions(
    provider: str = Query("AWS"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.regions.list_regions(provider=provider, tenant_id=tenant_id)


# 3. Resource Inventory & Relationship Graph
@router.post("/resources", response_model=Dict[str, Any])
def catalog_resource(
    req: InfraResourceInventoryCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.resources.catalog_resource(
        account_id=req.account_id,
        resource_type=req.resource_type,
        native_id=req.native_id,
        name=req.name,
        region=req.region,
        environment=req.environment,
        tenant_id=tenant_id
    )


@router.get("/resources", response_model=List[Dict[str, Any]])
def list_resources(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.resources.list_resources(tenant_id)


@router.post("/resources/link", response_model=Dict[str, Any])
def link_resources(
    req: InfraResourceRelationshipCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.resource_graph.link_resources(
        source_id=req.source_resource_id,
        target_id=req.target_resource_id,
        relation=req.relationship_type,
        tenant_id=tenant_id
    )


@router.get("/resources/{resource_id}/impact", response_model=Dict[str, Any])
def query_resource_impact(
    resource_id: str,
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.resource_graph.query_impact(resource_id)


# 4. Kubernetes Platform & Clusters
@router.get("/kubernetes/health", response_model=Dict[str, Any])
def get_kubernetes_platform_health(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.kubernetes.get_platform_health(tenant_id)


@router.post("/kubernetes/clusters", response_model=Dict[str, Any])
def register_kubernetes_cluster(
    req: InfraKubernetesClusterCreate,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.clusters.register_cluster(
        cluster_name=req.cluster_name,
        provider=req.provider,
        region=req.region,
        version=req.kubernetes_version,
        tenant_id=tenant_id
    )


@router.get("/kubernetes/clusters", response_model=List[Dict[str, Any]])
def list_kubernetes_clusters(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.clusters.list_clusters(tenant_id)


@router.get("/kubernetes/clusters/{cluster_id}/nodes", response_model=List[Dict[str, Any]])
def list_cluster_nodes(
    cluster_id: str,
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.nodes.list_nodes(cluster_id)


@router.get("/kubernetes/clusters/{cluster_id}/workloads", response_model=List[Dict[str, Any]])
def list_cluster_workloads(
    cluster_id: str,
    namespace: str = Query("production"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.workloads.list_workloads(cluster_id=cluster_id, namespace=namespace)


# 5. Autoscaling & Capacity Planning
@router.post("/scaling/evaluate", response_model=Dict[str, Any])
def evaluate_autoscaling(
    resource_id: str = Query(...),
    current_metric_value: float = Query(82.0),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.scaling.evaluate_scaling(
        resource_id=resource_id,
        current_metric_value=current_metric_value,
        tenant_id=tenant_id
    )


@router.post("/capacity/forecast", response_model=Dict[str, Any])
def forecast_capacity(
    req: InfraCapacityForecastRequest,
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.capacity.forecast_capacity(resource_type=req.resource_type, horizon_days=req.horizon_days)


# 6. FinOps & Cost Intelligence
@router.get("/finops/spend", response_model=Dict[str, Any])
def get_finops_monthly_spend(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.cost.get_monthly_spend(tenant_id)


@router.get("/finops/budgets", response_model=Dict[str, Any])
def get_finops_budgets(
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.budgets.get_budget_status()


@router.get("/finops/optimizations", response_model=List[Dict[str, Any]])
def get_finops_optimizations(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.optimization.identify_optimizations(tenant_id)


# 7. GPU & AI Infrastructure
@router.get("/gpu/stats", response_model=Dict[str, Any])
def get_gpu_cluster_stats(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.gpu.get_gpu_cluster_stats(tenant_id)


# 8. Drift Detection & Change Simulation
@router.get("/drift/scan", response_model=Dict[str, Any])
def scan_configuration_drift(
    cluster_id: str = Query("cls_main_prod"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.drift.scan_for_drift(cluster_id)


@router.post("/changes/simulate", response_model=Dict[str, Any])
def simulate_infrastructure_change(
    req: InfraBlastRadiusSimulationRequest,
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.change_management.simulate_change(
        target_resource=req.target_resource_id,
        action_type=req.action_type
    )


# 9. Disaster Recovery & Backups
@router.get("/disaster-recovery/validate", response_model=Dict[str, Any])
def validate_disaster_recovery(
    plan_id: str = Query("dr_multi_region_prod"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.disaster_recovery.validate_dr_plan(plan_id)


# 10. Governed Remediation & Self-Healing Gate
@router.post("/remediation/execute", response_model=Dict[str, Any])
def execute_remediation(
    runbook_id: str = Query(...),
    target_resource: str = Query(...),
    approver: Optional[str] = Query(None),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.remediation.execute_remediation(
        runbook_id=runbook_id,
        target_resource=target_resource,
        approver=approver,
        tenant_id=tenant_id
    )


# 11. Master Autonomous Infrastructure Self-Optimization Cycle
@router.post("/cycle/optimize", response_model=Dict[str, Any])
def run_optimization_cycle(
    req: InfraOptimizationCycleRequest,
    tenant_id: str = Query("default_tenant"),
    service: AutonomousInfrastructureCloudOsService = Depends(get_infra_service)
):
    return service.run_infrastructure_optimization_cycle(
        tenant_id=tenant_id,
        cluster_name=req.cluster_id or "production-cluster-01",
        dry_run=req.dry_run
    )
