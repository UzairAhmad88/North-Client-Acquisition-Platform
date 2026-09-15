"""
Phase 81: Enterprise IT Service Management, IT Operations, Observability, Infrastructure Intelligence, AIOps, Incident Automation & Autonomous IT Operations Models.
Zero-collision namespace and extend_existing=True for maximum compatibility with existing tables.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid

from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, Base


# --- SERVICES & PORTFOLIO ---
class ItServiceModel(BaseModel):
    """Governed Enterprise Services Catalog."""
    __tablename__ = "it_services"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    business_owner = Column(String(255), nullable=False)
    technical_owner = Column(String(255), nullable=False)
    criticality = Column(String(32), default="TIER_1", nullable=False)  # TIER_1, TIER_2, TIER_3
    availability_target = Column(Float, default=99.99, nullable=False)
    status = Column(String(32), default="OPERATIONAL", nullable=False)  # OPERATIONAL, DEGRADED, PARTIAL_OUTAGE, MAJOR_OUTAGE
    monthly_cost_usd = Column(Float, default=0.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItServiceDependencyModel(BaseModel):
    """Service-to-service and Service-to-Infrastructure dependencies."""
    __tablename__ = "it_service_dependencies"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), nullable=False, index=True)
    depends_on_code = Column(String(128), nullable=False, index=True)
    dependency_type = Column(String(64), default="HARD", nullable=False)  # HARD, SOFT, ASYNCHRONOUS
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItServiceOwnerModel(BaseModel):
    """Service ownership registry."""
    __tablename__ = "it_service_owners"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), nullable=False, index=True)
    owner_email = Column(String(255), nullable=False)
    role = Column(String(64), default="TECHNICAL_LEAD", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItServiceCatalogModel(BaseModel):
    """Searchable Service Catalog."""
    __tablename__ = "it_service_catalog"
    __table_args__ = {"extend_existing": True}

    item_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False)  # APPLICATION, INFRASTRUCTURE, CLOUD, DATABASE, NETWORK, SECURITY
    description = Column(Text, nullable=True)
    sla_hours = Column(Float, default=4.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItServiceLevelModel(BaseModel):
    """Service level definitions."""
    __tablename__ = "it_service_levels"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), nullable=False, index=True)
    target_name = Column(String(128), nullable=False)
    target_value = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItServiceSloModel(BaseModel):
    """SLOs tied to services."""
    __tablename__ = "it_service_slos"
    __table_args__ = {"extend_existing": True}

    slo_code = Column(String(128), unique=True, nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    target_pct = Column(Float, default=99.9, nullable=False)
    current_pct = Column(Float, default=99.95, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- CMDB & IT ASSET MANAGEMENT ---
class ItAssetModel(BaseModel):
    """Hardware & Software IT Assets."""
    __tablename__ = "it_assets"
    __table_args__ = {"extend_existing": True}

    asset_tag = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    asset_type = Column(String(64), nullable=False)  # SERVER, VM, CONTAINER, DATABASE, NETWORK_DEVICE, LAPTOP
    environment = Column(String(32), default="PRODUCTION", nullable=False)
    status = Column(String(32), default="IN_USE", nullable=False)
    owner = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAssetLifecycleModel(BaseModel):
    """Procurement to Retirement lifecycle tracking."""
    __tablename__ = "it_asset_lifecycle"
    __table_args__ = {"extend_existing": True}

    asset_tag = Column(String(128), nullable=False, index=True)
    phase = Column(String(32), default="OPERATIONAL", nullable=False)  # PROCUREMENT, PROVISIONED, OPERATIONAL, RETIRED
    acquired_date = Column(DateTime(timezone=True), nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAssetLicenseModel(BaseModel):
    """Software License tracking."""
    __tablename__ = "it_asset_licenses"
    __table_args__ = {"extend_existing": True}

    license_code = Column(String(128), unique=True, nullable=False, index=True)
    software_name = Column(String(255), nullable=False)
    total_seats = Column(Integer, default=100, nullable=False)
    allocated_seats = Column(Integer, default=64, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItConfigurationItemModel(BaseModel):
    """CMDB Configuration Items (CIs)."""
    __tablename__ = "it_configuration_items"
    __table_args__ = {"extend_existing": True}

    ci_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    ci_type = Column(String(64), nullable=False)  # HOST, SERVICE, DATABASE, CLOUD_RES, APP
    environment = Column(String(32), default="PRODUCTION", nullable=False)
    version = Column(String(32), default="1.0.0", nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItConfigurationVersionModel(BaseModel):
    """CMDB state versions."""
    __tablename__ = "it_configuration_versions"
    __table_args__ = {"extend_existing": True}

    ci_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    config_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItConfigurationRelationshipModel(BaseModel):
    """CMDB Relationship Graph."""
    __tablename__ = "it_configuration_relationships"
    __table_args__ = {"extend_existing": True}

    parent_ci = Column(String(128), nullable=False, index=True)
    child_ci = Column(String(128), nullable=False, index=True)
    relationship_type = Column(String(64), default="RUNS_ON", nullable=False)  # RUNS_ON, DEPENDS_ON, CONNECTS_TO
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- INFRASTRUCTURE & MULTI-CLOUD ---
class ItInfrastructureModel(BaseModel):
    """Servers, VMs, Clusters state."""
    __tablename__ = "it_infrastructure"
    __table_args__ = {"extend_existing": True}

    infra_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    infra_type = Column(String(64), nullable=False)  # KUBERNETES_CLUSTER, PHYSICAL_HOST, CLOUD_VM
    region = Column(String(64), nullable=False)
    cpu_usage_pct = Column(Float, default=42.0, nullable=False)
    memory_usage_pct = Column(Float, default=58.0, nullable=False)
    status = Column(String(32), default="HEALTHY", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItCloudResourceModel(BaseModel):
    """Multi-cloud resources."""
    __tablename__ = "it_cloud_resources"
    __table_args__ = {"extend_existing": True}

    resource_id_str = Column(String(255), unique=True, nullable=False, index=True)
    provider = Column(String(32), nullable=False)  # AWS, GCP, AZURE
    resource_type = Column(String(64), nullable=False)
    region = Column(String(64), nullable=False)
    status = Column(String(32), default="RUNNING", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItNetworkDeviceModel(BaseModel):
    """Routers, Switches, Firewalls state."""
    __tablename__ = "it_network_devices"
    __table_args__ = {"extend_existing": True}

    device_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    device_type = Column(String(64), nullable=False)
    latency_ms = Column(Float, default=2.4, nullable=False)
    packet_loss_pct = Column(Float, default=0.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItDatabaseModel(BaseModel):
    """Databases operational state."""
    __tablename__ = "it_databases"
    __table_args__ = {"extend_existing": True}

    db_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    engine = Column(String(64), nullable=False)  # POSTGRES, MYSQL, ORACLE, MONGO
    active_connections = Column(Integer, default=42, nullable=False)
    replication_lag_sec = Column(Float, default=0.0, nullable=False)
    status = Column(String(32), default="HEALTHY", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItApplicationModel(BaseModel):
    """Application instances operational health."""
    __tablename__ = "it_applications"
    __table_args__ = {"extend_existing": True}

    app_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    error_rate_pct = Column(Float, default=0.02, nullable=False)
    avg_response_ms = Column(Float, default=48.5, nullable=False)
    throughput_rps = Column(Float, default=1240.0, nullable=False)
    status = Column(String(32), default="HEALTHY", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItEndpointModel(BaseModel):
    """Endpoint operations state."""
    __tablename__ = "it_endpoints"
    __table_args__ = {"extend_existing": True}

    endpoint_code = Column(String(128), unique=True, nullable=False, index=True)
    os_name = Column(String(64), nullable=False)
    patch_status = Column(String(32), default="UP_TO_DATE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- OBSERVABILITY (METRICS, LOGS, TRACES, APM) ---
class ItMetricModel(BaseModel):
    """Infrastructure & Operational Telemetry Metrics."""
    __tablename__ = "it_metrics"
    __table_args__ = {"extend_existing": True}

    metric_name = Column(String(128), nullable=False, index=True)
    resource_id_str = Column(String(128), nullable=False, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItLogModel(BaseModel):
    """Operational Logs."""
    __tablename__ = "it_logs"
    __table_args__ = {"extend_existing": True}

    log_id_str = Column(String(128), unique=True, nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    level = Column(String(16), default="INFO", nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItTraceModel(BaseModel):
    """Distributed Traces."""
    __tablename__ = "it_traces"
    __table_args__ = {"extend_existing": True}

    trace_id_str = Column(String(128), unique=True, nullable=False, index=True)
    span_id_str = Column(String(128), nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    duration_ms = Column(Float, nullable=False)
    has_error = Column(Boolean, default=False, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItEventModel(BaseModel):
    """Operational Events."""
    __tablename__ = "it_events"
    __table_args__ = {"extend_existing": True}

    event_code = Column(String(128), unique=True, nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    source = Column(String(128), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItSyntheticTestModel(BaseModel):
    """Synthetic API / Web monitoring tests."""
    __tablename__ = "it_synthetic_tests"
    __table_args__ = {"extend_existing": True}

    test_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    target_url = Column(String(255), nullable=False)
    passed = Column(Boolean, default=True, nullable=False)
    response_ms = Column(Float, default=120.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRumEventModel(BaseModel):
    """Real User Monitoring (RUM) Telemetry."""
    __tablename__ = "it_rum_events"
    __table_args__ = {"extend_existing": True}

    rum_event_id = Column(String(128), unique=True, nullable=False, index=True)
    page_load_ms = Column(Float, default=320.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- INCIDENTS, PROBLEMS & CHANGES ---
class ItIncidentModel(BaseModel):
    """IT Operations Incidents."""
    __tablename__ = "it_incidents"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    severity = Column(String(32), default="P2_HIGH", nullable=False)  # P1_CRITICAL, P2_HIGH, P3_MEDIUM, P4_LOW
    service_code = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="INVESTIGATING", nullable=False)  # OPEN, INVESTIGATING, MITIGATED, RESOLVED
    assigned_team = Column(String(128), nullable=False)
    root_cause = Column(Text, nullable=True)
    summary = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItIncidentEventModel(BaseModel):
    """Events in incident history."""
    __tablename__ = "it_incident_events"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), nullable=False, index=True)
    event_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    description = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItIncidentServiceModel(BaseModel):
    """Affected services in incident."""
    __tablename__ = "it_incident_services"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItIncidentTimelineModel(BaseModel):
    """Auditable incident timeline."""
    __tablename__ = "it_incident_timeline"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), nullable=False, index=True)
    phase = Column(String(32), nullable=False)  # DETECTION, ALERT, TRIAGE, MITIGATION, RECOVERY, POSTMORTEM
    notes = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItIncidentResponderModel(BaseModel):
    """Incident responders assignment."""
    __tablename__ = "it_incident_responders"
    __table_args__ = {"extend_existing": True}

    incident_code = Column(String(64), nullable=False, index=True)
    responder_email = Column(String(255), nullable=False)
    role = Column(String(64), default="COMMANDER", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItIncidentActionModel(BaseModel):
    """Remediation actions taken."""
    __tablename__ = "it_incident_actions"
    __table_args__ = {"extend_existing": True}

    action_code = Column(String(128), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItProblemModel(BaseModel):
    """Problem Management tracking."""
    __tablename__ = "it_problems"
    __table_args__ = {"extend_existing": True}

    problem_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    root_cause = Column(Text, nullable=False)
    workaround = Column(Text, nullable=True)
    status = Column(String(32), default="UNDER_INVESTIGATION", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItKnownErrorModel(BaseModel):
    """Known Error Database (KEDB)."""
    __tablename__ = "it_known_errors"
    __table_args__ = {"extend_existing": True}

    kedb_code = Column(String(64), unique=True, nullable=False, index=True)
    symptoms = Column(Text, nullable=False)
    workaround = Column(Text, nullable=False)
    resolution = Column(Text, nullable=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItProblemIncidentModel(BaseModel):
    """Problem to Incidents link."""
    __tablename__ = "it_problem_incidents"
    __table_args__ = {"extend_existing": True}

    problem_code = Column(String(64), nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItChangeModel(BaseModel):
    """Change Requests Management."""
    __tablename__ = "it_changes"
    __table_args__ = {"extend_existing": True}

    change_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    change_type = Column(String(32), default="NORMAL", nullable=False)  # STANDARD, NORMAL, EMERGENCY
    service_code = Column(String(128), nullable=False, index=True)
    risk_level = Column(String(32), default="MEDIUM", nullable=False)
    scheduled_start = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(32), default="APPROVED", nullable=False)  # DRAFT, SUBMITTED, APPROVED, IMPLEMENTED, ROLLED_BACK
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItChangeApprovalModel(BaseModel):
    """Change approvals log."""
    __tablename__ = "it_change_approvals"
    __table_args__ = {"extend_existing": True}

    change_code = Column(String(64), nullable=False, index=True)
    approver_email = Column(String(255), nullable=False)
    status = Column(String(32), default="APPROVED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItChangeCalendarModel(BaseModel):
    """Change calendar schedule."""
    __tablename__ = "it_change_calendar"
    __table_args__ = {"extend_existing": True}

    change_code = Column(String(64), nullable=False, index=True)
    maintenance_window = Column(String(128), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItChangeRiskModel(BaseModel):
    """Calculated change risk metrics."""
    __tablename__ = "it_change_risks"
    __table_args__ = {"extend_existing": True}

    change_code = Column(String(64), nullable=False, index=True)
    risk_score = Column(Float, default=25.0, nullable=False)
    collision_warning = Column(Boolean, default=False, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItChangeDependencyModel(BaseModel):
    """Change dependencies."""
    __tablename__ = "it_change_dependencies"
    __table_args__ = {"extend_existing": True}

    change_code = Column(String(64), nullable=False, index=True)
    depends_on_change = Column(String(64), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- RELEASES, RUNBOOKS & SLOs ---
class ItReleaseModel(BaseModel):
    """Release Management tracking."""
    __tablename__ = "it_releases"
    __table_args__ = {"extend_existing": True}

    release_code = Column(String(64), unique=True, nullable=False, index=True)
    version = Column(String(32), nullable=False)
    service_code = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="DEPLOYED", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItDeploymentModel(BaseModel):
    """Deployments tracking (Canary, Blue-Green)."""
    __tablename__ = "it_deployments"
    __table_args__ = {"extend_existing": True}

    deploy_code = Column(String(128), unique=True, nullable=False, index=True)
    release_code = Column(String(64), nullable=False, index=True)
    strategy = Column(String(32), default="CANARY", nullable=False)  # CANARY, BLUE_GREEN, ROLLING
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItDeploymentHealthModel(BaseModel):
    """Deployment health checks."""
    __tablename__ = "it_deployment_health"
    __table_args__ = {"extend_existing": True}

    deploy_code = Column(String(128), nullable=False, index=True)
    passed = Column(Boolean, default=True, nullable=False)
    error_rate = Column(Float, default=0.001, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItDeploymentRollbackModel(BaseModel):
    """Automated rollback state."""
    __tablename__ = "it_deployment_rollbacks"
    __table_args__ = {"extend_existing": True}

    deploy_code = Column(String(128), unique=True, nullable=False, index=True)
    previous_release = Column(String(64), nullable=False)
    status = Column(String(32), default="READY", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItConfigurationModel(BaseModel):
    """Configuration management."""
    __tablename__ = "it_configurations"
    __table_args__ = {"extend_existing": True}

    config_code = Column(String(128), unique=True, nullable=False, index=True)
    desired_state = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItConfigurationBaselineModel(BaseModel):
    """Approved configuration baselines."""
    __tablename__ = "it_configuration_baselines"
    __table_args__ = {"extend_existing": True}

    baseline_code = Column(String(128), unique=True, nullable=False, index=True)
    rules_json = Column(JSON, default=dict, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItConfigurationDriftModel(BaseModel):
    """Configuration drift detection."""
    __tablename__ = "it_configuration_drift"
    __table_args__ = {"extend_existing": True}

    drift_code = Column(String(128), unique=True, nullable=False, index=True)
    ci_code = Column(String(128), nullable=False, index=True)
    details = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRunbookModel(BaseModel):
    """Runbook Automation library."""
    __tablename__ = "it_runbooks"
    __table_args__ = {"extend_existing": True}

    runbook_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    autonomy_level = Column(String(16), default="L3", nullable=False)  # L0 to L5
    is_reversible = Column(Boolean, default=True, nullable=False)
    status = Column(String(32), default="ACTIVE", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRunbookVersionModel(BaseModel):
    """Runbook versions."""
    __tablename__ = "it_runbook_versions"
    __table_args__ = {"extend_existing": True}

    runbook_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    steps_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRunbookStepModel(BaseModel):
    """Individual runbook step."""
    __tablename__ = "it_runbook_steps"
    __table_args__ = {"extend_existing": True}

    runbook_code = Column(String(128), nullable=False, index=True)
    step_number = Column(Integer, nullable=False)
    step_name = Column(String(128), nullable=False)
    command = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRunbookExecutionModel(BaseModel):
    """Runbook execution log."""
    __tablename__ = "it_runbook_executions"
    __table_args__ = {"extend_existing": True}

    execution_code = Column(String(128), unique=True, nullable=False, index=True)
    runbook_code = Column(String(128), nullable=False, index=True)
    status = Column(String(32), default="SUCCESS", nullable=False)
    executed_by = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItSloModel(BaseModel):
    """SRE Service Level Objectives."""
    __tablename__ = "it_slos"
    __table_args__ = {"extend_existing": True}

    slo_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    service_code = Column(String(128), nullable=False, index=True)
    target_pct = Column(Float, default=99.9, nullable=False)
    window_days = Column(Integer, default=30, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItSliModel(BaseModel):
    """Service Level Indicators."""
    __tablename__ = "it_slis"
    __table_args__ = {"extend_existing": True}

    sli_code = Column(String(128), unique=True, nullable=False, index=True)
    metric_name = Column(String(128), nullable=False)
    current_value = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItErrorBudgetModel(BaseModel):
    """SRE Error Budgets management."""
    __tablename__ = "it_error_budgets"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), primary_key=True)
    allowed_downtime_mins = Column(Float, default=43.2, nullable=False)
    consumed_downtime_mins = Column(Float, default=4.5, nullable=False)
    remaining_budget_pct = Column(Float, default=89.6, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItBurnRateModel(BaseModel):
    """Error budget burn rates."""
    __tablename__ = "it_burn_rates"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), nullable=False, index=True)
    burn_rate_1h = Column(Float, default=0.5, nullable=False)
    burn_rate_6h = Column(Float, default=0.8, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- CAPACITY, PERFORMANCE, VENDORS & SERVICE DESK ---
class ItCapacityMetricModel(BaseModel):
    """Capacity utilization tracking."""
    __tablename__ = "it_capacity_metrics"
    __table_args__ = {"extend_existing": True}

    resource_id_str = Column(String(128), nullable=False, index=True)
    resource_type = Column(String(64), nullable=False)
    current_pct = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItCapacityForecastModel(BaseModel):
    """Capacity depletion forecasting."""
    __tablename__ = "it_capacity_forecasts"
    __table_args__ = {"extend_existing": True}

    resource_id_str = Column(String(128), nullable=False, index=True)
    exhaustion_date = Column(DateTime(timezone=True), nullable=False)
    recommended_action = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAvailabilityMetricModel(BaseModel):
    """Uptime / Downtime metrics."""
    __tablename__ = "it_availability_metrics"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), nullable=False, index=True)
    uptime_pct = Column(Float, default=99.98, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItPerformanceMetricModel(BaseModel):
    """Performance metrics (Latency, RPS)."""
    __tablename__ = "it_performance_metrics"
    __table_args__ = {"extend_existing": True}

    service_code = Column(String(128), nullable=False, index=True)
    p95_latency_ms = Column(Float, default=45.2, nullable=False)
    p99_latency_ms = Column(Float, default=120.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItVendorServiceModel(BaseModel):
    """Third-party SaaS/Cloud Vendors."""
    __tablename__ = "it_vendor_services"
    __table_args__ = {"extend_existing": True}

    vendor_code = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(32), default="OPERATIONAL", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItVendorIncidentModel(BaseModel):
    """Third-party vendor incidents."""
    __tablename__ = "it_vendor_incidents"
    __table_args__ = {"extend_existing": True}

    vendor_code = Column(String(128), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItVendorSlaModel(BaseModel):
    """Vendor contract SLAs."""
    __tablename__ = "it_vendor_slas"
    __table_args__ = {"extend_existing": True}

    vendor_code = Column(String(128), nullable=False, index=True)
    agreed_uptime = Column(Float, default=99.9, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItTicketModel(BaseModel):
    """IT Service Desk Tickets."""
    __tablename__ = "it_tickets"
    __table_args__ = {"extend_existing": True}

    ticket_code = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False)  # SERVICE_REQUEST, INCIDENT, HARDWARE, ACCESS
    requester = Column(String(255), nullable=False)
    priority = Column(String(32), default="MEDIUM", nullable=False)
    status = Column(String(32), default="OPEN", nullable=False)  # OPEN, IN_PROGRESS, RESOLVED, CLOSED
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItTicketCommentModel(BaseModel):
    """Ticket updates and comments."""
    __tablename__ = "it_ticket_comments"
    __table_args__ = {"extend_existing": True}

    ticket_code = Column(String(64), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    comment = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItTicketAssignmentModel(BaseModel):
    """Ticket routing assignments."""
    __tablename__ = "it_ticket_assignments"
    __table_args__ = {"extend_existing": True}

    ticket_code = Column(String(64), nullable=False, index=True)
    assignee = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItTicketSlaModel(BaseModel):
    """Service desk SLA tracking."""
    __tablename__ = "it_ticket_slas"
    __table_args__ = {"extend_existing": True}

    ticket_code = Column(String(64), nullable=False, index=True)
    response_sla_hours = Column(Float, default=1.0, nullable=False)
    resolution_sla_hours = Column(Float, default=8.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItTicketEscalationModel(BaseModel):
    """Ticket escalation tracking."""
    __tablename__ = "it_ticket_escalations"
    __table_args__ = {"extend_existing": True}

    ticket_code = Column(String(64), nullable=False, index=True)
    escalated_to = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


# --- KNOWLEDGE, FINOPS, DR & POSTMORTEMS ---
class ItKnowledgeModel(BaseModel):
    """IT Operations Knowledge Base."""
    __tablename__ = "it_knowledge"
    __table_args__ = {"extend_existing": True}

    article_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(64), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItKnowledgeVersionModel(BaseModel):
    """Knowledge article versions."""
    __tablename__ = "it_knowledge_versions"
    __table_args__ = {"extend_existing": True}

    article_code = Column(String(128), nullable=False, index=True)
    version = Column(String(32), nullable=False)
    content = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItKnowledgeLinkModel(BaseModel):
    """Knowledge to Incident/Runbook links."""
    __tablename__ = "it_knowledge_links"
    __table_args__ = {"extend_existing": True}

    article_code = Column(String(128), nullable=False, index=True)
    linked_code = Column(String(128), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAgentPermissionModel(BaseModel):
    """IT Agent tool permissions."""
    __tablename__ = "it_agent_permissions"
    __table_args__ = {"extend_existing": True}

    agent_id = Column(String(128), nullable=False, index=True)
    tool_name = Column(String(128), nullable=False)
    autonomy_level = Column(String(16), default="L3", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAgentTaskModel(BaseModel):
    """IT Agent tasks."""
    __tablename__ = "it_agent_tasks"
    __table_args__ = {"extend_existing": True}

    task_code = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAgentActionModel(BaseModel):
    """IT Agent executed actions."""
    __tablename__ = "it_agent_actions"
    __table_args__ = {"extend_existing": True}

    action_code = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    action_type = Column(String(64), nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAgentRunModel(BaseModel):
    """IT Agent run history."""
    __tablename__ = "it_agent_runs"
    __table_args__ = {"extend_existing": True}

    run_code = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAgentApprovalModel(BaseModel):
    """Human approvals for IT Agent actions."""
    __tablename__ = "it_agent_approvals"
    __table_args__ = {"extend_existing": True}

    approval_code = Column(String(128), unique=True, nullable=False, index=True)
    agent_id = Column(String(128), nullable=False, index=True)
    approved_by = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItCostModel(BaseModel):
    """IT FinOps Cost tracking."""
    __tablename__ = "it_costs"
    __table_args__ = {"extend_existing": True}

    cost_code = Column(String(128), unique=True, nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    monthly_usd = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItCostAnomalyModel(BaseModel):
    """Cost spike anomalies."""
    __tablename__ = "it_cost_anomalies"
    __table_args__ = {"extend_existing": True}

    anomaly_code = Column(String(128), unique=True, nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    excess_cost_usd = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItUnitEconomicsModel(BaseModel):
    """Unit Economics (Cost / User / Transaction)."""
    __tablename__ = "it_unit_economics"
    __table_args__ = {"extend_existing": True}

    metric_name = Column(String(128), primary_key=True)
    cost_per_unit = Column(Float, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItBackupModel(BaseModel):
    """Backup & Disaster Recovery tracking."""
    __tablename__ = "it_backups"
    __table_args__ = {"extend_existing": True}

    backup_code = Column(String(128), unique=True, nullable=False, index=True)
    target_service = Column(String(128), nullable=False, index=True)
    rpo_minutes = Column(Integer, default=15, nullable=False)
    rto_minutes = Column(Integer, default=60, nullable=False)
    status = Column(String(32), default="SUCCESS", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRestoreTestModel(BaseModel):
    """Automated restore verification tests."""
    __tablename__ = "it_restore_tests"
    __table_args__ = {"extend_existing": True}

    test_code = Column(String(128), unique=True, nullable=False, index=True)
    passed = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItDrTestModel(BaseModel):
    """Disaster Recovery Exercises."""
    __tablename__ = "it_dr_tests"
    __table_args__ = {"extend_existing": True}

    test_code = Column(String(128), unique=True, nullable=False, index=True)
    exercise_name = Column(String(255), nullable=False)
    passed = Column(Boolean, default=True, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItRecoveryPlanModel(BaseModel):
    """Disaster Recovery Plans."""
    __tablename__ = "it_recovery_plans"
    __table_args__ = {"extend_existing": True}

    plan_code = Column(String(128), unique=True, nullable=False, index=True)
    service_code = Column(String(128), nullable=False, index=True)
    steps_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItPostmortemModel(BaseModel):
    """Structured Blameless Postmortems."""
    __tablename__ = "it_postmortems"
    __table_args__ = {"extend_existing": True}

    postmortem_code = Column(String(64), unique=True, nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=False)
    what_went_well = Column(Text, nullable=True)
    what_failed = Column(Text, nullable=True)
    action_items_json = Column(JSON, default=list, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItPostmortemActionModel(BaseModel):
    """Corrective action items from postmortems."""
    __tablename__ = "it_postmortem_actions"
    __table_args__ = {"extend_existing": True}

    action_code = Column(String(128), unique=True, nullable=False, index=True)
    postmortem_code = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=False)
    assignee = Column(String(255), nullable=False)
    status = Column(String(32), default="OPEN", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItReliabilityFindingModel(BaseModel):
    """SRE reliability findings."""
    __tablename__ = "it_reliability_findings"
    __table_args__ = {"extend_existing": True}

    finding_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItToilTaskModel(BaseModel):
    """SRE Toil Measurement & Tracking."""
    __tablename__ = "it_toil_tasks"
    __table_args__ = {"extend_existing": True}

    task_code = Column(String(128), unique=True, nullable=False, index=True)
    task_name = Column(String(255), nullable=False)
    hours_per_month = Column(Float, default=18.5, nullable=False)
    automation_potential = Column(String(32), default="HIGH", nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAutomationOpportunityModel(BaseModel):
    """Identified automation ROI opportunities."""
    __tablename__ = "it_automation_opportunities"
    __table_args__ = {"extend_existing": True}

    opp_code = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    est_hours_saved_monthly = Column(Float, default=45.0, nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)


class ItAuditEventModel(BaseModel):
    """Tamper-evident IT Operations Audit Log."""
    __tablename__ = "it_audit_events"
    __table_args__ = {"extend_existing": True}

    audit_code = Column(String(128), unique=True, nullable=False, index=True)
    actor_email = Column(String(255), nullable=False, index=True)
    action = Column(String(128), nullable=False)
    target = Column(String(255), nullable=False)
    tenant_id = Column(String(64), default="tenant-default", nullable=False, index=True)
