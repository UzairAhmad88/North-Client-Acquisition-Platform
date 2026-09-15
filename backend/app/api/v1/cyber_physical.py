"""
FastAPI Router for Phase 70: Autonomous Cyber-Physical Systems, IoT, Robotics & Digital Twins.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.services.cyber_physical.service import AutonomousCyberPhysicalService
from app.schemas.cyber_physical_systems_iot_robotics import (
    CpsFacilityResponse,
    CpsZoneResponse,
    CpsAssetResponse,
    CpsDeviceResponse,
    CpsDeviceShadowResponse,
    CpsSensorResponse,
    CpsActuatorResponse,
    CpsCommandResponse,
    CpsRobotResponse,
    CpsRobotMissionResponse,
    CpsMachineHealthResponse,
    CpsMaintenanceWorkOrderResponse,
    CpsDigitalTwinResponse,
    CpsSafetyPolicyResponse,
    CpsSafetyEventResponse,
    CpsCommandCenterSummaryResponse,
)

router = APIRouter(prefix="/cyber-physical", tags=["Autonomous Cyber-Physical Systems & Robotics"])


def get_cps_service() -> AutonomousCyberPhysicalService:
    return AutonomousCyberPhysicalService()


@router.get("/summary", response_model=CpsCommandCenterSummaryResponse)
def get_command_center_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Provides executive telemetry for the Cyber-Physical Command Center."""
    return service.get_command_center_summary(tenant_id=tenant_id)


@router.post("/operating-cycle/run")
def run_operating_cycle(
    dry_run: bool = Query(True),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Executes the closed-loop 12-stage cyber-physical operating cycle."""
    return service.run_cyber_physical_operating_cycle(tenant_id=tenant_id, dry_run=dry_run)


@router.get("/facilities", response_model=List[CpsFacilityResponse])
def list_facilities(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists smart factories and industrial facilities."""
    return service.facilities.list_facilities(tenant_id=tenant_id)


@router.get("/zones", response_model=List[CpsZoneResponse])
def list_zones(
    facility_id: str = Query("fac_detroit_01"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists safety tiers and occupancy zones in a facility."""
    return service.zones.list_zones(facility_id=facility_id)


@router.get("/assets", response_model=List[CpsAssetResponse])
def list_assets(
    facility_id: Optional[str] = Query(None),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists physical industrial machines, robotics, and assets."""
    return service.assets.list_assets(facility_id=facility_id, tenant_id=tenant_id)


@router.get("/devices", response_model=List[CpsDeviceResponse])
def list_devices(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists IoT gateways, PLCs, and embedded edge controllers."""
    return service.devices.list_devices(tenant_id=tenant_id)


@router.get("/devices/{device_id}/shadow", response_model=CpsDeviceShadowResponse)
def get_device_shadow(
    device_id: str,
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Gets reported state, desired state, and delta drift for an IoT device."""
    return service.device_shadow.get_shadow(device_id=device_id)


@router.get("/sensors", response_model=List[CpsSensorResponse])
def list_sensors(
    asset_id: Optional[str] = Query(None),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists physical sensors and calibration health statuses."""
    return service.sensors.list_sensors(asset_id=asset_id, tenant_id=tenant_id)


@router.get("/actuators", response_model=List[CpsActuatorResponse])
def list_actuators(
    asset_id: Optional[str] = Query(None),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists physical actuators, valves, servos, and allowed safety ranges."""
    return service.actuators.list_actuators(asset_id=asset_id)


@router.post("/commands/execute", response_model=CpsCommandResponse)
def issue_physical_command(
    idempotency_key: str = Query(...),
    command_action: str = Query(...),
    dry_run: bool = Query(True),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Issues a policy-validated physical actuation command."""
    return service.commands.issue_command(
        idempotency_key=idempotency_key,
        command_action=command_action,
        parameters={"dry_run": dry_run},
        dry_run=dry_run,
        tenant_id=tenant_id
    )


@router.get("/robots", response_model=List[CpsRobotResponse])
def list_robots(
    facility_id: str = Query("fac_detroit_01"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists AMRs and robotic arms in the facility fleet."""
    return service.robots.list_robots(facility_id=facility_id, tenant_id=tenant_id)


@router.get("/robot-fleet/telemetry")
def get_robot_fleet_telemetry(
    facility_id: str = Query("fac_detroit_01"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Gets real-time robotics fleet availability and battery telemetry."""
    return service.robot_fleet.get_fleet_telemetry(facility_id=facility_id)


@router.post("/missions/dispatch", response_model=CpsRobotMissionResponse)
def dispatch_robot_mission(
    mission_code: str = Query(...),
    robot_id: str = Query(...),
    mission_type: str = Query("MATERIAL_TRANSPORT"),
    priority: str = Query("MEDIUM"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Dispatches a robotics task mission within a facility."""
    return service.robot_missions.create_mission(
        mission_code=mission_code,
        robot_id=robot_id,
        mission_type=mission_type,
        priority=priority,
        tenant_id=tenant_id
    )


@router.get("/machines/health/{asset_id}", response_model=CpsMachineHealthResponse)
def get_machine_health(
    asset_id: str,
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Retrieves industrial machine health, vibration RMS, and OEE."""
    return service.machine_health.get_machine_health(asset_id=asset_id)


@router.post("/maintenance/work-orders", response_model=CpsMaintenanceWorkOrderResponse)
def create_maintenance_work_order(
    work_order_code: str = Query(...),
    asset_id: str = Query(...),
    maintenance_type: str = Query("PREDICTIVE"),
    priority: str = Query("MEDIUM"),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Creates a predictive or corrective maintenance work order."""
    return service.work_orders.create_work_order(
        work_order_code=work_order_code,
        asset_id=asset_id,
        maintenance_type=maintenance_type,
        priority=priority,
        tenant_id=tenant_id
    )


@router.get("/digital-twins/{asset_id}", response_model=CpsDigitalTwinResponse)
def get_digital_twin(
    asset_id: str,
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Gets the synchronized digital twin state for a physical asset."""
    return service.digital_twins.get_twin_state(asset_id=asset_id)


@router.post("/simulations/run")
def run_twin_simulation(
    twin_id: str = Query("twin_arm_01"),
    scenario_type: str = Query("PEAK_OVERLOAD"),
    dry_run: bool = Query(True),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Executes a sandboxed physical stress simulation on a digital twin."""
    return service.simulation.run_simulation(twin_id=twin_id, scenario_type=scenario_type, dry_run=dry_run)


@router.get("/safety/policies", response_model=List[CpsSafetyPolicyResponse])
def list_safety_policies(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists hard-boundary physical safety policies and interlocks."""
    return service.safety.list_safety_policies(tenant_id=tenant_id)


@router.get("/emergency/status")
def get_emergency_status(
    facility_id: str = Query("fac_detroit_01"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Checks facility emergency stop and safety interlock state."""
    return service.emergency.check_emergency_state(facility_id=facility_id)


@router.get("/energy/metrics")
def get_energy_metrics(
    facility_id: str = Query("fac_detroit_01"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Retrieves real-time electrical power, demand, and efficiency metrics."""
    return service.energy.get_facility_energy_metrics(facility_id=facility_id)


@router.get("/environmental/metrics")
def get_environmental_metrics(
    zone_id: str = Query("zone_assembly_a"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Retrieves temperature, humidity, and air quality telemetry."""
    return service.environmental.get_environmental_status(zone_id=zone_id)


@router.get("/downtime/metrics")
def get_downtime_metrics(
    facility_id: str = Query("fac_detroit_01"),
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Retrieves planned vs unplanned downtime and financial impact."""
    return service.downtime.get_downtime_metrics(facility_id=facility_id)


@router.get("/agents")
def list_active_agents(
    service: AutonomousCyberPhysicalService = Depends(get_cps_service)
):
    """Lists registered autonomous cyber-physical AI agents."""
    return service.agents.list_active_cps_agents()
