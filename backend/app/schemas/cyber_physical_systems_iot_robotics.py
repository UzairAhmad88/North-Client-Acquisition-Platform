"""
Phase 70: Cyber-Physical Systems, IoT, Robotics Infrastructure, Digital Twins & Real-World Operations Schemas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# 1. Facilities & Zones
class CpsFacilityCreate(BaseModel):
    facility_code: str
    name: str
    facility_type: str = "FACTORY"
    location_id: Optional[str] = None
    total_area_sqm: float = 10000.0


class CpsFacilityResponse(BaseModel):
    id: str
    facility_code: str
    name: str
    facility_type: str
    total_area_sqm: float
    operating_status: str
    emergency_stop_engaged: bool


class CpsZoneResponse(BaseModel):
    id: str
    facility_id: str
    zone_code: str
    name: str
    safety_tier: str
    max_human_occupancy: int
    current_occupancy: int
    restricted_access: bool


# 2. Physical Assets
class CpsAssetCreate(BaseModel):
    asset_tag: str
    name: str
    asset_type: str
    facility_id: str
    zone_id: Optional[str] = None
    manufacturer: Optional[str] = None
    criticality_rating: str = "HIGH"


class CpsAssetResponse(BaseModel):
    id: str
    asset_tag: str
    name: str
    asset_type: str
    facility_id: str
    zone_id: Optional[str] = None
    criticality_rating: str
    operating_state: str
    health_score: float


# 3. IoT Devices & Shadow
class CpsDeviceCreate(BaseModel):
    device_uid: str
    name: str
    device_type: str = "PLC_GATEWAY"
    asset_id: Optional[str] = None
    connectivity_protocol: str = "MQTT"


class CpsDeviceResponse(BaseModel):
    id: str
    device_uid: str
    name: str
    device_type: str
    connectivity_protocol: str
    connection_state: str
    firmware_version: str


class CpsDeviceShadowResponse(BaseModel):
    device_id: str
    reported_state: Dict[str, Any]
    desired_state: Dict[str, Any]
    state_delta: Dict[str, Any]
    has_drift: bool
    version: int


# 4. Sensors & Telemetry
class CpsSensorResponse(BaseModel):
    id: str
    sensor_code: str
    device_id: str
    asset_id: Optional[str] = None
    sensor_type: str
    measurement_unit: str
    sampling_rate_hz: float
    calibration_status: str
    health_verdict: str


class CpsSensorReadingResponse(BaseModel):
    sensor_id: str
    asset_id: Optional[str] = None
    value: float
    quality_score: float
    quality_flag: str
    recorded_at: datetime


# 5. Actuators & Commands
class CpsActuatorResponse(BaseModel):
    id: str
    actuator_code: str
    device_id: str
    actuator_type: str
    min_safe_range: float
    max_safe_range: float
    current_position: float
    status: str


class CpsCommandCreate(BaseModel):
    idempotency_key: str
    target_asset_id: Optional[str] = None
    target_actuator_id: Optional[str] = None
    command_action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    dry_run: bool = True


class CpsCommandResponse(BaseModel):
    id: str
    idempotency_key: str
    command_action: str
    safety_check_passed: bool
    requires_human_approval: bool
    approval_status: str
    execution_status: str


# 6. Robotics & Fleets
class CpsRobotResponse(BaseModel):
    id: str
    robot_code: str
    name: str
    robot_type: str
    facility_id: str
    battery_charge_pct: float
    operational_state: str
    safety_zone_clear: bool


class CpsRobotMissionCreate(BaseModel):
    mission_code: str
    robot_id: str
    mission_type: str
    priority: str = "MEDIUM"
    start_zone_id: Optional[str] = None
    target_zone_id: Optional[str] = None


class CpsRobotMissionResponse(BaseModel):
    id: str
    mission_code: str
    robot_id: str
    mission_type: str
    priority: str
    status: str
    progress_pct: float


# 7. Machines & Maintenance
class CpsMachineHealthResponse(BaseModel):
    asset_id: str
    overall_equipment_effectiveness: float  # OEE
    availability_pct: float
    performance_pct: float
    quality_pct: float
    vibration_velocity_rms_mm_s: float
    bearing_temperature_celsius: float
    failure_probability_30d: float
    predicted_remaining_useful_life_hours: float
    health_verdict: str


class CpsMaintenanceWorkOrderCreate(BaseModel):
    work_order_code: str
    asset_id: str
    maintenance_type: str = "PREDICTIVE"
    priority: str = "MEDIUM"
    assigned_technician: Optional[str] = None
    estimated_downtime_hours: float = 2.0


class CpsMaintenanceWorkOrderResponse(BaseModel):
    id: str
    work_order_code: str
    asset_id: str
    maintenance_type: str
    priority: str
    status: str
    estimated_downtime_hours: float


# 8. Digital Twins & What-If Simulations
class CpsDigitalTwinResponse(BaseModel):
    id: str
    twin_code: str
    asset_id: str
    twin_version: str
    synchronization_status: str
    sync_latency_ms: float


class CpsSimulationRunRequest(BaseModel):
    twin_id: str
    scenario_type: str = "PEAK_OVERLOAD"
    dry_run: bool = True


class CpsSimulationRunResponse(BaseModel):
    simulation_code: str
    twin_id: str
    scenario_type: str
    predicted_downtime_hours: float
    projected_risk_score: float
    recommendations: List[str]


# 9. Safety, Emergency & Command Center
class CpsSafetyPolicyResponse(BaseModel):
    id: str
    policy_code: str
    name: str
    target_asset_type: str
    rule_type: str
    enforcement_action: str
    is_active: bool


class CpsSafetyEventResponse(BaseModel):
    id: str
    event_code: str
    facility_id: str
    severity: str
    event_type: str
    description: str
    resolution_status: str


class CpsCommandCenterSummaryResponse(BaseModel):
    physical_assets_count: int
    iot_devices_online_count: int
    robot_fleet_active_count: int
    average_oee_pct: float
    active_safety_events_count: int
    emergency_stop_engaged: bool
    overall_facility_health_score: float
    active_cps_agents_count: int
