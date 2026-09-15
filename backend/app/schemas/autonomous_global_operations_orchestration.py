"""
Phase 74: Autonomous Global Operations, Supply Network Intelligence, Logistics,
Procurement, Workforce & Enterprise Resource Orchestration Schemas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -------------------------------------------------------------------
# 1. Global Operations Control Tower & 10-Stage Loop
# -------------------------------------------------------------------
class OpsControlTowerSummaryResponse(BaseModel):
    operational_health_score: float
    on_time_delivery_rate_pct: float
    inventory_turnover_ratio: float
    supplier_otif_pct: float
    warehouse_capacity_utilization_pct: float
    workforce_capacity_utilization_pct: float
    production_schedule_adherence_pct: float
    critical_exceptions_count: int
    open_purchase_orders_count: int
    in_transit_shipments_count: int
    active_facilities_count: int
    digital_twin_nodes_count: int
    revenue_at_risk_estimate: float
    currency: str = "USD"


class OpsOperatingCycleExecutionResponse(BaseModel):
    cycle_run_id: str
    stages_executed: List[str]
    overall_status: str
    demand_forecasts_generated: int
    procurement_orders_planned: int
    shipment_routes_optimized: int
    bottlenecks_identified: int
    actions_requiring_human_approval: int
    simulation_scenarios_evaluated: int


# -------------------------------------------------------------------
# 2. Locations & Facilities
# -------------------------------------------------------------------
class OpsLocationCreate(BaseModel):
    code: str
    name: str
    location_type: str = "FACILITY"
    country: str = "US"
    region: Optional[str] = None
    city: Optional[str] = None
    timezone: str = "UTC"
    currency: str = "USD"


class OpsLocationResponse(BaseModel):
    id: str
    code: str
    name: str
    location_type: str
    country: str
    region: Optional[str] = None
    city: Optional[str] = None
    timezone: str
    currency: str
    is_active: bool
    created_at: datetime


class OpsFacilityResponse(BaseModel):
    id: str
    location_id: str
    name: str
    facility_type: str
    total_area_sqm: float
    utilization_pct: float
    safety_compliance_score: float
    status: str


# -------------------------------------------------------------------
# 3. Demand & Supply Planning
# -------------------------------------------------------------------
class OpsDemandForecastRequest(BaseModel):
    item_code: str
    forecast_horizon_days: int = 90
    scenario: str = "BASE_CASE"


class OpsForecastResponse(BaseModel):
    id: str
    item_code: str
    model_algorithm: str
    forecast_horizon_days: int
    predicted_quantity: float
    actual_quantity: Optional[float] = None
    variance_pct: Optional[float] = None
    scenario: str
    status: str
    created_at: datetime


class OpsSupplyPlanResponse(BaseModel):
    id: str
    plan_code: str
    planning_cycle: str
    target_service_level_pct: float
    total_planned_spend: float
    currency: str
    status: str
    bottlenecks_detected: Optional[Dict[str, Any]] = None


# -------------------------------------------------------------------
# 4. Suppliers & Procurement
# -------------------------------------------------------------------
class OpsSupplierResponse(BaseModel):
    id: str
    vendor_code: str
    legal_name: str
    country: str
    tier_level: int
    overall_score: float
    otif_rate_pct: float
    risk_rating: str
    financial_health_index: float
    sanctions_screened: bool
    active: bool


class OpsPurchaseOrderCreate(BaseModel):
    supplier_id: str
    total_amount: float
    currency: str = "USD"
    delivery_date_promised: Optional[datetime] = None
    line_items: Optional[List[Dict[str, Any]]] = None


class OpsPurchaseOrderResponse(BaseModel):
    id: str
    po_number: str
    supplier_id: str
    total_amount: float
    currency: str
    status: str
    three_way_match_status: str
    delivery_date_promised: Optional[datetime] = None
    created_at: datetime


class OpsThreeWayMatchResponse(BaseModel):
    po_id: str
    po_number: str
    invoice_number: str
    receipt_number: str
    price_variance_pct: float
    quantity_variance_pct: float
    is_matched: bool
    match_disposition: str
    details: Optional[Dict[str, Any]] = None


# -------------------------------------------------------------------
# 5. Inventory & Warehouses
# -------------------------------------------------------------------
class OpsInventoryItemResponse(BaseModel):
    id: str
    sku: str
    name: str
    category: str
    facility_id: str
    on_hand_qty: float
    allocated_qty: float
    available_qty: float
    safety_stock_qty: float
    reorder_point: float
    unit_cost: float
    currency: str
    status: str


class OpsWarehouseResponse(BaseModel):
    id: str
    code: str
    name: str
    facility_id: str
    total_capacity_pallets: int
    current_occupancy_pallets: int
    occupancy_pct: float
    dock_doors_count: int
    status: str


# -------------------------------------------------------------------
# 6. Logistics & Fleet
# -------------------------------------------------------------------
class OpsShipmentCreate(BaseModel):
    carrier_name: str
    transport_mode: str = "ROAD"
    origin_location: str
    destination_location: str
    weight_kg: float = 0.0
    eta: Optional[datetime] = None


class OpsShipmentResponse(BaseModel):
    id: str
    tracking_number: str
    carrier_name: str
    transport_mode: str
    origin_location: str
    destination_location: str
    weight_kg: float
    status: str
    eta: Optional[datetime] = None
    delay_risk_score: float
    customs_cleared: bool


class OpsRouteOptimizationResponse(BaseModel):
    route_id: str
    origin: str
    destination: str
    stops: List[str]
    total_distance_km: float
    estimated_transit_hours: float
    carbon_emissions_kg: float
    cost_estimate: float
    recommended_carrier: str


# -------------------------------------------------------------------
# 7. Workforce & Production
# -------------------------------------------------------------------
class OpsWorkforceCapacityResponse(BaseModel):
    facility_id: str
    department: str
    total_headcount: int
    active_headcount: int
    labor_utilization_pct: float
    critical_skill_gaps: Optional[List[str]] = None


class OpsShiftScheduleResponse(BaseModel):
    id: str
    schedule_code: str
    facility_id: str
    shift_name: str
    start_time: datetime
    end_time: datetime
    headcount_assigned: int
    optimization_fairness_score: float
    status: str


class OpsProductionOrderResponse(BaseModel):
    id: str
    order_code: str
    product_sku: str
    planned_quantity: float
    completed_quantity: float
    work_center_id: str
    efficiency_pct: float
    status: str


# -------------------------------------------------------------------
# 8. Digital Twin, Scenarios & Exceptions
# -------------------------------------------------------------------
class OpsDigitalTwinNodeResponse(BaseModel):
    id: str
    node_code: str
    node_type: str
    name: str
    throughput_capacity: float
    current_load: float
    resilience_score: float
    time_to_recover_hours: float
    time_to_survive_hours: float


class OpsScenarioSimulationRequest(BaseModel):
    scenario_type: str = "SUPPLIER_SHOCK"
    disruption_duration_days: int = 14
    impacted_nodes: Optional[List[str]] = None


class OpsScenarioSimulationResponse(BaseModel):
    simulation_code: str
    scenario_type: str
    disruption_duration_days: int
    estimated_revenue_at_risk: float
    working_capital_impact: float
    mitigation_strategy: str
    status: str


class OpsExceptionResponse(BaseModel):
    id: str
    exception_code: str
    category: str
    severity: str
    impact_description: str
    financial_cost_estimate: float
    assigned_owner: str
    recommended_action: Optional[str] = None
    status: str
