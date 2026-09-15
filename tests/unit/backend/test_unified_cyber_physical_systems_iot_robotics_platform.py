"""
Unit test suite for Phase 70: Autonomous Cyber-Physical Systems, IoT Intelligence,
Robotics Infrastructure, Digital Twins & Real-World AI Operations.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.cyber_physical_systems_iot_robotics import Base as CpsBase
from app.services.cyber_physical.service import AutonomousCyberPhysicalService

# 19 Autonomous Cyber-Physical AI Agents
from agents.core.context import AgentContext
from agents.cyber_physical import (
    CpsOrchestratorAgent,
    IotAgent,
    TelemetryAgent,
    DeviceHealthAgent,
    SensorAgent,
    AnomalyAgent,
    MaintenanceAgent,
    PredictiveMaintenanceAgent,
    RobotFleetAgent,
    RobotMissionAgent,
    MachineAgent,
    PhysicalEnergyAgent,
    FacilityAgent,
    DigitalTwinAgent,
    SimulationAgent,
    SafetyAgent,
    PhysicalIncidentAgent,
    AssetLifecycleAgent,
    PhysicalOperationsAgent,
)


@pytest.fixture(scope="module")
def db_session():
    """In-memory SQLite test database for Phase 70 isolated to cps_ tables."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    cps_tables = [t for name, t in CpsBase.metadata.tables.items() if name.startswith("cps_")]
    CpsBase.metadata.create_all(bind=engine, tables=cps_tables)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def cps_service(db_session):
    return AutonomousCyberPhysicalService(db_session)


def test_facility_and_zone_hierarchy(cps_service):
    """Test smart factory registration and zone safety tiers."""
    fac = cps_service.facilities.register_facility(
        facility_code="FAC-DET-01",
        name="Detroit Advanced Robotics Assembly",
        facility_type="FACTORY",
        total_area_sqm=45000.0,
        tenant_id="t_cps_01"
    )
    assert fac["facility_code"] == "FAC-DET-01"
    assert fac["operating_status"] == "OPERATIONAL"

    facilities = cps_service.facilities.list_facilities("t_cps_01")
    assert len(facilities) >= 2

    zones = cps_service.zones.list_zones(fac["id"])
    assert len(zones) >= 2
    assert any(z["safety_tier"] == "ROBOTIC_RESTRICTED" for z in zones)


def test_physical_asset_and_relationships(cps_service):
    """Test physical asset tagging, health, and parent-child hierarchy."""
    asset = cps_service.assets.register_asset(
        asset_tag="ROB-ARM-001",
        name="KUKA Titan Heavy Arm",
        asset_type="ROBOT_ARM",
        facility_id="fac_detroit_01",
        tenant_id="t_cps_01"
    )
    assert asset["asset_tag"] == "ROB-ARM-001"
    assert asset["health_score"] >= 90.0

    assets = cps_service.assets.list_assets(tenant_id="t_cps_01")
    assert len(assets) >= 2

    hierarchy = cps_service.asset_relationships.get_asset_hierarchy(asset["id"])
    assert len(hierarchy) >= 2
    assert any(h["relationship_type"] == "CONTAINS" for h in hierarchy)


def test_iot_device_and_shadow_drift(cps_service):
    """Test IoT gateway registration, identity verification, and shadow state."""
    dev = cps_service.devices.register_device(
        device_uid="PLC-SIEMENS-S7-1500",
        name="Line 1 Main PLC Gateway",
        device_type="PLC_GATEWAY",
        connectivity_protocol="OPC_UA",
        tenant_id="t_cps_01"
    )
    assert dev["device_uid"] == "PLC-SIEMENS-S7-1500"
    assert dev["connection_state"] == "ONLINE"

    devices = cps_service.devices.list_devices("t_cps_01")
    assert len(devices) >= 2

    ident = cps_service.device_identity.verify_device_credentials(dev["id"])
    assert ident["mtls_cert_valid"] is True
    assert ident["trust_level"] == "HARDWARE_ROOT_OF_TRUST"

    shadow = cps_service.device_shadow.get_shadow(dev["id"])
    assert shadow["has_drift"] is False
    assert "target_rpm" in shadow["reported_state"]


def test_sensor_telemetry_and_quality_scoring(cps_service):
    """Test sensor registry, high-frequency telemetry, and quality evaluation."""
    sensors = cps_service.sensors.list_sensors(tenant_id="t_cps_01")
    assert len(sensors) >= 2
    assert any(s["sensor_type"] == "VIBRATION" for s in sensors)

    telemetry = cps_service.telemetry.stream_telemetry(sensors[0]["id"], limit=5)
    assert len(telemetry) >= 2
    assert telemetry[0]["quality_flag"] == "VALID"

    quality = cps_service.telemetry_quality.evaluate_quality([1.74, 1.78, 1.75])
    assert quality["quality_grade"] == "PRISTINE"
    assert quality["valid_percentage"] == 100.0


def test_sensor_calibration_tracking(cps_service):
    """Test sensor calibration certification and drift tolerance."""
    cal = cps_service.calibration.get_calibration_record("sns_vib_01")
    assert cal["status"] == "CERTIFIED"
    assert cal["tolerance_deviation_pct"] < 0.5


def test_actuator_ranges_and_physical_commands(cps_service):
    """Test physical actuator safe limits, dry-run commands, and idempotency."""
    actuators = cps_service.actuators.list_actuators()
    assert len(actuators) >= 2
    assert actuators[0]["min_safe_range"] <= actuators[0]["current_position"] <= actuators[0]["max_safe_range"]

    cmd = cps_service.commands.issue_command(
        idempotency_key="key_test_valve_001",
        command_action="OPEN_VALVE",
        parameters={"target_position": 45.0},
        dry_run=True,
        tenant_id="t_cps_01"
    )
    assert cmd["execution_status"] == "SUCCESS"
    assert cmd["safety_check_passed"] is True
    assert cmd["dry_run"] is True


def test_command_safety_checks_and_dual_control(cps_service):
    """Test hard-boundary safety validation and authorization policies."""
    safety = cps_service.command_safety.validate_command_safety("SET_SPEED", {"target_rpm": 1800})
    assert safety["is_safe"] is True
    assert safety["within_thermal_limits"] is True

    auth = cps_service.command_authorization.authorize_physical_command(
        user_role="LEAD_AUTOMATION_ENGINEER",
        risk_level="LOW"
    )
    assert auth["authorized"] is True
    assert auth["audit_trail_recorded"] is True


def test_robotics_fleet_and_mission_dispatch(cps_service):
    """Test AMR fleet health, battery monitoring, and mission dispatch."""
    robots = cps_service.robots.list_robots(facility_id="fac_detroit_01", tenant_id="t_cps_01")
    assert len(robots) >= 2
    assert robots[0]["battery_charge_pct"] > 80.0

    fleet = cps_service.robot_fleet.get_fleet_telemetry("fac_detroit_01")
    assert fleet["total_fleet_size"] == 24
    assert fleet["available_count"] > 10

    mission = cps_service.robot_missions.create_mission(
        mission_code="MSN-TRANS-01",
        robot_id=robots[0]["id"],
        mission_type="MATERIAL_TRANSPORT",
        priority="HIGH",
        tenant_id="t_cps_01"
    )
    assert mission["mission_code"] == "MSN-TRANS-01"
    assert mission["status"] == "PENDING"


def test_robot_safety_zones(cps_service):
    """Test LiDAR field of view and speed governing in shared human spaces."""
    zone_check = cps_service.robot_safety.audit_robot_safety_zone("rob_amr_01")
    assert zone_check["lidar_fov_clear"] is True
    assert zone_check["safe_to_navigate"] is True


def test_machine_health_and_oee_diagnostics(cps_service):
    """Test industrial machinery health, vibration RMS, and OEE metrics."""
    machines = cps_service.machines.list_machines("fac_detroit_01")
    assert len(machines) >= 2
    assert machines[0]["oee_pct"] > 85.0

    health = cps_service.machine_health.get_machine_health("asset_cnc_02")
    assert health["overall_equipment_effectiveness"] > 85.0
    assert health["vibration_velocity_rms_mm_s"] < 2.5
    assert health["predicted_remaining_useful_life_hours"] > 3000.0
    assert health["health_verdict"] == "HEALTHY"


def test_predictive_maintenance_and_work_orders(cps_service):
    """Test predictive maintenance need forecasting and work order generation."""
    maint = cps_service.maintenance.predict_maintenance_need("asset_cnc_02")
    assert maint["confidence_level"] > 0.90
    assert maint["days_until_service_recommended"] > 30

    wo = cps_service.work_orders.create_work_order(
        work_order_code="WO-PRED-491",
        asset_id="asset_cnc_02",
        maintenance_type="PREDICTIVE",
        priority="LOW",
        tenant_id="t_cps_01"
    )
    assert wo["work_order_code"] == "WO-PRED-491"
    assert wo["status"] == "SCHEDULED"


def test_spare_parts_inventory_optimization(cps_service):
    """Test industrial spare parts stock check and lead time."""
    part = cps_service.spare_parts.check_part_stock("PART-BRG-6204")
    assert part["stock_status"] == "SUFFICIENT"
    assert part["stock_quantity"] >= part["reorder_threshold"]


def test_facility_energy_and_environmental_metrics(cps_service):
    """Test electrical demand, power factor, and ambient cleanroom telemetry."""
    energy = cps_service.energy.get_facility_energy_metrics("fac_detroit_01")
    assert energy["power_factor"] > 0.90
    assert energy["status"] == "OPTIMAL"

    env = cps_service.environmental.get_environmental_status("zone_assembly_a")
    assert 18.0 <= env["temperature_celsius"] <= 26.0
    assert env["status"] == "WITHIN_REGULATORY_LIMITS"


def test_digital_twin_synchronization_and_what_if_simulation(cps_service):
    """Test digital twin state synchronization and sandboxed What-If simulation."""
    twin = cps_service.digital_twins.get_twin_state("asset_arm_01")
    assert twin["synchronization_status"] == "IN_SYNC"
    assert twin["sync_latency_ms"] < 100.0

    sim = cps_service.simulation.run_simulation("twin_arm_01", "PEAK_OVERLOAD", dry_run=True)
    assert sim["verdict"] == "PHYSICALLY_STABLE"
    assert len(sim["recommendations"]) > 0

    what_if = cps_service.scenarios.evaluate_what_if_scenario("What happens if Line 1 coolant pump fails?")
    assert what_if["automatic_derate_triggered"] is True
    assert what_if["safety_buffer_sufficient"] is True


def test_safety_policies_and_emergency_stop(cps_service):
    """Test hard-boundary safety policy listing and facility emergency state."""
    policies = cps_service.safety.list_safety_policies("t_cps_01")
    assert len(policies) >= 2
    assert any(p["enforcement_action"] in ["BLOCK_AND_ALARM", "EMERGENCY_STOP"] for p in policies)

    emg = cps_service.emergency.check_emergency_state("fac_detroit_01")
    assert emg["emergency_stop_engaged"] is False
    assert emg["safety_interlocks_armed"] is True
    assert emg["status"] == "ALL_SYSTEMS_SAFE"


def test_field_operations_and_checklists(cps_service):
    """Test mobile technician work orders, digital checklists, and evidence."""
    tasks = cps_service.field_operations.list_field_tasks("tech_491")
    assert len(tasks) >= 1
    assert tasks[0]["checklist_status"] == "COMPLETED"

    chk = cps_service.checklists.verify_checklist("chk_robot_commission")
    assert chk["status"] == "VERIFIED"
    assert chk["safety_items_verified"] is True

    ev = cps_service.evidence.capture_evidence("wo_prevent_01", "IMAGE_CALIBRATION_CERT")
    assert "sha256_hash" in ev


@pytest.mark.asyncio
async def test_all_19_cyber_physical_agents():
    """Verify all 19 Autonomous Cyber-Physical AI Agents execute cleanly under AgentContext."""
    agents = [
        CpsOrchestratorAgent(),
        IotAgent(),
        TelemetryAgent(),
        DeviceHealthAgent(),
        SensorAgent(),
        AnomalyAgent(),
        MaintenanceAgent(),
        PredictiveMaintenanceAgent(),
        RobotFleetAgent(),
        RobotMissionAgent(),
        MachineAgent(),
        PhysicalEnergyAgent(),
        FacilityAgent(),
        DigitalTwinAgent(),
        SimulationAgent(),
        SafetyAgent(),
        PhysicalIncidentAgent(),
        AssetLifecycleAgent(),
        PhysicalOperationsAgent(),
    ]
    assert len(agents) == 19

    ctx = AgentContext(
        workflow_id="wf_cps_test",
        task_id="task_physical_diagnostics",
        agent_run_id="run_cps_001",
        metadata={"tenant_id": "t_cps_01"}
    )

    for agent in agents:
        res = await agent.execute(ctx)
        assert res["status"] == "COMPLETED"
        assert res["tenant_id"] == "t_cps_01"
        assert len(agent.get_required_permissions()) > 0


def test_closed_loop_12_stage_real_world_cycle(cps_service):
    """Test the complete 12-stage real-world operating cycle."""
    cycle = cps_service.run_cyber_physical_operating_cycle(
        tenant_id="t_cps_01",
        dry_run=True,
    )
    assert cycle["status"] == "COMPLETED"
    assert len(cycle["stages_executed"]) == 12
    assert "1_SENSE" in cycle["stages_executed"]
    assert "2_INGEST" in cycle["stages_executed"]
    assert "3_UNDERSTAND" in cycle["stages_executed"]
    assert "4_DETECT" in cycle["stages_executed"]
    assert "5_PREDICT" in cycle["stages_executed"]
    assert "6_SIMULATE" in cycle["stages_executed"]
    assert "7_PLAN" in cycle["stages_executed"]
    assert "8_SAFETY_CHECK" in cycle["stages_executed"]
    assert "9_AUTHORIZE" in cycle["stages_executed"]
    assert "10_ACT" in cycle["stages_executed"]
    assert "11_VERIFY" in cycle["stages_executed"]
    assert "12_LEARN" in cycle["stages_executed"]
    assert cycle["dry_run"] is True
    assert len(cycle["actions_taken"]) >= 8


def test_command_center_summary(cps_service):
    """Test executive-level Cyber-Physical Command Center summary metrics."""
    summary = cps_service.get_command_center_summary(tenant_id="t_cps_01")
    assert summary["physical_assets_count"] >= 2
    assert summary["iot_devices_online_count"] >= 2
    assert summary["robot_fleet_active_count"] == 24
    assert summary["average_oee_pct"] >= 85.0
    assert summary["emergency_stop_engaged"] is False
    assert summary["overall_facility_health_score"] >= 95.0
    assert summary["active_cps_agents_count"] == 19
