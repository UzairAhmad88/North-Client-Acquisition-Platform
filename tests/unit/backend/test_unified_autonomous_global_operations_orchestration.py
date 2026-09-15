"""
Phase 74 Test Suite: Unified Autonomous Global Operations, Supply Network Intelligence,
Logistics, Procurement, Workforce & Enterprise Resource Orchestration.
Validating 10-Stage Operations Loop, 3-Way Matching, Inventory Optimization, Route Planning,
Digital Twin Simulation, 20 Autonomous Operations Agents, and Safety Guardrails.
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.services.operations.service import EnterpriseOperationsOrchestrationService
from app.api.v1.operations_os import router as operations_os_router
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS
)
from agents.operations import (
    DemandForecastingAgent,
    SupplyPlanningAgent,
    ProcurementAgent,
    SourcingAgent,
    SupplierAgent,
    InventoryAgent,
    WarehouseAgent,
    LogisticsAgent,
    RouteOptimizationAgent,
    ShipmentAgent,
    WorkforceAgent,
    SchedulingAgent,
    CapacityAgent,
    ProductionAgent,
    QualityAgent,
    MaintenanceAgent,
    FacilityAgent,
    RiskAgent,
    DigitalTwinAgent,
    OperationsOrchestratorAgent
)
from agents.core.base import AgentContext


@pytest.fixture
def ops_service():
    return EnterpriseOperationsOrchestrationService()


@pytest.fixture
def test_client():
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(operations_os_router)
    return TestClient(app)


# ----------------------------------------------------------------------
# 1. 10-Stage Autonomous Operations Loop Tests
# ----------------------------------------------------------------------
def test_10_stage_operations_cycle(ops_service):
    """Verify end-to-end execution of the 10-stage autonomous operations cycle."""
    res = ops_service.run_operations_cycle("tenant-test", dry_run=True)
    assert res["status"] == "COMPLETED_SIMULATION"
    assert len(res["stages"]) == 10

    stage_names = [s["stage"] for s in res["stages"]]
    expected_stages = [
        "OBSERVE", "FORECAST", "PLAN", "OPTIMIZE", "SIMULATE",
        "RECOMMEND", "APPROVE", "EXECUTE", "VERIFY", "LEARN"
    ]
    assert stage_names == expected_stages


def test_control_tower_summary_metrics(ops_service):
    """Verify synthesis of operational health and control tower metrics."""
    summary = ops_service.get_control_tower_summary("tenant-test")
    assert summary["operational_health_score"] >= 90.0
    assert summary["on_time_delivery_rate_pct"] >= 95.0
    assert summary["inventory_turnover_ratio"] > 0
    assert summary["supplier_otif_pct"] >= 90.0
    assert summary["warehouse_capacity_utilization_pct"] > 0
    assert summary["workforce_capacity_utilization_pct"] > 0
    assert summary["critical_exceptions_count"] >= 0


# ----------------------------------------------------------------------
# 2. Three-Way Matching & Procurement Logic
# ----------------------------------------------------------------------
def test_three_way_match_execution(ops_service):
    """Verify 3-way matching reconciles PO, Goods Receipt, and Supplier Invoice."""
    match_res = ops_service.perform_three_way_match(
        po_id="po-9812",
        invoice_id="inv-88124",
        receipt_id="rec-4401"
    )
    assert match_res["is_matched"] is True
    assert match_res["match_disposition"] == "VERIFIED_READY_FOR_PAYMENT"
    assert match_res["price_variance_pct"] == 0.0
    assert match_res["quantity_variance_pct"] == 0.0


# ----------------------------------------------------------------------
# 3. Inventory Policies & Optimization
# ----------------------------------------------------------------------
def test_inventory_optimization_calculation(ops_service):
    """Verify safety stock and Economic Order Quantity calculation."""
    inv_opt = ops_service.calculate_inventory_optimization(
        sku="SKU-SENSOR-X9",
        facility_id="loc-001"
    )
    assert inv_opt["recommended_safety_stock"] > 0
    assert inv_opt["economic_order_quantity"] > 0
    assert inv_opt["stockout_probability_reduction_pct"] > 0


# ----------------------------------------------------------------------
# 4. Agent Permissions & Safety Prohibitions
# ----------------------------------------------------------------------
def test_operations_permissions_defined():
    """Verify Phase 74 operations permissions exist in AgentPermission enum."""
    assert hasattr(AgentPermission, "READ_OPERATIONS_OS")
    assert hasattr(AgentPermission, "MANAGE_GLOBAL_LOCATIONS")
    assert hasattr(AgentPermission, "GOVERN_DEMAND_SUPPLY_PLANNING")
    assert hasattr(AgentPermission, "MANAGE_ENTERPRISE_PROCUREMENT")
    assert hasattr(AgentPermission, "OPTIMIZE_MULTI_LOCATION_INVENTORY")
    assert hasattr(AgentPermission, "DISPATCH_MULTIMODAL_LOGISTICS")
    assert hasattr(AgentPermission, "SCHEDULE_ENTERPRISE_WORKFORCE")
    assert hasattr(AgentPermission, "OPERATE_SUPPLY_CHAIN_DIGITAL_TWIN")


def test_operations_prohibitions_enforced():
    """Verify non-negotiable Phase 74 safety prohibitions are strictly in PROHIBITED_PERMISSIONS."""
    prohibitions = [
        "AUTONOMOUS_AWARD_STRATEGIC_SUPPLIER_UNREVIEWED",
        "AUTONOMOUS_COMMIT_MAJOR_PROCUREMENT_UNREVIEWED",
        "AUTONOMOUS_EXECUTE_INVENTORY_WRITEOFF_UNREVIEWED",
        "AUTONOMOUS_SHUTDOWN_PRODUCTION_FACILITY_UNREVIEWED",
        "EXPOSE_PROPRIETARY_BILL_OF_MATERIALS",
        "AUTONOMOUS_ENFORCE_WORKFORCE_DISCIPLINARY_ACTION"
    ]
    for p in prohibitions:
        assert p in PROHIBITED_PERMISSIONS, f"Safety prohibition {p} missing from PROHIBITED_PERMISSIONS"


# ----------------------------------------------------------------------
# 5. 20 Autonomous Operations AI Agents Verification
# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_all_20_operations_agents_instantiation_and_execution():
    """Verify all 20 Phase 74 autonomous operations agents execute cleanly."""
    agents = [
        DemandForecastingAgent(),
        SupplyPlanningAgent(),
        ProcurementAgent(),
        SourcingAgent(),
        SupplierAgent(),
        InventoryAgent(),
        WarehouseAgent(),
        LogisticsAgent(),
        RouteOptimizationAgent(),
        ShipmentAgent(),
        WorkforceAgent(),
        SchedulingAgent(),
        CapacityAgent(),
        ProductionAgent(),
        QualityAgent(),
        MaintenanceAgent(),
        FacilityAgent(),
        RiskAgent(),
        DigitalTwinAgent(),
        OperationsOrchestratorAgent()
    ]
    assert len(agents) == 20

    context = AgentContext(workflow_id="wf-ops", task_id="t-ops-1", agent_run_id="run-ops-1", metadata={"tenant_id": "test-operations-tenant"})
    for agent in agents:
        res = await agent.run(context)
        assert res.status == "COMPLETED"
        assert res.confidence == "HIGH"
        assert "summary" in res.result


# ----------------------------------------------------------------------
# 6. FastAPI Operations OS API Endpoints Verification
# ----------------------------------------------------------------------
def test_api_control_tower_summary(test_client):
    """Test GET /operations-os/control-tower/summary endpoint."""
    resp = test_client.get("/operations-os/control-tower/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["operational_health_score"] >= 90.0
    assert data["on_time_delivery_rate_pct"] >= 95.0


def test_api_run_operating_cycle(test_client):
    """Test POST /operations-os/operating-cycle/run endpoint."""
    resp = test_client.post("/operations-os/operating-cycle/run?dry_run=true")
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_status"] == "COMPLETED_SIMULATION"
    assert len(data["stages_executed"]) == 10


def test_api_locations_endpoints(test_client):
    """Test GET & POST /operations-os/locations endpoints."""
    resp = test_client.get("/operations-os/locations")
    assert resp.status_code == 200
    locs = resp.json()
    assert len(locs) >= 2

    post_resp = test_client.post(
        "/operations-os/locations",
        json={
            "code": "US-DET-FAC-03",
            "name": "Detroit Advanced Assembly Plant",
            "location_type": "FACTORY",
            "country": "US",
            "city": "Detroit"
        }
    )
    assert post_resp.status_code == 200
    assert post_resp.json()["code"] == "US-DET-FAC-03"


def test_api_demand_forecast_generate(test_client):
    """Test POST /operations-os/forecasts/generate endpoint."""
    resp = test_client.post(
        "/operations-os/forecasts/generate",
        json={
            "item_code": "SKU-SENSOR-X9",
            "forecast_horizon_days": 90,
            "scenario": "BASE_CASE"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["item_code"] == "SKU-SENSOR-X9"
    assert data["predicted_quantity"] > 0


def test_api_suppliers_list(test_client):
    """Test GET /operations-os/suppliers endpoint."""
    resp = test_client.get("/operations-os/suppliers")
    assert resp.status_code == 200
    supps = resp.json()
    assert len(supps) >= 2
    assert supps[0]["otif_rate_pct"] >= 90.0


def test_api_three_way_match(test_client):
    """Test POST /operations-os/matching/three-way endpoint."""
    resp = test_client.post(
        "/operations-os/matching/three-way?po_id=po-1&invoice_id=inv-1&receipt_id=rc-1"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_matched"] is True
    assert data["match_disposition"] == "VERIFIED_READY_FOR_PAYMENT"


def test_api_inventory_items_and_optimization(test_client):
    """Test GET /operations-os/inventory/items and /inventory/optimization."""
    resp = test_client.get("/operations-os/inventory/items")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    opt_resp = test_client.get("/operations-os/inventory/optimization?sku=SKU-SENSOR-X9&facility_id=loc-001")
    assert opt_resp.status_code == 200
    assert opt_resp.json()["recommended_safety_stock"] > 0


def test_api_routes_optimize(test_client):
    """Test POST /operations-os/routes/optimize endpoint."""
    resp = test_client.post("/operations-os/routes/optimize?origin=Chicago&destination=Detroit")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_distance_km"] > 0
    assert len(data["stops"]) >= 1


def test_api_workforce_capacity_and_schedules(test_client):
    """Test GET /operations-os/workforce/capacity and /workforce/schedules."""
    resp = test_client.get("/operations-os/workforce/capacity?facility_id=loc-001")
    assert resp.status_code == 200
    assert resp.json()["labor_utilization_pct"] > 0

    sched_resp = test_client.get("/operations-os/workforce/schedules?facility_id=loc-001")
    assert sched_resp.status_code == 200
    assert len(sched_resp.json()) >= 1


def test_api_digital_twin_and_simulations(test_client):
    """Test GET /operations-os/digital-twin/nodes and POST /scenarios/simulate."""
    nodes_resp = test_client.get("/operations-os/digital-twin/nodes")
    assert nodes_resp.status_code == 200
    assert len(nodes_resp.json()) >= 2

    sim_resp = test_client.post(
        "/operations-os/scenarios/simulate",
        json={"scenario_type": "SUPPLIER_SHOCK", "disruption_duration_days": 14}
    )
    assert sim_resp.status_code == 200
    assert sim_resp.json()["status"] == "COMPLETED"


def test_api_exceptions_list(test_client):
    """Test GET /operations-os/exceptions endpoint."""
    resp = test_client.get("/operations-os/exceptions")
    assert resp.status_code == 200
    excs = resp.json()
    assert len(excs) >= 1
    assert excs[0]["severity"] in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
