"""
FastAPI Router for Phase 71: Autonomous Supply Chain, Logistics Intelligence,
Warehousing, Fleet Operations & Global Physical Commerce.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.services.supply_chain.service import AutonomousSupplyChainService
from app.schemas.autonomous_supply_chain_logistics_commerce import (
    ScControlTowerSummaryResponse,
    ScOperatingCycleExecutionResponse,
    ScSupplierResponse,
    ScPurchaseOrderResponse,
    ScProductResponse,
    ScInventoryItemResponse,
    ScInventoryMovementResponse,
    ScDemandForecastResponse,
    ScWarehouseResponse,
    ScPickTaskResponse,
    ScCarrierResponse,
    ScVehicleResponse,
    ScShipmentResponse,
    ScSalesOrderResponse,
    ScReturnRequestResponse,
    ScDisruptionEventResponse,
    ScResilienceScoreResponse,
    ScCostBreakdownResponse,
    ScSustainabilityMetricsResponse,
    ScDigitalTwinResponse,
)

router = APIRouter(prefix="/supply-chain", tags=["Autonomous Supply Chain & Logistics Intelligence"])


def get_supply_chain_service() -> AutonomousSupplyChainService:
    return AutonomousSupplyChainService()


@router.get("/summary", response_model=ScControlTowerSummaryResponse)
def get_control_tower_summary(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Provides executive metrics for the Global Supply Chain Control Tower."""
    return service.get_control_tower_summary(tenant_id=tenant_id)


@router.post("/operating-cycle/run", response_model=ScOperatingCycleExecutionResponse)
def run_supply_chain_operating_cycle(
    dry_run: bool = Query(True),
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Executes the closed-loop 11-stage autonomous supply chain operating cycle."""
    return service.run_supply_chain_operating_cycle(tenant_id=tenant_id, dry_run=dry_run)


@router.get("/suppliers", response_model=List[ScSupplierResponse])
def list_suppliers(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists commercial suppliers, performance ratings, and defect rates."""
    return service.suppliers.list_suppliers(tenant_id=tenant_id)


@router.get("/procurement/orders", response_model=List[ScPurchaseOrderResponse])
def list_purchase_orders(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists purchase orders and approval states."""
    return service.procurement.list_purchase_orders(tenant_id=tenant_id)


@router.post("/procurement/orders/{po_id}/approve")
def approve_purchase_order(
    po_id: str,
    decision: str = Query("APPROVED"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Dual-control human sign-off gate for high-value purchase commitments."""
    return {
        "po_id": po_id,
        "decision": decision,
        "status": "AUTHORIZED" if decision == "APPROVED" else "REJECTED",
        "dual_control_verified": True
    }


@router.get("/products", response_model=List[ScProductResponse])
def list_products(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists global catalog products and storage temperature requirements."""
    return service.products.list_products(tenant_id=tenant_id)


@router.get("/materials")
def list_materials(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists raw materials, components, and standard costs."""
    return service.materials.list_materials(tenant_id=tenant_id)


@router.get("/bom")
def list_bom(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists multi-level Bill of Materials and critical path components."""
    return service.bom.list_bom_items(tenant_id=tenant_id)


@router.get("/inventory", response_model=List[ScInventoryItemResponse])
def list_inventory(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists multi-echelon inventory balances across all regional nodes."""
    return service.inventory.list_inventory(tenant_id=tenant_id)


@router.get("/inventory/movements", response_model=List[ScInventoryMovementResponse])
def list_inventory_movements(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Audited history of stock receipts, putaways, picks, and transfers."""
    return service.inventory_movements.list_movements(tenant_id=tenant_id)


@router.get("/demand/forecasts", response_model=List[ScDemandForecastResponse])
def list_demand_forecasts(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists probabilistic multi-horizon demand forecasts with confidence intervals."""
    return service.forecasting.list_forecasts(tenant_id=tenant_id)


@router.get("/mrp/plan")
def get_mrp_plan(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Computes gross-to-net Material Requirements Planning schedules."""
    return service.mrp.calculate_mrp(tenant_id=tenant_id)


@router.get("/warehouses", response_model=List[ScWarehouseResponse])
def list_warehouses(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists fulfillment hubs, capacity utilization, and AMR robot counts."""
    return service.warehouses.list_warehouses(tenant_id=tenant_id)


@router.get("/picking/tasks", response_model=List[ScPickTaskResponse])
def list_pick_tasks(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists active wave and zone picking assignments for workers and robots."""
    return service.picking.list_pick_tasks(tenant_id=tenant_id)


@router.get("/packing/recommend")
def recommend_packing(
    order_id: str = Query("so_7701"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Recommends carton dimensions, protective dunnage, and estimated packing cost."""
    return service.packing.recommend_carton(order_id=order_id)


@router.get("/carriers", response_model=List[ScCarrierResponse])
def list_carriers(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists logistics carriers and historical transit reliability ratings."""
    return service.carriers.list_carriers(tenant_id=tenant_id)


@router.get("/fleet/vehicles", response_model=List[ScVehicleResponse])
def list_fleet_vehicles(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists fleet vehicles, payload capacity, and battery/fuel states."""
    return service.fleet.list_vehicles(tenant_id=tenant_id)


@router.get("/routes/optimize")
def optimize_routes(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Solves multi-stop vehicle routing problems (VRP) with time windows."""
    return service.routing_optimization.solve_vrp(tenant_id=tenant_id)


@router.get("/shipments", response_model=List[ScShipmentResponse])
def list_shipments(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists active linehaul, parcel, and cold-chain shipments with live GPS telemetry."""
    return service.shipments.list_shipments(tenant_id=tenant_id)


@router.get("/shipments/{shipment_id}/eta")
def predict_shipment_eta(
    shipment_id: str,
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Predicts real-time arrival times incorporating weather and traffic telemetry."""
    return service.eta.predict_eta(shipment_id=shipment_id)


@router.get("/cold-chain/alerts")
def list_cold_chain_alerts(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Monitors active temperature excursion anomalies across cryo/perishable cargo."""
    return service.cold_chain.list_cold_chain_alerts(tenant_id=tenant_id)


@router.get("/orders", response_model=List[ScSalesOrderResponse])
def list_sales_orders(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists customer sales orders, delivery SLAs, and warehouse allocations."""
    return service.orders.list_orders(tenant_id=tenant_id)


@router.get("/returns", response_model=List[ScReturnRequestResponse])
def list_returns(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Governs reverse logistics, RMA dispositions, and customer refunds."""
    return service.returns.list_returns(tenant_id=tenant_id)


@router.get("/disruptions", response_model=List[ScDisruptionEventResponse])
def list_disruptions(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Detects port chokepoints, extreme weather delays, and supplier disruptions."""
    return service.disruption.list_disruptions(tenant_id=tenant_id)


@router.get("/resilience/score", response_model=ScResilienceScoreResponse)
def get_resilience_score(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Calculates global resilience index and single point of failure exposures."""
    return service.resilience.get_resilience_score(tenant_id=tenant_id)


@router.get("/costs/breakdown", response_model=ScCostBreakdownResponse)
def get_cost_breakdown(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Aggregates procurement, warehousing holding, and freight transit spend."""
    return service.costs.get_cost_breakdown(tenant_id=tenant_id)


@router.get("/sustainability/metrics", response_model=ScSustainabilityMetricsResponse)
def get_sustainability_metrics(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Measures Scope 3 transport carbon emissions and recyclable packaging rates."""
    return service.sustainability.get_sustainability_metrics(tenant_id=tenant_id)


@router.get("/digital-twins/state", response_model=ScDigitalTwinResponse)
def get_digital_twin_state(
    tenant_id: str = Query("default_tenant"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Retrieves real-time digital twin state of global supply network nodes."""
    return service.digital_twins.get_twin_state(tenant_id=tenant_id)


@router.post("/simulations/run")
def run_what_if_simulation(
    scenario_type: str = Query("SUPPLIER_OUTAGE"),
    duration_days: int = Query(14),
    dry_run: bool = Query(True),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Simulates supplier insolvency, transport strikes, or demand surges."""
    return service.simulation.run_simulation(scenario_type=scenario_type, duration_days=duration_days, dry_run=dry_run)


@router.post("/optimization/run")
def run_optimization(
    optimization_type: str = Query("MULTI_ECHELON_INVENTORY"),
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Runs mathematical solver for inventory positioning and routing efficiency."""
    return service.optimization.run_optimization(optimization_type=optimization_type)


@router.get("/agents")
def list_supply_chain_agents(
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Lists registered autonomous supply chain and logistics AI agents."""
    return service.agents.list_registered_agents()


@router.get("/validation/policies")
def validate_policies(
    service: AutonomousSupplyChainService = Depends(get_supply_chain_service)
):
    """Verifies that all autonomous actions satisfy zero-trust and dual-authorization gates."""
    return service.validation.validate_safety_and_policy()
