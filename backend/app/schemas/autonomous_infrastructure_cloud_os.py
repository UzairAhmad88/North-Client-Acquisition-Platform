"""
Phase 68: Autonomous Infrastructure, Cloud Operating System, Kubernetes Intelligence,
FinOps, Capacity Planning & Self-Optimizing Platform Schemas.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# 1. Cloud Accounts & Regions
class CloudAccountCreate(BaseModel):
    provider: str = "AWS"  # AWS, GCP, AZURE, ON_PREM
    account_identifier: str
    organization: str = "Uzaii Enterprise"
    environment: str = "PRODUCTION"
    default_region: str = "us-east-1"
    cost_center: str = "INFRA-CORE"
    owner: str = "cloud-admin@enterprise.internal"
    credentials_vault_ref: Optional[str] = None


class CloudAccountResponse(BaseModel):
    id: str
    tenant_id: str
    provider: str
    account_identifier: str
    organization: str
    environment: str
    default_region: str
    cost_center: str
    owner: str
    status: str
    security_state: str
    created_at: Optional[Any] = None

    class Config:
        from_attributes = True


class RegionResponse(BaseModel):
    id: str
    provider: str
    region_name: str
    display_name: str
    availability_zones_count: int
    latency_score_ms: float
    cost_tier: str
    compliance_boundary: str
    health_status: str


# 2. Resource Inventory & Relationships
class ResourceInventoryCreate(BaseModel):
    account_id: str
    resource_type: str
    native_id: str
    name: str
    region: str = "us-east-1"
    environment: str = "PRODUCTION"
    project: str = "Core Platform"
    service: str = "core-service"
    cost_center: str = "INFRA-CORE"
    criticality: str = "TIER_1"
    monthly_cost_usd: float = 0.0
    tags: Dict[str, str] = Field(default_factory=dict)


class ResourceInventoryResponse(BaseModel):
    id: str
    tenant_id: str
    account_id: str
    resource_type: str
    native_id: str
    name: str
    region: str
    environment: str
    project: str
    service: str
    cost_center: str
    criticality: str
    status: str
    security_state: str
    monthly_cost_usd: float
    tags: Dict[str, Any]
    created_at: Optional[Any] = None

    class Config:
        from_attributes = True


class ResourceRelationshipCreate(BaseModel):
    source_resource_id: str
    target_resource_id: str
    relationship_type: str  # DEPLOYED_ON, RUNS_ON, DEPENDS_ON, USES
    blast_radius_multiplier: float = 1.0


class ResourceRelationshipResponse(BaseModel):
    id: str
    source_resource_id: str
    target_resource_id: str
    relationship_type: str
    blast_radius_multiplier: float


# 3. Kubernetes Platform
class KubernetesClusterCreate(BaseModel):
    cluster_name: str
    kubernetes_version: str = "1.30.2"
    provider: str = "EKS"
    region: str = "us-east-1"
    total_nodes: int = 12


class KubernetesClusterResponse(BaseModel):
    id: str
    tenant_id: str
    cluster_name: str
    kubernetes_version: str
    provider: str
    region: str
    total_nodes: int
    healthy_nodes: int
    total_namespaces: int
    workloads_count: int
    health_status: str
    endpoint_url: str

    class Config:
        from_attributes = True


class KubernetesNodeResponse(BaseModel):
    id: str
    cluster_id: str
    node_name: str
    instance_type: str
    cpu_allocatable_cores: float
    cpu_allocated_cores: float
    memory_allocatable_gb: float
    memory_allocated_gb: float
    pod_capacity: int
    pods_running: int
    ready: bool


class KubernetesWorkloadResponse(BaseModel):
    id: str
    cluster_id: str
    namespace: str
    name: str
    workload_type: str
    desired_replicas: int
    available_replicas: int
    image_tag: str
    cpu_request: str
    memory_request: str
    hpa_enabled: bool
    health_status: str


# 4. Scaling & Capacity
class ScalingPolicyCreate(BaseModel):
    target_resource_id: str
    policy_name: str
    min_replicas: int = 2
    max_replicas: int = 20
    target_cpu_utilization: float = 70.0
    target_memory_utilization: float = 80.0


class ScalingPolicyResponse(BaseModel):
    id: str
    target_resource_id: str
    policy_name: str
    min_replicas: int
    max_replicas: int
    target_cpu_utilization: float
    target_memory_utilization: float


class CapacityForecastRequest(BaseModel):
    resource_type: str = "CPU_CORES"
    horizon_days: int = 90


class CapacityForecastResponse(BaseModel):
    id: str
    resource_type: str
    forecast_horizon_days: int
    current_capacity: float
    forecasted_demand: float
    headroom_percentage: float
    exhaustion_risk: str
    recommended_procurement: Dict[str, Any]


# 5. FinOps, Budgets & Savings
class BudgetCreate(BaseModel):
    name: str
    monthly_limit_usd: float = 15000.0
    alert_threshold_pct: float = 80.0


class BudgetResponse(BaseModel):
    id: str
    name: str
    monthly_limit_usd: float
    actual_spend_usd: float
    forecast_spend_usd: float
    alert_threshold_pct: float
    status: str


class CostAnomalyResponse(BaseModel):
    id: str
    service_name: str
    baseline_spend_usd: float
    actual_spike_usd: float
    deviation_factor: float
    driver: str
    status: str


class SavingsOpportunityResponse(BaseModel):
    id: str
    category: str
    title: str
    resource_id: str
    estimated_monthly_savings_usd: float
    risk_level: str
    status: str


# 6. GPU & AI Infrastructure
class GpuWorkloadCreate(BaseModel):
    workload_name: str
    gpu_type: str = "NVIDIA_H100_SXM5"
    gpu_count: int = 4
    workload_priority: str = "HIGH"


class GpuWorkloadResponse(BaseModel):
    id: str
    workload_name: str
    gpu_type: str
    gpu_count: int
    vram_allocated_gb: float
    gpu_utilization_pct: float
    workload_priority: str
    cost_per_hour_usd: float


# 7. Drift, Blast Radius & Change Management
class ConfigurationDriftResponse(BaseModel):
    id: str
    resource_id: str
    drift_severity: str
    is_critical_security_drift: bool
    remediation_proposal: Optional[str]
    status: str


class BlastRadiusSimulationRequest(BaseModel):
    target_resource_id: str
    action_type: str  # TERMINATE_NODE, SCALE_DOWN, UPGRADE_CLUSTER, DESTROY_VOLUME


class BlastRadiusSimulationResponse(BaseModel):
    simulation_id: str
    target_resource_id: str
    affected_services: List[str]
    affected_workloads_count: int
    estimated_cost_delta_usd: float
    availability_risk: str  # LOW, MEDIUM, HIGH, CRITICAL
    rollback_ready: bool
    dry_run_passed: bool


class ChangeRequestCreate(BaseModel):
    title: str
    reason: str
    risk_score: str = "MEDIUM"
    rollback_plan: str


class ChangeRequestResponse(BaseModel):
    id: str
    title: str
    reason: str
    risk_score: str
    approval_status: str
    execution_status: str


# 8. Disaster Recovery & Backups
class BackupValidationResponse(BaseModel):
    id: str
    resource_id: str
    backup_snapshot_id: str
    checksum_verified: bool
    restore_duration_seconds: float
    rpo_met: bool
    rto_met: bool
    status: str


class DisasterRecoveryPlanResponse(BaseModel):
    id: str
    plan_name: str
    target_rpo_minutes: int
    target_rto_minutes: int
    primary_region: str
    failover_region: str
    active_replication: bool
    last_drill_status: str


# 9. Agent Approvals & Optimization Cycle
class AgentApprovalRequest(BaseModel):
    approval_id: str
    decision: str  # APPROVED, REJECTED
    approver: str
    notes: Optional[str] = None


class OptimizationCycleRequest(BaseModel):
    cluster_id: Optional[str] = None
    target_environment: str = "PRODUCTION"
    dry_run: bool = True


class OptimizationCycleResponse(BaseModel):
    cycle_id: str
    status: str
    phases_completed: List[str]
    savings_identified_usd: float
    workloads_rightsized_count: int
    capacity_headroom_pct: float
    approval_required: bool
    dry_run: bool


# Aliases for Infra* naming
InfraCloudAccountCreate = CloudAccountCreate
InfraCloudAccountResponse = CloudAccountResponse
InfraRegionResponse = RegionResponse
InfraResourceInventoryCreate = ResourceInventoryCreate
InfraResourceInventoryResponse = ResourceInventoryResponse
InfraResourceRelationshipCreate = ResourceRelationshipCreate
InfraResourceRelationshipResponse = ResourceRelationshipResponse
InfraKubernetesClusterCreate = KubernetesClusterCreate
InfraKubernetesClusterResponse = KubernetesClusterResponse
InfraKubernetesNodeResponse = KubernetesNodeResponse
InfraKubernetesWorkloadResponse = KubernetesWorkloadResponse
InfraScalingPolicyCreate = ScalingPolicyCreate
InfraScalingPolicyResponse = ScalingPolicyResponse
InfraCapacityForecastRequest = CapacityForecastRequest
InfraCapacityForecastResponse = CapacityForecastResponse
InfraBudgetCreate = BudgetCreate
InfraBudgetResponse = BudgetResponse
InfraCostAnomalyResponse = CostAnomalyResponse
InfraSavingsOpportunityResponse = SavingsOpportunityResponse
InfraGpuWorkloadCreate = GpuWorkloadCreate
InfraGpuWorkloadResponse = GpuWorkloadResponse
InfraConfigurationDriftResponse = ConfigurationDriftResponse
InfraBlastRadiusSimulationRequest = BlastRadiusSimulationRequest
InfraBlastRadiusSimulationResponse = BlastRadiusSimulationResponse
InfraChangeRequestCreate = ChangeRequestCreate
InfraChangeRequestResponse = ChangeRequestResponse
InfraBackupValidationResponse = BackupValidationResponse
InfraDisasterRecoveryPlanResponse = DisasterRecoveryPlanResponse
InfraAgentApprovalRequest = AgentApprovalRequest
InfraOptimizationCycleRequest = OptimizationCycleRequest
InfraOptimizationCycleResponse = OptimizationCycleResponse
