"""
Unit test suite for Phase 71: Autonomous Supply Chain, Logistics Intelligence,
Warehousing, Fleet Operations & Global Physical Commerce.
"""

import sys
import os
sys.path.insert(0, os.path.abspath("backend"))
sys.path.insert(0, os.path.abspath("."))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.autonomous_supply_chain_logistics_commerce import Base as ScBase
from app.services.supply_chain.service import AutonomousSupplyChainService

# 22 Autonomous Supply Chain AI Agents
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS
from agents.supply_chain import (
    SupplyChainOrchestratorAgent,
    SupplierAgent,
    ProcurementAgent,
    DemandAgent,
    ForecastingAgent,
    InventoryAgent,
    WarehouseAgent,
    PickingAgent,
    PackingAgent,
    ShippingAgent,
    TransportationAgent,
    FleetAgent,
    RoutingAgent,
    EtaAgent,
    DisruptionAgent,
    ResilienceAgent,
    OrderAgent,
    ReturnsAgent,
    CostAgent,
    SustainabilityAgent,
    DigitalTwinAgent,
    OptimizationAgent,
)


@pytest.fixture(scope="module")
def db_session():
    """In-memory SQLite test database for Phase 71 isolated to sc_ tables."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    sc_tables = [t for name, t in ScBase.metadata.tables.items() if name.startswith("sc_")]
    ScBase.metadata.create_all(bind=engine, tables=sc_tables)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def sc_service(db_session):
    return AutonomousSupplyChainService(db_session)


def test_supplier_management_and_performance(sc_service):
    """Test supplier tracking, PPM defect rates, and compliance."""
    suppliers = sc_service.suppliers.list_suppliers("t_sc_01")
    assert len(suppliers) >= 2
    alpha = next((s for s in suppliers if s["supplier_code"] == "SUP-ALPHA"), None)
    assert alpha is not None
    assert alpha["on_time_delivery_rate"] >= 95.0
    assert alpha["compliance_status"] == "COMPLIANT"
    assert alpha["quality_defect_rate_ppm"] <= 20.0


def test_procurement_intelligence_and_po_approval(sc_service):
    """Test purchase order formulation and dual-control human approval gate."""
    orders = sc_service.procurement.list_purchase_orders("t_sc_01")
    assert len(orders) >= 2
    high_value_po = next((po for po in orders if po["total_amount"] > 50000.0), None)
    assert high_value_po is not None
    assert high_value_po["requires_human_approval"] is True
    assert high_value_po["approval_status"] == "PENDING_APPROVAL"


def test_product_catalog_and_materials(sc_service):
    """Test global product catalog, storage temp regimes, and raw materials."""
    products = sc_service.products.list_products("t_sc_01")
    assert len(products) >= 2
    cryo_prod = next((p for p in products if p["sku"] == "SKU-BIO-SENS"), None)
    assert cryo_prod is not None
    assert cryo_prod["storage_temp_zone"] == "COLD_CHAIN"

    materials = sc_service.materials.list_materials("t_sc_01")
    assert len(materials) >= 2
    assert any(m["material_type"] == "RAW_MATERIAL" for m in materials)


def test_bill_of_materials_explosion(sc_service):
    """Test multi-level BOM explosion and critical path component flags."""
    bom_items = sc_service.bom.list_bom_items("t_sc_01")
    assert len(bom_items) >= 2
    assert all(item["is_critical_path"] for item in bom_items)
    assert any(item["component_sku"] == "MAT-SIL-99" for item in bom_items)


def test_multi_echelon_inventory_and_safety_stock(sc_service):
    """Test multi-echelon stock levels, allocation, and safety stock."""
    inventory = sc_service.inventory.list_inventory("t_sc_01")
    assert len(inventory) >= 2
    chicago_item = next((i for i in inventory if i["warehouse_id"] == "wh_chicago_01"), None)
    assert chicago_item is not None
    assert chicago_item["quantity_on_hand"] >= chicago_item["quantity_allocated"]
    assert chicago_item["safety_stock_level"] > 0
    assert chicago_item["stockout_risk_score"] < 10.0


def test_inventory_movement_audit_trail(sc_service):
    """Test audited stock receipts, picks, and reason tracking."""
    movements = sc_service.inventory_movements.list_movements("t_sc_01")
    assert len(movements) >= 2
    assert any(m["movement_type"] == "RECEIPT" for m in movements)
    assert any(m["audited_by_agent"] == "sc_warehouse" for m in movements)


def test_demand_forecasting_and_mrp(sc_service):
    """Test probabilistic multi-horizon forecasting (MAPE) and net MRP."""
    forecasts = sc_service.forecasting.list_forecasts("t_sc_01")
    assert len(forecasts) >= 1
    fc = forecasts[0]
    assert fc["mape_accuracy_pct"] >= 90.0
    assert fc["confidence_interval_low"] < fc["forecasted_units"] < fc["confidence_interval_high"]

    mrp = sc_service.mrp.calculate_mrp("t_sc_01")
    assert len(mrp) >= 1
    assert mrp[0]["planned_order_releases"] > 0


def test_warehouse_management_and_slotting(sc_service):
    """Test warehouse capacity, utilization, and golden-zone putaway."""
    warehouses = sc_service.warehouses.list_warehouses("t_sc_01")
    assert len(warehouses) >= 2
    wh1 = warehouses[0]
    assert wh1["operating_status"] == "OPERATIONAL"
    assert wh1["active_robots_count"] > 0

    slotting = sc_service.putaway.recommend_slotting("t_sc_01")
    assert len(slotting) >= 1
    assert slotting[0]["travel_distance_saving_pct"] > 0


def test_picking_and_smart_packing(sc_service):
    """Test wave picking tasks and eco-friendly cartonization."""
    pick_tasks = sc_service.picking.list_pick_tasks("t_sc_01")
    assert len(pick_tasks) >= 1
    assert pick_tasks[0]["picking_method"] == "WAVE_PICKING"

    packing = sc_service.packing.recommend_carton("t_sc_01")
    assert len(packing) >= 1
    assert "RECYCLED" in packing[0]["material_type"]


def test_carrier_and_fleet_management(sc_service):
    """Test carrier reliability and private electric vehicle fleet telemetry."""
    carriers = sc_service.carriers.list_carriers("t_sc_01")
    assert len(carriers) >= 2
    assert all(c["reliability_rating_pct"] >= 90.0 for c in carriers)

    vehicles = sc_service.fleet.list_vehicles("t_sc_01")
    assert len(vehicles) >= 2
    semi = next((v for v in vehicles if "SEMI" in v["vehicle_type"]), None)
    assert semi is not None
    assert semi["is_telemetry_active"] is True
    assert semi["battery_or_fuel_level_pct"] > 50.0


def test_vehicle_routing_optimization(sc_service):
    """Test mixed-integer VRP route optimization and fuel efficiency gain."""
    vrp = sc_service.routing_optimization.solve_vrp("t_sc_01")
    assert len(vrp) >= 1
    assert vrp[0]["fuel_savings_pct"] >= 10.0
    assert vrp[0]["stops_optimized"] > 0


def test_shipment_tracking_and_dynamic_eta(sc_service):
    """Test milestone GPS tracking and dynamic ETA prediction."""
    shipments = sc_service.shipments.list_shipments("t_sc_01")
    assert len(shipments) >= 1
    ship = shipments[0]
    assert ship["status"] == "IN_TRANSIT"
    assert ship["delay_risk_score"] < 5.0

    eta = sc_service.eta.predict_eta("t_sc_01")
    assert len(eta) >= 1
    assert eta[0]["confidence_interval_minutes"] > 0


def test_cold_chain_and_excursion_alerts(sc_service):
    """Test cryo biosensor temperature monitoring and excursion state."""
    alerts = sc_service.cold_chain.list_cold_chain_alerts("t_sc_01")
    assert len(alerts) >= 1
    alert = alerts[0]
    assert alert["allowed_min_temp"] <= alert["current_temperature_celsius"] <= alert["allowed_max_temp"]
    assert alert["is_excursion_critical"] is False


def test_order_management_and_returns(sc_service):
    """Test customer order allocation, RMA reverse logistics, and restock."""
    orders = sc_service.orders.list_orders("t_sc_01")
    assert len(orders) >= 1
    assert orders[0]["allocated_warehouse_id"] is not None

    returns = sc_service.returns.list_returns("t_sc_01")
    assert len(returns) >= 1
    assert returns[0]["disposition"] == "RESTOCK"
    assert returns[0]["refund_authorized"] is True


def test_disruption_management_and_resilience(sc_service):
    """Test chokepoint congestion detection and resilience index."""
    disruptions = sc_service.disruption.list_disruptions("t_sc_01")
    assert len(disruptions) >= 1
    assert disruptions[0]["requires_human_signoff"] is True

    resilience = sc_service.resilience.get_resilience_score("t_sc_01")
    assert len(resilience) >= 1
    res = resilience[0]
    assert res["global_resilience_index"] >= 90.0
    assert res["supplier_concentration_risk"] < 25.0


def test_cost_breakdown_and_sustainability(sc_service):
    """Test supply chain cost accounting and Scope 3 freight emissions."""
    costs = sc_service.costs.get_cost_breakdown("t_sc_01")
    assert len(costs) >= 1
    assert costs[0]["total_supply_chain_spend_usd"] > 0

    sust = sc_service.sustainability.get_sustainability_metrics("t_sc_01")
    assert len(sust) >= 1
    assert sust[0]["sustainable_packaging_adoption_pct"] >= 90.0
    assert sust[0]["warehouse_renewable_energy_ratio"] >= 0.80


def test_closed_loop_autonomous_supply_chain_cycle(sc_service):
    """Test the complete 11-stage closed-loop autonomous operating cycle."""
    cycle = sc_service.run_supply_chain_operating_cycle("t_sc_01", dry_run=True)
    assert cycle["overall_status"] == "COMPLETED"
    assert cycle["autonomous_actions_taken"] >= 15
    assert cycle["actions_requiring_human_approval"] >= 1
    assert cycle["simulated_savings_usd"] > 0
    stages = cycle["stage_progress"]
    assert "1_OBSERVE" in stages
    assert "2_FORECAST" in stages
    assert "3_PLAN" in stages
    assert "4_SIMULATE" in stages
    assert "5_OPTIMIZE" in stages
    assert "6_POLICY_CHECK" in stages
    assert "7_APPROVAL" in stages
    assert "8_EXECUTE" in stages
    assert "9_VERIFY" in stages
    assert "10_LEARN" in stages
    assert "11_AUDIT" in stages


@pytest.mark.asyncio
async def test_all_22_autonomous_supply_chain_agents():
    """Verify that all 22 Phase 71 supply chain agents execute cleanly."""
    agents = [
        SupplyChainOrchestratorAgent(),
        SupplierAgent(),
        ProcurementAgent(),
        DemandAgent(),
        ForecastingAgent(),
        InventoryAgent(),
        WarehouseAgent(),
        PickingAgent(),
        PackingAgent(),
        ShippingAgent(),
        TransportationAgent(),
        FleetAgent(),
        RoutingAgent(),
        EtaAgent(),
        DisruptionAgent(),
        ResilienceAgent(),
        OrderAgent(),
        ReturnsAgent(),
        CostAgent(),
        SustainabilityAgent(),
        DigitalTwinAgent(),
        OptimizationAgent(),
    ]
    assert len(agents) == 22

    context = AgentContext(
        workflow_id="wf_sc_test",
        task_id="task_supply_chain_diagnostics",
        agent_run_id="run_sc_001",
        metadata={"tenant_id": "test_tenant_71"}
    )
    for ag in agents:
        res = await ag.execute(context)
        assert res["status"] == "COMPLETED"
        assert res["agent_id"] == ag.agent_id
        assert "recommendations" in res
        assert len(res["recommendations"]) >= 1


def test_agent_safety_prohibitions():
    """Verify that Phase 71 safety prohibitions protect purchasing and fleet operations."""
    assert "AUTONOMOUS_ISSUE_PURCHASE_ORDER_UNREVIEWED" in PROHIBITED_PERMISSIONS
    assert "AUTONOMOUS_REROUTE_HAZARDOUS_FLEET_UNREVIEWED" in PROHIBITED_PERMISSIONS
    assert "AUTONOMOUS_WRITE_OFF_INVENTORY_UNREVIEWED" in PROHIBITED_PERMISSIONS
    assert "EXPOSE_SUPPLIER_COMMERCIAL_SECRETS" in PROHIBITED_PERMISSIONS
    assert "BYPASS_PROCUREMENT_BUDGET_GATES" in PROHIBITED_PERMISSIONS
    assert "AUTONOMOUS_CANCEL_CUSTOMER_ORDERS_UNREVIEWED" in PROHIBITED_PERMISSIONS
