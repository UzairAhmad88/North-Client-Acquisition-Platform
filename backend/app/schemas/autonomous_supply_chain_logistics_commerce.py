"""
Phase 71: Autonomous Supply Chain, Logistics Intelligence, Warehousing,
Fleet Operations & Global Physical Commerce Schemas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# 1. Suppliers & Contracts
class ScSupplierCreate(BaseModel):
    supplier_code: str
    company_name: str
    tier: str = "TIER_1"
    country_code: str = "US"
    risk_score: float = 14.2
    financial_health_rating: str = "AAA"
    compliance_status: str = "COMPLIANT"


class ScSupplierResponse(BaseModel):
    id: str
    supplier_code: str
    company_name: str
    tier: str
    country_code: str
    on_time_delivery_rate: float
    quality_defect_rate_ppm: float
    risk_score: float
    financial_health_rating: str
    compliance_status: str


class ScSupplierContractResponse(BaseModel):
    id: str
    contract_code: str
    supplier_id: str
    currency: str
    annual_committed_spend: float
    payment_terms_days: int
    lead_time_days: int
    is_active: bool


# 2. Products, Materials & BOM
class ScProductCreate(BaseModel):
    sku: str
    name: str
    category: str = "FINISHED_GOOD"
    unit: str = "UNIT"
    weight_kg: float = 1.0
    storage_temp_zone: str = "AMBIENT"


class ScProductResponse(BaseModel):
    id: str
    sku: str
    name: str
    category: str
    unit: str
    weight_kg: float
    storage_temp_zone: str
    unit_cost: float
    selling_price: float
    lifecycle_stage: str


class ScBillOfMaterialsResponse(BaseModel):
    id: str
    parent_product_id: str
    component_sku: str
    component_name: str
    quantity_required: float
    component_unit: str
    scrap_allowance_pct: float
    is_critical_path: bool


# 3. Procurement & Purchase Orders
class ScPurchaseOrderCreate(BaseModel):
    supplier_id: str
    destination_warehouse_id: str
    total_amount: float
    currency: str = "USD"
    items_count: int = 1
    requires_human_approval: bool = False


class ScPurchaseOrderResponse(BaseModel):
    id: str
    po_number: str
    supplier_id: str
    destination_warehouse_id: str
    total_amount: float
    currency: str
    items_count: int
    approval_status: str
    fulfillment_status: str
    requires_human_approval: bool


class ScPurchaseApprovalRequest(BaseModel):
    po_id: str
    decision: str = "APPROVED"  # APPROVED or REJECTED
    approver_notes: Optional[str] = None


# 4. Inventory & Multi-Echelon Tracking
class ScInventoryItemCreate(BaseModel):
    sku: str
    warehouse_id: str
    quantity_on_hand: float = 0.0
    safety_stock_level: float = 100.0
    reorder_point: float = 250.0


class ScInventoryItemResponse(BaseModel):
    id: str
    sku: str
    warehouse_id: str
    zone_code: Optional[str] = None
    bin_location: Optional[str] = None
    quantity_on_hand: float
    quantity_allocated: float
    quantity_available: float
    quantity_in_transit: float
    safety_stock_level: float
    reorder_point: float
    stockout_risk_score: float


class ScInventoryMovementResponse(BaseModel):
    id: str
    movement_type: str
    sku: str
    quantity: float
    source_location: Optional[str] = None
    destination_location: Optional[str] = None
    reason: str
    audited_by_agent: str


class ScSafetyStockResponse(BaseModel):
    sku: str
    service_level_target_pct: float
    calculated_safety_stock: float
    recommended_reorder_point: float
    lead_time_days: int
    demand_std_dev: float


# 5. Demand Forecasting & Scenarios
class ScDemandForecastCreate(BaseModel):
    product_sku: str
    target_region: str = "GLOBAL"
    forecast_period: str = "30_DAYS"
    forecasted_units: float = 1000.0


class ScDemandForecastResponse(BaseModel):
    id: str
    product_sku: str
    target_region: str
    forecast_period: str
    forecasted_units: float
    confidence_interval_low: float
    confidence_interval_high: float
    mape_accuracy_pct: float
    anomaly_detected: bool


# 6. Warehouses & Fulfillment
class ScWarehouseResponse(BaseModel):
    id: str
    warehouse_code: str
    name: str
    region: str
    country_code: str
    total_capacity_pallets: int
    used_capacity_pallets: int
    utilization_pct: float
    active_workers_count: int
    active_robots_count: int
    operating_status: str


class ScPickTaskResponse(BaseModel):
    id: str
    task_code: str
    warehouse_id: str
    order_id: str
    sku: str
    quantity_to_pick: float
    bin_location: str
    assigned_worker_or_robot_id: str
    status: str
    picking_method: str


class ScPackingRecommendationResponse(BaseModel):
    order_id: str
    recommended_carton_size: str
    material_type: str
    dunnage_required: str
    total_packed_weight_kg: float
    estimated_packing_cost_usd: float


# 7. Transportation, Fleet & Shipments
class ScCarrierResponse(BaseModel):
    id: str
    carrier_code: str
    name: str
    transport_mode: str
    reliability_rating_pct: float
    average_transit_time_days: float
    is_preferred: bool


class ScVehicleResponse(BaseModel):
    id: str
    vehicle_tag: str
    vehicle_type: str
    current_carrier_id: Optional[str] = None
    payload_capacity_kg: float
    battery_or_fuel_level_pct: float
    is_telemetry_active: bool
    status: str


class ScShipmentCreate(BaseModel):
    sales_order_id: str
    origin_warehouse_id: str
    destination_address: str
    carrier_id: str
    shipping_mode: str = "GROUND_EXPRESS"


class ScShipmentResponse(BaseModel):
    id: str
    tracking_number: str
    sales_order_id: str
    origin_warehouse_id: str
    destination_address: str
    carrier_id: str
    status: str
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    estimated_arrival_time: Optional[datetime] = None
    delay_risk_score: float
    temperature_excursion_alert: bool


class ScEtaPredictionResponse(BaseModel):
    shipment_id: str
    predicted_eta: datetime
    confidence_interval_minutes: int
    traffic_delay_minutes: int
    weather_impact_severity: str


class ScColdChainAlertResponse(BaseModel):
    shipment_id: str
    sensor_id: str
    current_temperature_celsius: float
    allowed_min_temp: float
    allowed_max_temp: float
    alert_type: str
    is_excursion_critical: bool


# 8. Order Management & Returns
class ScSalesOrderCreate(BaseModel):
    order_number: str
    customer_id: str
    destination_city: str
    total_order_value_usd: float
    delivery_priority: str = "STANDARD"


class ScSalesOrderResponse(BaseModel):
    id: str
    order_number: str
    customer_id: str
    destination_city: str
    total_order_value_usd: float
    delivery_priority: str
    allocated_warehouse_id: Optional[str] = None
    fulfillment_status: str


class ScReturnRequestResponse(BaseModel):
    id: str
    return_code: str
    sales_order_id: str
    sku: str
    quantity: float
    return_reason: str
    inspection_status: str
    disposition: str
    refund_authorized: bool


# 9. Disruption, Resilience & Simulation
class ScDisruptionEventResponse(BaseModel):
    id: str
    event_code: str
    disruption_type: str
    severity: str
    affected_facility_or_route: str
    financial_impact_estimate_usd: float
    mitigation_strategy: str
    requires_human_signoff: bool


class ScWhatIfSimulationRequest(BaseModel):
    scenario_type: str = "SUPPLIER_OUTAGE"  # SUPPLIER_OUTAGE, DEMAND_DOUBLING, ROUTE_BLOCKAGE, WAREHOUSE_FIRE
    affected_entity_id: str
    duration_days: int = 14
    dry_run: bool = True


class ScWhatIfSimulationResponse(BaseModel):
    scenario_type: str
    affected_entity_id: str
    duration_days: int
    projected_revenue_loss_usd: float
    projected_service_level_drop_pct: float
    stockout_risk_increase_pct: float
    recommended_mitigation_actions: List[str]
    is_human_signoff_required: bool


class ScResilienceScoreResponse(BaseModel):
    global_resilience_index: float
    supplier_concentration_risk: float
    single_point_of_failure_nodes: List[str]
    buffer_inventory_health_pct: float
    contingency_coverage_pct: float


# 10. Costs, Landed Cost & Sustainability
class ScCostBreakdownResponse(BaseModel):
    procurement_costs_usd: float
    warehousing_holding_costs_usd: float
    transportation_freight_costs_usd: float
    returns_reverse_costs_usd: float
    total_supply_chain_spend_usd: float
    cost_per_delivered_order_usd: float


class ScLandedCostCalculationResponse(BaseModel):
    sku: str
    fob_purchase_cost: float
    freight_shipping_cost: float
    customs_duties_and_tariffs: float
    insurance_and_handling: float
    total_landed_cost_unit_usd: float


class ScSustainabilityMetricsResponse(BaseModel):
    scope_3_freight_emissions_kg_co2: float
    average_carbon_intensity_per_ton_km: float
    sustainable_packaging_adoption_pct: float
    warehouse_renewable_energy_ratio: float


# 11. Digital Twins, Optimization & Agents
class ScDigitalTwinResponse(BaseModel):
    id: str
    twin_code: str
    network_nodes_count: int
    active_shipments_simulated: int
    resilience_score: float
    sync_status: str


class ScOptimizationRequest(BaseModel):
    optimization_type: str = "MULTI_ECHELON_INVENTORY"  # MULTI_ECHELON_INVENTORY, VEHICLE_ROUTING_VRP, WAREHOUSE_SLOTTING
    objective: str = "MINIMIZE_COST_MAXIMIZE_SLA"
    constraints: Dict[str, Any] = Field(default_factory=dict)


class ScOptimizationResponse(BaseModel):
    optimization_run_id: str
    optimization_type: str
    objective_value_achieved: float
    projected_cost_savings_pct: float
    sla_improvement_pct: float
    recommendations: List[str]


class ScAgentActionResponse(BaseModel):
    id: str
    agent_name: str
    action_type: str
    status: str
    dry_run: bool
    execution_result: Dict[str, Any]


# 12. Control Tower Summary & Autonomous Operating Cycle
class ScControlTowerSummaryResponse(BaseModel):
    active_suppliers_count: int
    active_purchase_orders_count: int
    total_inventory_valuation_usd: float
    global_stockout_risk_score: float
    active_warehouses_count: int
    warehouse_capacity_utilization_pct: float
    in_transit_shipments_count: int
    on_time_delivery_rate_pct: float
    active_fleet_vehicles_count: int
    active_cold_chain_alerts_count: int
    active_disruptions_count: int
    global_supply_chain_resilience_score: float
    active_agents_count: int


class ScOperatingCycleExecutionResponse(BaseModel):
    cycle_run_id: str
    stage_progress: Dict[str, str]
    overall_status: str
    autonomous_actions_taken: int
    actions_requiring_human_approval: int
    simulated_savings_usd: float
