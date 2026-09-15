"""
Phase 69: Autonomous Data Center, Edge Computing, Global Infrastructure,
Distributed Systems Intelligence & Planet-Scale Reliability Models.
"""

from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Text,
)
try:
    from app.models.base import Base
except ImportError:
    from backend.app.models.base import Base


class GlobalLocationModel(Base):
    """Geographical location registry for data centers, edge POPs, and regional hubs."""
    __tablename__ = "global_locations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    country_code = Column(String(8), nullable=False, index=True)
    country_name = Column(String(128), nullable=False)
    state_province = Column(String(128), nullable=True)
    city = Column(String(128), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    compliance_zone = Column(String(64), nullable=False, default="GLOBAL_GENERAL")
    time_zone = Column(String(64), nullable=False, default="UTC")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalRegionModel(Base):
    """Global multi-cloud regional presence and inter-region network meshes."""
    __tablename__ = "global_regions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    provider = Column(String(64), nullable=False, index=True)  # AWS, GCP, AZURE, EQUINIX, ONPREM
    region_code = Column(String(64), nullable=False, index=True)  # us-east-1, europe-west1, etc.
    display_name = Column(String(128), nullable=False)
    location_id = Column(String(64), nullable=True, index=True)
    availability_zones_count = Column(Integer, nullable=False, default=3)
    latency_score_ms = Column(Float, nullable=False, default=15.0)
    health_status = Column(String(32), nullable=False, default="HEALTHY")
    data_residency_jurisdiction = Column(String(64), nullable=False, default="STANDARD")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalDataCenterModel(Base):
    """Physical data center facilities, power ratings, cooling, and environmental metrics."""
    __tablename__ = "global_data_centers"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    data_center_code = Column(String(64), nullable=False, unique=True, index=True)
    facility_name = Column(String(128), nullable=False)
    location_id = Column(String(64), nullable=True, index=True)
    provider = Column(String(64), nullable=False, default="COLOCATION")
    total_power_capacity_kw = Column(Float, nullable=False, default=2500.0)
    current_power_usage_kw = Column(Float, nullable=False, default=1450.0)
    power_usage_effectiveness = Column(Float, nullable=False, default=1.18)  # PUE
    cooling_capacity_tons = Column(Float, nullable=False, default=700.0)
    average_ambient_temp_celsius = Column(Float, nullable=False, default=21.5)
    rack_count = Column(Integer, nullable=False, default=120)
    health_status = Column(String(32), nullable=False, default="HEALTHY")
    security_tier = Column(String(32), nullable=False, default="TIER_3")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalRackModel(Base):
    """Data center server racks, power distribution units, and thermal sensors."""
    __tablename__ = "global_racks"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    data_center_id = Column(String(64), nullable=False, index=True)
    rack_identifier = Column(String(64), nullable=False, index=True)
    u_height = Column(Integer, nullable=False, default=42)
    allocated_u = Column(Integer, nullable=False, default=28)
    max_power_draw_kw = Column(Float, nullable=False, default=15.0)
    current_power_draw_kw = Column(Float, nullable=False, default=8.2)
    top_temperature_celsius = Column(Float, nullable=False, default=23.4)
    bottom_temperature_celsius = Column(Float, nullable=False, default=19.8)
    health_state = Column(String(32), nullable=False, default="NORMAL")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalHardwareAssetModel(Base):
    """Bare-metal physical servers, mainboards, CPU sockets, and NIC fabrics."""
    __tablename__ = "global_hardware_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    rack_id = Column(String(64), nullable=True, index=True)
    serial_number = Column(String(128), nullable=False, unique=True, index=True)
    asset_tag = Column(String(64), nullable=False, index=True)
    model_name = Column(String(128), nullable=False)
    vendor = Column(String(64), nullable=False)  # Dell, HPE, Supermicro, Cisco
    cpu_model = Column(String(128), nullable=False)
    cpu_cores_total = Column(Integer, nullable=False, default=64)
    memory_total_gb = Column(Float, nullable=False, default=256.0)
    storage_total_tb = Column(Float, nullable=False, default=32.0)
    nic_speed_gbps = Column(Float, nullable=False, default=100.0)
    firmware_version = Column(String(64), nullable=False, default="v2.18.4")
    lifecycle_phase = Column(String(32), nullable=False, default="OPERATIONAL")
    warranty_expiration = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalHardwareHealthModel(Base):
    """Predictive failure telemetry, SMART indicators, and thermals."""
    __tablename__ = "global_hardware_health"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    hardware_asset_id = Column(String(64), nullable=False, index=True)
    cpu_temp_celsius = Column(Float, nullable=False, default=54.2)
    fan_speed_rpm = Column(Integer, nullable=False, default=4200)
    disk_smart_reallocated_sectors = Column(Integer, nullable=False, default=0)
    ecc_memory_errors_corrected = Column(Integer, nullable=False, default=0)
    failure_probability_next_30d = Column(Float, nullable=False, default=0.012)
    health_verdict = Column(String(32), nullable=False, default="HEALTHY")
    last_telemetry_timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalEdgeLocationModel(Base):
    """Distributed edge Points of Presence (POPs), telecom metro hubs, and 5G edge."""
    __tablename__ = "global_edge_locations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    edge_code = Column(String(64), nullable=False, unique=True, index=True)  # EDGE-LHR-01
    metro_city = Column(String(128), nullable=False)
    country_code = Column(String(8), nullable=False)
    provider = Column(String(64), nullable=False, default="FASTLY_POP")
    latency_to_user_p95_ms = Column(Float, nullable=False, default=8.4)
    total_node_capacity = Column(Integer, nullable=False, default=16)
    active_node_count = Column(Integer, nullable=False, default=14)
    offline_capability_enabled = Column(Boolean, nullable=False, default=True)
    health_status = Column(String(32), nullable=False, default="HEALTHY")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalEdgeNodeModel(Base):
    """Edge compute nodes, Micro-K8s/K3s workers, and local acceleration units."""
    __tablename__ = "global_edge_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    edge_location_id = Column(String(64), nullable=False, index=True)
    node_name = Column(String(128), nullable=False, index=True)
    cpu_cores = Column(Integer, nullable=False, default=16)
    memory_gb = Column(Float, nullable=False, default=64.0)
    nvme_storage_gb = Column(Float, nullable=False, default=1000.0)
    is_connected = Column(Boolean, nullable=False, default=True)
    queued_offline_events_count = Column(Integer, nullable=False, default=0)
    sync_status = Column(String(32), nullable=False, default="IN_SYNC")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalEdgeWorkloadModel(Base):
    """Containerized edge microservices, wasm workloads, and local inference models."""
    __tablename__ = "global_edge_workloads"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    edge_node_id = Column(String(64), nullable=False, index=True)
    workload_name = Column(String(128), nullable=False, index=True)
    image_digest = Column(String(128), nullable=False)
    replica_count = Column(Integer, nullable=False, default=2)
    local_storage_mode = Column(String(32), nullable=False, default="TRANSIENT")
    health_state = Column(String(32), nullable=False, default="HEALTHY")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalDeviceFleetModel(Base):
    """IoT devices, branch gateways, and point-of-sale terminal infrastructure."""
    __tablename__ = "global_device_fleets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    fleet_name = Column(String(128), nullable=False, index=True)
    device_type = Column(String(64), nullable=False)  # GATEWAY, SENSOR, KIOSK, CAMERA
    total_devices = Column(Integer, nullable=False, default=2500)
    active_devices = Column(Integer, nullable=False, default=2480)
    firmware_version_target = Column(String(64), nullable=False, default="v3.4.1")
    compliance_percentage = Column(Float, nullable=False, default=99.2)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalDeviceUpdateModel(Base):
    """Over-The-Air (OTA) firmware campaigns with canary progressive delivery."""
    __tablename__ = "global_device_updates"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    fleet_id = Column(String(64), nullable=False, index=True)
    release_version = Column(String(64), nullable=False)
    canary_percentage = Column(Float, nullable=False, default=5.0)
    success_rate_percentage = Column(Float, nullable=False, default=99.8)
    rollout_state = Column(String(32), nullable=False, default="CANARY_VERIFIED")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalNetworkPathModel(Base):
    """Inter-region backbone transits, SD-WAN fabrics, and direct connect circuits."""
    __tablename__ = "global_network_paths"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_region_id = Column(String(64), nullable=False, index=True)
    target_region_id = Column(String(64), nullable=False, index=True)
    circuit_type = Column(String(64), nullable=False, default="DIRECT_CONNECT")
    bandwidth_capacity_gbps = Column(Float, nullable=False, default=100.0)
    current_utilization_pct = Column(Float, nullable=False, default=48.2)
    rtt_latency_ms = Column(Float, nullable=False, default=68.4)
    packet_loss_rate = Column(Float, nullable=False, default=0.0001)
    status = Column(String(32), nullable=False, default="OPTIMAL")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalTrafficMetricModel(Base):
    """Live planetary ingress and egress telemetry per continent and protocol."""
    __tablename__ = "global_traffic_metrics"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    continent_code = Column(String(8), nullable=False, index=True)  # NA, EU, AP, SA, AF
    requests_per_second = Column(Float, nullable=False, default=45000.0)
    throughput_gbps = Column(Float, nullable=False, default=18.5)
    http_2xx_ratio = Column(Float, nullable=False, default=0.994)
    http_5xx_ratio = Column(Float, nullable=False, default=0.0008)
    recorded_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalRoutingPolicyModel(Base):
    """Policy-driven traffic routing, latency-based steering, and geo-fencing."""
    __tablename__ = "global_routing_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    policy_name = Column(String(128), nullable=False, index=True)
    routing_strategy = Column(String(64), nullable=False, default="LATENCY_OPTIMIZED")  # GEO, WEIGHTED, FAILOVER
    weights_json = Column(JSON, nullable=True)
    failover_threshold_ms = Column(Float, nullable=False, default=250.0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalDnsZoneModel(Base):
    """Global Anycast DNS authority, failover health monitors, and TTL rules."""
    __tablename__ = "global_dns_zones"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    domain_name = Column(String(128), nullable=False, unique=True, index=True)
    record_count = Column(Integer, nullable=False, default=48)
    anycast_pop_count = Column(Integer, nullable=False, default=320)
    health_probe_status = Column(String(32), nullable=False, default="ALL_PASSING")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalCdnEdgeModel(Base):
    """Planetary CDN distribution, origin shielding, and cache offload ratios."""
    __tablename__ = "global_cdn_edges"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    cdn_distribution_id = Column(String(64), nullable=False, index=True)
    origin_domain = Column(String(128), nullable=False)
    cache_hit_ratio_pct = Column(Float, nullable=False, default=94.6)
    bandwidth_saved_tb_monthly = Column(Float, nullable=False, default=145.0)
    origin_protection_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalServiceTopologyModel(Base):
    """Cross-region distributed service call graphs and dependency matrices."""
    __tablename__ = "global_service_topologies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    upstream_service = Column(String(128), nullable=False, index=True)
    downstream_service = Column(String(128), nullable=False, index=True)
    cross_region_call = Column(Boolean, nullable=False, default=False)
    source_region = Column(String(64), nullable=False, default="us-east-1")
    target_region = Column(String(64), nullable=False, default="eu-west-1")
    average_rtt_ms = Column(Float, nullable=False, default=74.0)
    call_frequency_per_sec = Column(Float, nullable=False, default=1200.0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalLatencyTelemetryModel(Base):
    """Empirical p50, p95, and p99 latency telemetry across the globe."""
    __tablename__ = "global_latency_telemetry"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    source_continent = Column(String(8), nullable=False)
    target_continent = Column(String(8), nullable=False)
    p50_latency_ms = Column(Float, nullable=False, default=24.5)
    p95_latency_ms = Column(Float, nullable=False, default=68.2)
    p99_latency_ms = Column(Float, nullable=False, default=112.4)
    measured_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalCapacityModel(Base):
    """Multi-region planetary capacity planning and headroom tracking."""
    __tablename__ = "global_capacity"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    region_id = Column(String(64), nullable=False, index=True)
    resource_category = Column(String(64), nullable=False, default="COMPUTE_CPU")
    total_capacity = Column(Float, nullable=False, default=10000.0)
    allocated_capacity = Column(Float, nullable=False, default=6800.0)
    headroom_percentage = Column(Float, nullable=False, default=32.0)
    exhaustion_horizon_days = Column(Integer, nullable=False, default=118)
    risk_state = Column(String(32), nullable=False, default="LOW_RISK")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalWorkloadPlacementModel(Base):
    """7-factor multi-objective workload placement decisions."""
    __tablename__ = "global_workload_placements"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    workload_id = Column(String(128), nullable=False, index=True)
    recommended_region = Column(String(64), nullable=False)
    recommended_edge_hub = Column(String(64), nullable=True)
    latency_score = Column(Float, nullable=False, default=0.94)
    carbon_intensity_score = Column(Float, nullable=False, default=0.88)
    cost_efficiency_score = Column(Float, nullable=False, default=0.91)
    status = Column(String(32), nullable=False, default="COMMITTED")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalWorkloadMigrationModel(Base):
    """Cross-region live workload and database migration plans."""
    __tablename__ = "global_workload_migrations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    migration_title = Column(String(128), nullable=False)
    source_region = Column(String(64), nullable=False)
    destination_region = Column(String(64), nullable=False)
    estimated_downtime_seconds = Column(Float, nullable=False, default=0.0)  # Zero-downtime
    data_transfer_gb = Column(Float, nullable=False, default=450.0)
    approval_state = Column(String(32), nullable=False, default="SIMULATED_PENDING_APPROVAL")
    executed_by = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalReplicationStateModel(Base):
    """Cross-region database replication streams, consensus, and lag tracking."""
    __tablename__ = "global_replication_states"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    database_cluster_name = Column(String(128), nullable=False, index=True)
    primary_region = Column(String(64), nullable=False)
    replica_region = Column(String(64), nullable=False)
    replication_lag_ms = Column(Float, nullable=False, default=14.2)
    data_consistency_model = Column(String(64), nullable=False, default="BOUNDED_STALENESS")
    synchronization_health = Column(String(32), nullable=False, default="HEALTHY")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalPartitionEventModel(Base):
    """Network partition detection, split-brain mitigation, and quorum telemetry."""
    __tablename__ = "global_partition_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    isolated_region_code = Column(String(64), nullable=False, index=True)
    partition_detected_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    quorum_preserved = Column(Boolean, nullable=False, default=True)
    automated_fence_applied = Column(Boolean, nullable=False, default=True)
    resolution_status = Column(String(32), nullable=False, default="RESOLVED")


class GlobalDisasterRecoveryPlanModel(Base):
    """Planet-scale disaster recovery runbooks, multi-region RTO/RPO targets."""
    __tablename__ = "global_disaster_recovery_plans"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    plan_name = Column(String(128), nullable=False, index=True)
    primary_dc_or_region = Column(String(64), nullable=False)
    secondary_dc_or_region = Column(String(64), nullable=False)
    target_rpo_seconds = Column(Integer, nullable=False, default=30)
    target_rto_seconds = Column(Integer, nullable=False, default=300)
    verified_rpo_seconds = Column(Integer, nullable=False, default=18)
    verified_rto_seconds = Column(Integer, nullable=False, default=184)
    readiness_score = Column(Float, nullable=False, default=98.5)
    last_drill_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalFailoverEventModel(Base):
    """Planetary failover execution records and traffic evacuation checkpoints."""
    __tablename__ = "global_failover_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    dr_plan_id = Column(String(64), nullable=False, index=True)
    evacuated_region = Column(String(64), nullable=False)
    receiving_region = Column(String(64), nullable=False)
    traffic_diverted_percentage = Column(Float, nullable=False, default=100.0)
    failover_status = Column(String(32), nullable=False, default="COMPLETED")
    authorized_by = Column(String(128), nullable=False)
    initiated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)


class GlobalChaosExperimentModel(Base):
    """Controlled planetary chaos engineering: packet loss, latency, and AZ outage injection."""
    __tablename__ = "global_chaos_experiments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    experiment_name = Column(String(128), nullable=False, index=True)
    fault_type = Column(String(64), nullable=False)  # PACKET_LOSS, LATENCY_SPIKE, AZ_BLACKHOLE
    target_region = Column(String(64), nullable=False)
    blast_radius_limit_pct = Column(Float, nullable=False, default=5.0)
    duration_seconds = Column(Integer, nullable=False, default=120)
    automatic_abort_triggered = Column(Boolean, nullable=False, default=False)
    outcome_status = Column(String(32), nullable=False, default="VERIFIED_RESILIENT")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalIncidentRecordModel(Base):
    """Global incident command, severity classification, and cross-team triage."""
    __tablename__ = "global_incident_records"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    incident_code = Column(String(64), nullable=False, unique=True, index=True)
    severity = Column(String(16), nullable=False, default="SEV2")  # SEV1 to SEV4
    title = Column(String(256), nullable=False)
    affected_regions_json = Column(JSON, nullable=False)
    incident_commander = Column(String(128), nullable=False)
    current_status = Column(String(32), nullable=False, default="STABILIZED")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalRootCauseAnalysisModel(Base):
    """Postmortem timelines, dependency chain hypotheses, and systemic lessons."""
    __tablename__ = "global_root_cause_analysis"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    incident_id = Column(String(64), nullable=False, index=True)
    root_cause_hypothesis = Column(Text, nullable=False)
    confidence_level = Column(Float, nullable=False, default=0.92)
    contributing_factors_json = Column(JSON, nullable=True)
    preventative_actions_json = Column(JSON, nullable=True)
    verification_status = Column(String(32), nullable=False, default="CONFIRMED_BY_SRE")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalDigitalTwinModel(Base):
    """Planet-scale infrastructure digital twin and what-if simulation scenarios."""
    __tablename__ = "global_digital_twins"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    scenario_title = Column(String(128), nullable=False)
    scenario_type = Column(String(64), nullable=False)  # REGION_FAILURE, TRAFFIC_DOUBLING, GPU_SURGE
    simulated_impact_summary = Column(Text, nullable=False)
    estimated_capacity_deficit_pct = Column(Float, nullable=False, default=0.0)
    projected_additional_cost_usd = Column(Float, nullable=False, default=1200.0)
    recommendation = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class GlobalAuditEventModel(Base):
    """Tamper-evident audit trail for all planetary operations and agent actions."""
    __tablename__ = "global_audit_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    actor_id = Column(String(128), nullable=False, index=True)
    actor_role = Column(String(64), nullable=False)
    action_type = Column(String(64), nullable=False, index=True)
    target_entity = Column(String(128), nullable=False)
    impact_tier = Column(String(32), nullable=False, default="HIGH_IMPACT")
    audit_payload = Column(JSON, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
