"""
FastAPI Router for Phase 69: Global Infrastructure, Data Center, Edge Computing & Planet-Scale Reliability.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.services.global_infrastructure.service import AutonomousGlobalInfrastructureService
from app.schemas.global_infrastructure_planet_scale_reliability import (
    GlobalLocationResponse,
    GlobalRegionResponse,
    GlobalDataCenterResponse,
    GlobalRackResponse,
    GlobalHardwareHealthResponse,
    GlobalEdgeLocationResponse,
    GlobalEdgeNodeResponse,
    GlobalDeviceFleetResponse,
    GlobalNetworkPathResponse,
    GlobalTrafficMetricResponse,
    GlobalRoutingPolicyResponse,
    GlobalDnsZoneResponse,
    GlobalCdnEdgeResponse,
    GlobalServiceTopologyResponse,
    GlobalLatencyTelemetryResponse,
    GlobalCapacityResponse,
    GlobalWorkloadPlacementResponse,
    GlobalWorkloadMigrationResponse,
    GlobalReplicationStateResponse,
    GlobalDisasterRecoveryPlanResponse,
    GlobalChaosExperimentResponse,
    GlobalDigitalTwinResponse,
    GlobalCommandCenterSummaryResponse,
    GlobalOperatingCycleResponse,
)

router = APIRouter(prefix="/global-infrastructure", tags=["Global Infrastructure & Planet-Scale Reliability"])


def get_global_infra_service() -> AutonomousGlobalInfrastructureService:
    return AutonomousGlobalInfrastructureService()


@router.get("/summary", response_model=GlobalCommandCenterSummaryResponse)
def get_command_center_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Provides enterprise planetary telemetry for the Command Center."""
    return service.get_command_center_summary(tenant_id=tenant_id)


@router.get("/health")
def get_planetary_health(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets composite global and regional health scores."""
    return service.global_health.get_global_health_score(tenant_id=tenant_id)


@router.get("/locations", response_model=List[GlobalLocationResponse])
def list_locations(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists geographical presence and data center location hubs."""
    return service.locations.list_locations(tenant_id=tenant_id)


@router.get("/regions", response_model=List[GlobalRegionResponse])
def list_regions(
    provider: str = Query("ALL"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists multi-cloud regional presence and inter-region latency ratings."""
    return service.regions.list_regions(provider=provider, tenant_id=tenant_id)


@router.get("/availability-zones")
def list_availability_zones(
    region_code: str = Query("us-east-1"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists availability zones and facility redundancy within a region."""
    return service.availability_zones.list_availability_zones(region_code=region_code)


@router.get("/data-centers", response_model=List[GlobalDataCenterResponse])
def list_data_centers(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists physical data centers, power capacities, and cooling loads."""
    return service.data_centers.list_data_centers(tenant_id=tenant_id)


@router.get("/data-centers/pue")
def get_data_center_pue(
    dc_code: str = Query("DC-IAD-01"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets Power Usage Effectiveness (PUE) and thermal efficiency ratings."""
    return service.data_centers.get_pue_telemetry(dc_code=dc_code)


@router.get("/racks", response_model=List[GlobalRackResponse])
def list_racks(
    dc_id: str = Query("dc_iad_01"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists server racks, U-allocations, and temperature telemetry."""
    return service.racks.list_racks(dc_id=dc_id)


@router.get("/hardware")
def list_hardware(
    rack_id: Optional[str] = Query(None),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists bare-metal servers, CPUs, RAM, and storage inventory."""
    return service.hardware.list_hardware_assets(rack_id=rack_id)


@router.get("/hardware/health", response_model=GlobalHardwareHealthResponse)
def get_hardware_health(
    asset_id: str = Query("hw_srv_01"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets predictive failure telemetry and SMART indicators for hardware assets."""
    return service.hardware_health.get_hardware_health(asset_id=asset_id)


@router.get("/edge/locations", response_model=List[GlobalEdgeLocationResponse])
def list_edge_locations(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists distributed edge POPs and metro latency performance."""
    return service.edge.list_edge_locations(tenant_id=tenant_id)


@router.get("/edge/nodes", response_model=List[GlobalEdgeNodeResponse])
def list_edge_nodes(
    edge_code: str = Query("EDGE-LHR-01"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists edge compute nodes, offline queues, and connectivity status."""
    return service.edge.list_edge_nodes(edge_code=edge_code)


@router.get("/device-fleets", response_model=List[GlobalDeviceFleetResponse])
def list_device_fleets(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists IoT gateways, sensors, and branch device fleets."""
    return service.device_fleet.list_fleets(tenant_id=tenant_id)


@router.get("/network-paths", response_model=List[GlobalNetworkPathResponse])
def list_network_paths(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Audits inter-region transit circuits, packet loss, and RTT latencies."""
    return service.network_paths.list_network_paths(tenant_id=tenant_id)


@router.get("/traffic")
def get_traffic_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets planetary traffic throughput, request volumes, and continent splits."""
    return service.traffic.get_planetary_traffic_summary(tenant_id=tenant_id)


@router.get("/routing-policies", response_model=List[GlobalRoutingPolicyResponse])
def list_routing_policies(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Lists dynamic traffic routing policies, geo-fences, and failover thresholds."""
    return service.routing.list_routing_policies(tenant_id=tenant_id)


@router.get("/dns")
def get_dns_fleet(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets global Anycast DNS fleet status and resolution latencies."""
    return service.dns.get_dns_fleet_status(tenant_id=tenant_id)


@router.get("/cdn")
def get_cdn_metrics(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets CDN cache hit ratios and origin shield telemetry."""
    return service.cdn.get_cdn_metrics(tenant_id=tenant_id)


@router.get("/service-topology", response_model=List[GlobalServiceTopologyResponse])
def get_service_topology(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets distributed cross-region service dependency topology."""
    return service.service_topology.get_cross_region_topology(tenant_id=tenant_id)


@router.get("/latency")
def get_latency_matrix(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets empirical p50, p95, and p99 planetary latency telemetry."""
    return service.latency.get_latency_matrix(tenant_id=tenant_id)


@router.get("/replication")
def get_database_replication(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets cross-region database replication streams and sync lag."""
    return service.replication.get_database_replication_status(tenant_id=tenant_id)


@router.get("/capacity")
def get_planetary_capacity(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets planetary capacity, headroom percentage, and exhaustion horizons."""
    return service.capacity.get_planetary_capacity(tenant_id=tenant_id)


@router.post("/placement/recommend", response_model=GlobalWorkloadPlacementResponse)
def recommend_workload_placement(
    workload_name: str = Query("core-api"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Recommends 7-factor optimal workload placement across regions and edge."""
    return service.placement.recommend_placement(workload_name=workload_name, tenant_id=tenant_id)


@router.post("/migration/plan", response_model=GlobalWorkloadMigrationResponse)
def plan_workload_migration(
    source_region: str = Query("us-east-1"),
    destination_region: str = Query("eu-west-1"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Plans zero-downtime cross-region migration with risk assessment."""
    return service.migration.plan_migration(source_region=source_region, destination_region=destination_region, tenant_id=tenant_id)


@router.get("/disaster-recovery")
def get_global_dr_readiness(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Gets planetary disaster recovery readiness scores and verified RPO/RTO."""
    return service.disaster_recovery.validate_global_dr(tenant_id=tenant_id)


@router.post("/chaos/experiment", response_model=GlobalChaosExperimentResponse)
def run_chaos_experiment(
    fault_type: str = Query("PACKET_LOSS"),
    target_region: str = Query("eu-west-1"),
    dry_run: bool = Query(True),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Executes safe, blast-radius-bounded planetary chaos experiment."""
    return service.chaos.run_chaos_experiment(fault_type=fault_type, target_region=target_region, dry_run=dry_run)


@router.post("/digital-twin/simulate")
def simulate_digital_twin_scenario(
    scenario_type: str = Query("DATACENTER_OUTAGE"),
    target: str = Query("DC-IAD-01"),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Simulates hypothetical failure scenarios in the digital twin."""
    return service.simulation.simulate_failure_scenario(scenario_type=scenario_type, target=target)


@router.post("/cycle/run", response_model=GlobalOperatingCycleResponse)
def run_planet_scale_operating_cycle(
    tenant_id: str = Query("default_tenant"),
    dry_run: bool = Query(True),
    service: AutonomousGlobalInfrastructureService = Depends(get_global_infra_service)
):
    """Executes the closed-loop 12-stage planetary operating cycle."""
    return service.run_planet_scale_operating_cycle(tenant_id=tenant_id, dry_run=dry_run)
