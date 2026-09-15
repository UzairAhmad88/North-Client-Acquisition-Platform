"""
Phase 68: Autonomous Infrastructure, Cloud Operating System, Kubernetes Intelligence,
FinOps, Capacity Planning & Self-Optimizing Platform Models.
Table prefix: infra_* to guarantee zero collision with earlier phases.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Float,
    Integer,
    DateTime,
    JSON,
    ForeignKey,
    Index
)
try:
    from app.models.base import Base
except ImportError:
    from backend.app.models.base import Base



def utc_now():
    return datetime.now(timezone.utc)


def generate_uuid():
    return str(uuid.uuid4())


# 1. Cloud Accounts & Regions
class InfraCloudAccountModel(Base):
    __tablename__ = "infra_cloud_accounts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    provider = Column(String(32), nullable=False, default="AWS")  # AWS, GCP, AZURE, ON_PREM
    account_identifier = Column(String(64), nullable=False, index=True)
    organization = Column(String(128), nullable=False, default="Uzaii Enterprise")
    environment = Column(String(32), nullable=False, default="PRODUCTION")  # DEV, STAGING, PROD
    default_region = Column(String(32), nullable=False, default="us-east-1")
    cost_center = Column(String(64), nullable=False, default="INFRA-CORE")
    owner = Column(String(128), nullable=False, default="cloud-admin@enterprise.internal")
    status = Column(String(32), nullable=False, default="ACTIVE")
    security_state = Column(String(32), nullable=False, default="COMPLIANT")
    credentials_vault_ref = Column(String(128), nullable=True)  # Secret key ref, never plaintext
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraRegionModel(Base):
    __tablename__ = "infra_regions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    provider = Column(String(32), nullable=False, default="AWS")
    region_name = Column(String(64), nullable=False, index=True)
    display_name = Column(String(128), nullable=False)
    availability_zones_count = Column(Integer, default=3)
    latency_score_ms = Column(Float, default=18.5)
    cost_tier = Column(String(32), default="STANDARD")
    compliance_boundary = Column(String(64), default="US_EAST_FEDRAMP")
    data_residency_guarantee = Column(String(64), default="US_DOMESTIC")
    health_status = Column(String(32), default="HEALTHY")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 2. Resource Inventory & Relationships
class InfraResourceInventoryModel(Base):
    __tablename__ = "infra_resources"
    __table_args__ = (
        Index("ix_infra_res_tenant_type", "tenant_id", "resource_type"),
        {"extend_existing": True},
    )

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    account_id = Column(String(36), nullable=False, index=True)
    resource_type = Column(String(64), nullable=False)  # COMPUTE, K8S_CLUSTER, STORAGE, DATABASE, NETWORK
    native_id = Column(String(128), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    region = Column(String(32), nullable=False, default="us-east-1")
    environment = Column(String(32), nullable=False, default="PRODUCTION")
    project = Column(String(64), nullable=False, default="Core Platform")
    service = Column(String(64), nullable=False, default="core-service")
    cost_center = Column(String(64), nullable=False, default="INFRA-CORE")
    criticality = Column(String(32), nullable=False, default="TIER_1")
    status = Column(String(32), nullable=False, default="ACTIVE")
    security_state = Column(String(32), nullable=False, default="HEALTHY")
    monthly_cost_usd = Column(Float, default=0.0)
    configuration_snapshot = Column(JSON, nullable=False, default=dict)
    tags = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraResourceRelationshipModel(Base):
    __tablename__ = "infra_resource_relationships"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    source_resource_id = Column(String(36), nullable=False, index=True)
    target_resource_id = Column(String(36), nullable=False, index=True)
    relationship_type = Column(String(64), nullable=False)  # DEPLOYED_ON, RUNS_ON, DEPENDS_ON, USES
    blast_radius_multiplier = Column(Float, default=1.0)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 3. Compute, Storage, Network, Database
class InfraComputeInstanceModel(Base):
    __tablename__ = "infra_compute"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    resource_id = Column(String(36), nullable=False, index=True)
    instance_type = Column(String(64), nullable=False, default="c6i.2xlarge")
    vcpus = Column(Integer, default=8)
    memory_gb = Column(Float, default=16.0)
    cpu_utilization_pct = Column(Float, default=32.4)
    memory_utilization_pct = Column(Float, default=45.1)
    lifecycle = Column(String(32), default="ON_DEMAND")  # ON_DEMAND, SPOT, RESERVED
    status = Column(String(32), default="RUNNING")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraStorageVolumeModel(Base):
    __tablename__ = "infra_storage"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    resource_id = Column(String(36), nullable=False, index=True)
    storage_type = Column(String(32), default="BLOCK")  # BLOCK, OBJECT, FILE
    storage_class = Column(String(32), default="GP3")
    capacity_gb = Column(Float, default=500.0)
    used_gb = Column(Float, default=180.0)
    iops = Column(Integer, default=3000)
    encrypted = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraNetworkVpcModel(Base):
    __tablename__ = "infra_networks"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    vpc_id = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    cidr_block = Column(String(32), default="10.0.0.0/16")
    subnets_count = Column(Integer, default=6)
    nat_gateways_count = Column(Integer, default=3)
    peered_vpcs = Column(JSON, default=list)
    flow_logs_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraDatabaseInstanceModel(Base):
    __tablename__ = "infra_databases"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    name = Column(String(128), nullable=False)
    engine = Column(String(32), default="POSTGRESQL")
    engine_version = Column(String(32), default="16.2")
    instance_class = Column(String(64), default="db.r6g.xlarge")
    allocated_storage_gb = Column(Float, default=1000.0)
    storage_used_pct = Column(Float, default=42.5)
    connection_count = Column(Integer, default=85)
    max_connections = Column(Integer, default=500)
    replication_lag_seconds = Column(Float, default=0.02)
    multi_az = Column(Boolean, default=True)
    status = Column(String(32), default="AVAILABLE")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 4. Kubernetes Operating Layer
class InfraKubernetesClusterModel(Base):
    __tablename__ = "infra_clusters"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    cluster_name = Column(String(128), nullable=False, index=True)
    kubernetes_version = Column(String(32), default="1.30.2")
    provider = Column(String(32), default="EKS")  # EKS, GKE, AKS, SELF_HOSTED
    region = Column(String(32), default="us-east-1")
    total_nodes = Column(Integer, default=12)
    healthy_nodes = Column(Integer, default=12)
    total_namespaces = Column(Integer, default=8)
    workloads_count = Column(Integer, default=48)
    health_status = Column(String(32), default="HEALTHY")
    endpoint_url = Column(String(256), default="https://k8s.api.enterprise.internal")
    metrics_summary = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraKubernetesNodeModel(Base):
    __tablename__ = "infra_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    cluster_id = Column(String(36), nullable=False, index=True)
    node_name = Column(String(128), nullable=False)
    instance_type = Column(String(64), default="m6i.4xlarge")
    cpu_allocatable_cores = Column(Float, default=16.0)
    cpu_allocated_cores = Column(Float, default=10.2)
    memory_allocatable_gb = Column(Float, default=64.0)
    memory_allocated_gb = Column(Float, default=44.8)
    pod_capacity = Column(Integer, default=110)
    pods_running = Column(Integer, default=62)
    ready = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraKubernetesWorkloadModel(Base):
    __tablename__ = "infra_workloads"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    cluster_id = Column(String(36), nullable=False, index=True)
    namespace = Column(String(64), nullable=False, default="production")
    name = Column(String(128), nullable=False)
    workload_type = Column(String(32), default="DEPLOYMENT")  # DEPLOYMENT, STATEFULSET, DAEMONSET
    desired_replicas = Column(Integer, default=3)
    available_replicas = Column(Integer, default=3)
    image_tag = Column(String(256), default="ghcr.io/uzaii/core-service:v4.2.1")
    cpu_request = Column(String(32), default="500m")
    memory_request = Column(String(32), default="1Gi")
    hpa_enabled = Column(Boolean, default=True)
    health_status = Column(String(32), default="HEALTHY")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraKubernetesPodModel(Base):
    __tablename__ = "infra_pods"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    workload_id = Column(String(36), nullable=False, index=True)
    pod_name = Column(String(128), nullable=False)
    node_name = Column(String(128), nullable=False)
    phase = Column(String(32), default="RUNNING")  # RUNNING, PENDING, FAILED
    restart_count = Column(Integer, default=0)
    ip_address = Column(String(64), default="10.244.2.14")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 5. Scaling, Capacity, GPU
class InfraScalingPolicyModel(Base):
    __tablename__ = "infra_scaling_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    target_resource_id = Column(String(36), nullable=False, index=True)
    policy_name = Column(String(128), nullable=False)
    min_replicas = Column(Integer, default=2)
    max_replicas = Column(Integer, default=20)
    target_cpu_utilization = Column(Float, default=70.0)
    target_memory_utilization = Column(Float, default=80.0)
    scale_in_cooldown_seconds = Column(Integer, default=300)
    scale_out_cooldown_seconds = Column(Integer, default=60)
    requires_approval = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraScalingEventModel(Base):
    __tablename__ = "infra_scaling_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    policy_id = Column(String(36), nullable=False, index=True)
    direction = Column(String(16), default="SCALE_OUT")  # SCALE_OUT, SCALE_IN
    previous_replicas = Column(Integer, default=3)
    new_replicas = Column(Integer, default=6)
    trigger_signal = Column(String(128), default="CPU_THRESHOLD_EXCEEDED")
    cost_impact_monthly_usd = Column(Float, default=85.0)
    status = Column(String(32), default="COMPLETED")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraCapacityForecastModel(Base):
    __tablename__ = "infra_capacity_forecasts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    resource_type = Column(String(64), default="CPU_CORES")
    forecast_horizon_days = Column(Integer, default=90)
    current_capacity = Column(Float, default=192.0)
    forecasted_demand = Column(Float, default=240.0)
    headroom_percentage = Column(Float, default=18.5)
    exhaustion_risk = Column(String(32), default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    recommended_procurement = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraGpuWorkloadModel(Base):
    __tablename__ = "infra_gpu_workloads"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    workload_name = Column(String(128), nullable=False)
    gpu_type = Column(String(64), default="NVIDIA_H100_SXM5")  # A100, H100, L4, T4
    gpu_count = Column(Integer, default=4)
    vram_allocated_gb = Column(Float, default=320.0)
    gpu_utilization_pct = Column(Float, default=78.2)
    workload_priority = Column(String(32), default="HIGH")  # BATCH, INFERENCE, TRAINING
    cost_per_hour_usd = Column(Float, default=14.80)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 6. FinOps, Budgets, Cost Anomalies & Savings
class InfraCostAllocationModel(Base):
    __tablename__ = "infra_cost_allocations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    cost_center = Column(String(64), nullable=False, default="PLATFORM_ENG")
    service_name = Column(String(128), nullable=False, default="core-api")
    team = Column(String(64), nullable=False, default="Core Team")
    amount_usd = Column(Float, nullable=False, default=1250.0)
    billing_period = Column(String(16), default="2026-09")
    unit_metric = Column(String(64), default="COST_PER_TRANSACTION")
    unit_cost_usd = Column(Float, default=0.00042)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraBudgetModel(Base):
    __tablename__ = "infra_budgets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    name = Column(String(128), nullable=False)
    monthly_limit_usd = Column(Float, nullable=False, default=15000.0)
    actual_spend_usd = Column(Float, nullable=False, default=9420.0)
    forecast_spend_usd = Column(Float, nullable=False, default=13800.0)
    alert_threshold_pct = Column(Float, default=80.0)
    status = Column(String(32), default="HEALTHY")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraCostAnomalyModel(Base):
    __tablename__ = "infra_cost_anomalies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    service_name = Column(String(128), nullable=False)
    anomaly_detected_at = Column(DateTime(timezone=True), default=utc_now)
    baseline_spend_usd = Column(Float, default=120.0)
    actual_spike_usd = Column(Float, default=850.0)
    deviation_factor = Column(Float, default=7.08)
    driver = Column(String(256), default="Cross-region S3 egress replication burst")
    status = Column(String(32), default="RESOLVED")


class InfraSavingsOpportunityModel(Base):
    __tablename__ = "infra_savings"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    category = Column(String(64), default="RIGHTSIZING")  # RIGHTSIZING, IDLE_RESOURCES, RESERVED_SAVINGS
    title = Column(String(256), nullable=False)
    resource_id = Column(String(64), nullable=False)
    estimated_monthly_savings_usd = Column(Float, default=240.0)
    risk_level = Column(String(32), default="LOW")
    status = Column(String(32), default="IDENTIFIED")  # IDENTIFIED, APPROVED, APPLIED, REJECTED
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 7. Drift, Change Management & Maintenance
class InfraConfigurationDriftModel(Base):
    __tablename__ = "infra_drift"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    resource_id = Column(String(36), nullable=False, index=True)
    expected_state = Column(JSON, nullable=False, default=dict)
    actual_state = Column(JSON, nullable=False, default=dict)
    drift_severity = Column(String(32), default="MEDIUM")
    is_critical_security_drift = Column(Boolean, default=False)
    remediation_proposal = Column(Text, nullable=True)
    status = Column(String(32), default="DETECTED")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraChangeRequestModel(Base):
    __tablename__ = "infra_changes"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    title = Column(String(256), nullable=False)
    reason = Column(Text, nullable=False)
    risk_score = Column(String(32), default="MEDIUM")
    blast_radius_resources = Column(JSON, default=list)
    cost_delta_usd = Column(Float, default=0.0)
    rollback_plan = Column(Text, nullable=False)
    approval_status = Column(String(32), default="PENDING_APPROVAL")  # PENDING, APPROVED, REJECTED
    approved_by = Column(String(128), nullable=True)
    execution_status = Column(String(32), default="PENDING")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 8. Disaster Recovery & Backup Validation
class InfraBackupValidationModel(Base):
    __tablename__ = "infra_restore_tests"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    resource_id = Column(String(36), nullable=False, index=True)
    backup_snapshot_id = Column(String(128), nullable=False)
    checksum_verified = Column(Boolean, default=True)
    restore_duration_seconds = Column(Float, default=142.0)
    rpo_met = Column(Boolean, default=True)
    rto_met = Column(Boolean, default=True)
    status = Column(String(32), default="PASSED")
    tested_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraDisasterRecoveryPlanModel(Base):
    __tablename__ = "infra_dr_plans"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    plan_name = Column(String(128), nullable=False)
    target_rpo_minutes = Column(Integer, default=15)
    target_rto_minutes = Column(Integer, default=60)
    primary_region = Column(String(32), default="us-east-1")
    failover_region = Column(String(32), default="us-west-2")
    active_replication = Column(Boolean, default=True)
    last_drill_status = Column(String(32), default="SUCCESS")
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


# 9. AI Infrastructure Agents, Approvals & Auditing
class InfraAgentRunModel(Base):
    __tablename__ = "infra_agent_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    agent_name = Column(String(64), nullable=False, index=True)
    task_type = Column(String(64), nullable=False)
    resources_inspected = Column(JSON, default=list)
    findings_count = Column(Integer, default=0)
    actions_proposed = Column(JSON, default=list)
    status = Column(String(32), default="COMPLETED")
    duration_ms = Column(Integer, default=450)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraAgentApprovalModel(Base):
    __tablename__ = "infra_agent_approvals"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    agent_id = Column(String(64), nullable=False)
    action_type = Column(String(64), nullable=False)
    target_resource = Column(String(128), nullable=False)
    blast_radius_summary = Column(Text, nullable=False)
    decision = Column(String(32), default="PENDING")  # PENDING, APPROVED, REJECTED
    approver = Column(String(128), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class InfraAuditEventModel(Base):
    __tablename__ = "infra_audit_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(36), primary_key=True, default=generate_uuid)
    tenant_id = Column(String(64), nullable=False, index=True, default="default_tenant")
    actor_id = Column(String(128), nullable=False)
    action = Column(String(64), nullable=False)
    resource_id = Column(String(128), nullable=False)
    previous_state = Column(JSON, nullable=True)
    new_state = Column(JSON, nullable=True)
    cryptographic_digest = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
