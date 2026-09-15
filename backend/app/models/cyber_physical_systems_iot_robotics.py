"""
Phase 70: Autonomous Cyber-Physical Systems, IoT Intelligence, Robotics Infrastructure,
Digital Twins & Real-World AI Operations Models.
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


class CpsFacilityModel(Base):
    """Real-world industrial plants, smart buildings, data centers, and warehouses."""
    __tablename__ = "cps_facilities"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    facility_code = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    facility_type = Column(String(64), nullable=False, default="FACTORY")  # FACTORY, WAREHOUSE, LAB, CAMPUS
    location_id = Column(String(64), nullable=True, index=True)
    total_area_sqm = Column(Float, nullable=False, default=10000.0)
    operating_status = Column(String(32), nullable=False, default="OPERATIONAL")  # OPERATIONAL, MAINTENANCE, EVACUATED
    emergency_stop_engaged = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsZoneModel(Base):
    """Sub-areas, assembly lines, cleanrooms, and human/robot shared zones."""
    __tablename__ = "cps_zones"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    facility_id = Column(String(64), nullable=False, index=True)
    zone_code = Column(String(64), nullable=False, index=True)
    name = Column(String(128), nullable=False)
    safety_tier = Column(String(32), nullable=False, default="STANDARD")  # STANDARD, ROBOTIC_RESTRICTED, HAZARDOUS, CLEANROOM
    max_human_occupancy = Column(Integer, nullable=False, default=50)
    current_occupancy = Column(Integer, nullable=False, default=0)
    restricted_access = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsAssetModel(Base):
    """Physical machines, robotics, vehicles, HVAC, and industrial equipment."""
    __tablename__ = "cps_assets"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    asset_tag = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    asset_type = Column(String(64), nullable=False, index=True)  # ROBOT_ARM, CNC_MILL, AGV_VEHICLE, TURBINE, HVAC_CHILLER
    facility_id = Column(String(64), nullable=False, index=True)
    zone_id = Column(String(64), nullable=True, index=True)
    manufacturer = Column(String(128), nullable=True)
    model_number = Column(String(128), nullable=True)
    serial_number = Column(String(128), nullable=True)
    criticality_rating = Column(String(32), nullable=False, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    operating_state = Column(String(32), nullable=False, default="RUNNING")  # RUNNING, IDLE, MAINTENANCE, FAULTED, STOPPED
    health_score = Column(Float, nullable=False, default=98.5)
    last_telemetry_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsAssetRelationshipModel(Base):
    """Parent-child and mechanical/power dependency hierarchy between physical assets."""
    __tablename__ = "cps_asset_relationships"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    parent_asset_id = Column(String(64), nullable=False, index=True)
    child_asset_id = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(64), nullable=False, default="CONTAINS")  # CONTAINS, POWERS, FEEDS, CONTROLS
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsDeviceModel(Base):
    """IoT controllers, PLCs, smart meters, edge gateways, and industrial embedded boards."""
    __tablename__ = "cps_devices"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    device_uid = Column(String(128), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    device_type = Column(String(64), nullable=False, default="PLC_GATEWAY")  # PLC, GATEWAY, SENSOR_NODE, ACTUATOR_NODE
    asset_id = Column(String(64), nullable=True, index=True)
    connectivity_protocol = Column(String(32), nullable=False, default="MQTT")  # MQTT, OPC_UA, MODBUS, COAP, BLE
    connection_state = Column(String(32), nullable=False, default="ONLINE")  # ONLINE, OFFLINE, DEGRADED
    firmware_version = Column(String(64), nullable=False, default="v1.0.0")
    ip_address = Column(String(64), nullable=True)
    last_heartbeat = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsDeviceIdentityModel(Base):
    """Cryptographic certificates and Zero-Trust identity references for IoT hardware."""
    __tablename__ = "cps_device_identity"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    device_id = Column(String(64), nullable=False, unique=True, index=True)
    cert_fingerprint_sha256 = Column(String(64), nullable=False)
    cert_expiry = Column(DateTime, nullable=False)
    revocation_status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, REVOKED, EXPIRED
    m2m_token_hash = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsDeviceShadowModel(Base):
    """Digital state shadow tracking reported state, desired state, and delta drift."""
    __tablename__ = "cps_device_shadow"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    device_id = Column(String(64), nullable=False, unique=True, index=True)
    reported_state = Column(JSON, nullable=False, default=dict)
    desired_state = Column(JSON, nullable=False, default=dict)
    state_delta = Column(JSON, nullable=False, default=dict)
    has_drift = Column(Boolean, nullable=False, default=False)
    version = Column(Integer, nullable=False, default=1)
    last_synced_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsSensorModel(Base):
    """Sensor metadata attached to devices or physical machinery."""
    __tablename__ = "cps_sensors"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    sensor_code = Column(String(64), nullable=False, index=True)
    device_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=True, index=True)
    sensor_type = Column(String(64), nullable=False)  # VIBRATION, TEMPERATURE, PRESSURE, CURRENT, HUMIDITY, PROXIMITY
    measurement_unit = Column(String(32), nullable=False, default="CELSIUS")  # CELSIUS, MM_S, BAR, AMPS, PCT
    sampling_rate_hz = Column(Float, nullable=False, default=10.0)
    calibration_status = Column(String(32), nullable=False, default="CALIBRATED")  # CALIBRATED, DUE, OUT_OF_TOLERANCE
    health_verdict = Column(String(32), nullable=False, default="HEALTHY")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsSensorReadingModel(Base):
    """High-frequency time-series telemetry records from cyber-physical sensors."""
    __tablename__ = "cps_sensor_readings"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    sensor_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=True, index=True)
    value = Column(Float, nullable=False)
    quality_score = Column(Float, nullable=False, default=1.0)  # 0.0 to 1.0
    quality_flag = Column(String(32), nullable=False, default="VALID")  # VALID, OUTLIER, STALE, INTERPOLATED
    recorded_at = Column(DateTime, nullable=False, index=True, default=lambda: datetime.now(timezone.utc))


class CpsActuatorModel(Base):
    """Physical actuators, motors, valves, relays, and robotic joints."""
    __tablename__ = "cps_actuators"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    actuator_code = Column(String(64), nullable=False, index=True)
    device_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=True, index=True)
    actuator_type = Column(String(64), nullable=False)  # VALVE, RELAY, SERVO, HEATER, PUMP
    min_safe_range = Column(Float, nullable=False, default=0.0)
    max_safe_range = Column(Float, nullable=False, default=100.0)
    current_position = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="OPERATIONAL")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsCommandModel(Base):
    """Authorized physical command requests with idempotency keys and safety limits."""
    __tablename__ = "cps_commands"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    idempotency_key = Column(String(128), nullable=False, unique=True, index=True)
    target_asset_id = Column(String(64), nullable=True, index=True)
    target_actuator_id = Column(String(64), nullable=True, index=True)
    command_action = Column(String(64), nullable=False)  # SET_SPEED, OPEN_VALVE, DISPATCH_ROBOT, EMERGENCY_STOP
    parameters = Column(JSON, nullable=False, default=dict)
    requested_by = Column(String(64), nullable=False)
    safety_check_passed = Column(Boolean, nullable=False, default=False)
    requires_human_approval = Column(Boolean, nullable=False, default=False)
    approval_status = Column(String(32), nullable=False, default="PENDING")  # PENDING, APPROVED, REJECTED, AUTO_PASSED
    execution_status = Column(String(32), nullable=False, default="QUEUED")  # QUEUED, EXECUTING, SUCCESS, FAILED, BLOCKED
    executed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsRobotModel(Base):
    """Robotics fleet members (AMRs, robotic arms, quadrupeds, autonomous forklifts)."""
    __tablename__ = "cps_robots"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    robot_code = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    robot_type = Column(String(64), nullable=False)  # AMR, INDUSTRIAL_ARM, INSPECTION_QUADRUPED, FORKLIFT
    facility_id = Column(String(64), nullable=False, index=True)
    current_zone_id = Column(String(64), nullable=True, index=True)
    battery_charge_pct = Column(Float, nullable=False, default=100.0)
    operational_state = Column(String(32), nullable=False, default="AVAILABLE")  # AVAILABLE, BUSY, CHARGING, MAINTENANCE, EMERGENCY_STOP
    safety_zone_clear = Column(Boolean, nullable=False, default=True)
    firmware_version = Column(String(64), nullable=False, default="v2.1.0")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsRobotMissionModel(Base):
    """Autonomous robotics multi-stage missions and navigation paths."""
    __tablename__ = "cps_robot_missions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    mission_code = Column(String(64), nullable=False, index=True)
    robot_id = Column(String(64), nullable=False, index=True)
    mission_type = Column(String(64), nullable=False)  # MATERIAL_TRANSPORT, SURVEILLANCE, PALLET_PICK, WELDING
    priority = Column(String(32), nullable=False, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String(32), nullable=False, default="PENDING")  # PENDING, IN_PROGRESS, COMPLETED, ABORTED
    start_zone_id = Column(String(64), nullable=True)
    target_zone_id = Column(String(64), nullable=True)
    progress_pct = Column(Float, nullable=False, default=0.0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsMachineHealthModel(Base):
    """Industrial machinery diagnostic telemetry (vibration, thermal load, OEE)."""
    __tablename__ = "cps_machine_health"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=False, unique=True, index=True)
    overall_equipment_effectiveness = Column(Float, nullable=False, default=88.5)
    availability_pct = Column(Float, nullable=False, default=95.0)
    performance_pct = Column(Float, nullable=False, default=94.0)
    quality_pct = Column(Float, nullable=False, default=99.0)
    vibration_velocity_rms_mm_s = Column(Float, nullable=False, default=1.8)
    bearing_temperature_celsius = Column(Float, nullable=False, default=58.2)
    failure_probability_30d = Column(Float, nullable=False, default=0.015)
    predicted_remaining_useful_life_hours = Column(Float, nullable=False, default=4200.0)
    health_verdict = Column(String(32), nullable=False, default="HEALTHY")  # HEALTHY, WARNING, CRITICAL
    assessed_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsMaintenanceModel(Base):
    """Predictive and corrective maintenance schedules and work orders."""
    __tablename__ = "cps_maintenance"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    work_order_code = Column(String(64), nullable=False, unique=True, index=True)
    asset_id = Column(String(64), nullable=False, index=True)
    maintenance_type = Column(String(64), nullable=False)  # PREDICTIVE, PREVENTIVE, EMERGENCY_REPAIR
    priority = Column(String(32), nullable=False, default="MEDIUM")
    status = Column(String(32), nullable=False, default="SCHEDULED")  # SCHEDULED, IN_PROGRESS, COMPLETED, CLOSED
    assigned_technician = Column(String(128), nullable=True)
    estimated_downtime_hours = Column(Float, nullable=False, default=2.0)
    scheduled_date = Column(DateTime, nullable=False)
    completed_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsSparePartModel(Base):
    """Industrial spare parts inventory and automated restocking signals."""
    __tablename__ = "cps_spare_parts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    part_number = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    compatible_asset_type = Column(String(64), nullable=False, index=True)
    stock_quantity = Column(Integer, nullable=False, default=10)
    reorder_threshold = Column(Integer, nullable=False, default=3)
    unit_cost_usd = Column(Float, nullable=False, default=150.0)
    lead_time_days = Column(Integer, nullable=False, default=5)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsEnergyMetricModel(Base):
    """Real-time energy consumption, voltage, and peak load optimization."""
    __tablename__ = "cps_energy"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    facility_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=True, index=True)
    power_demand_kw = Column(Float, nullable=False, default=450.0)
    voltage_volts = Column(Float, nullable=False, default=480.0)
    power_factor = Column(Float, nullable=False, default=0.96)
    peak_demand_hour = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsDigitalTwinModel(Base):
    """Comprehensive physical asset digital twin model and synchronization anchor."""
    __tablename__ = "cps_digital_twins"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    twin_code = Column(String(64), nullable=False, unique=True, index=True)
    asset_id = Column(String(64), nullable=False, unique=True, index=True)
    twin_version = Column(String(32), nullable=False, default="v1.0")
    synchronization_status = Column(String(32), nullable=False, default="IN_SYNC")  # IN_SYNC, DRIFT_DETECTED, OFFLINE
    sync_latency_ms = Column(Float, nullable=False, default=45.0)
    last_physical_telemetry_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsTwinSimulationModel(Base):
    """Sandboxed What-If simulation runs modeling physical asset loads, stress, and failures."""
    __tablename__ = "cps_twin_simulations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    simulation_code = Column(String(64), nullable=False, index=True)
    twin_id = Column(String(64), nullable=False, index=True)
    scenario_type = Column(String(64), nullable=False)  # PEAK_OVERLOAD, BEARING_FAILURE, POWER_BROWNOUT
    simulation_state = Column(String(32), nullable=False, default="COMPLETED")
    predicted_downtime_hours = Column(Float, nullable=False, default=0.0)
    projected_risk_score = Column(Float, nullable=False, default=12.0)
    recommendations = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsSafetyPolicyModel(Base):
    """Hard-boundary safety rules, thermal ceilings, speed limits, and interlocks."""
    __tablename__ = "cps_safety_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    policy_code = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    target_asset_type = Column(String(64), nullable=False, index=True)
    rule_type = Column(String(64), nullable=False)  # MAX_SPEED, MAX_TEMPERATURE, RESTRICTED_ZONE, DUAL_AUTHORIZATION
    parameter_thresholds = Column(JSON, nullable=False, default=dict)
    enforcement_action = Column(String(32), nullable=False, default="BLOCK_AND_ALARM")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsSafetyEventModel(Base):
    """Real-world safety alerts, e-stops, boundary breaches, and physical incident records."""
    __tablename__ = "cps_safety_events"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    event_code = Column(String(64), nullable=False, index=True)
    facility_id = Column(String(64), nullable=False, index=True)
    asset_id = Column(String(64), nullable=True, index=True)
    severity = Column(String(32), nullable=False, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    event_type = Column(String(64), nullable=False)  # EMERGENCY_STOP, THERMAL_SPIKE, ZONE_BREACH, COLLISION_AVOIDANCE
    description = Column(Text, nullable=False)
    operator_notified = Column(Boolean, nullable=False, default=True)
    resolution_status = Column(String(32), nullable=False, default="OPEN")  # OPEN, INVESTIGATING, MITIGATED, RESOLVED
    occurred_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsFieldOperationModel(Base):
    """Mobile technician work checklists, digital signatures, and evidence capture."""
    __tablename__ = "cps_field_operations"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    operation_code = Column(String(64), nullable=False, unique=True, index=True)
    work_order_id = Column(String(64), nullable=False, index=True)
    technician_name = Column(String(128), nullable=False)
    checklist_status = Column(String(32), nullable=False, default="COMPLETED")
    evidence_attached = Column(Boolean, nullable=False, default=True)
    customer_signoff_verified = Column(Boolean, nullable=False, default=True)
    completed_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class CpsAgentRunModel(Base):
    """Autonomous Cyber-Physical agent activity and execution audit."""
    __tablename__ = "cps_agent_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_name = Column(String(64), nullable=False, index=True)
    action_name = Column(String(128), nullable=False)
    target_asset_id = Column(String(64), nullable=True, index=True)
    status = Column(String(32), nullable=False, default="COMPLETED")
    dry_run = Column(Boolean, nullable=False, default=True)
    execution_result = Column(JSON, nullable=False, default=dict)
    executed_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
