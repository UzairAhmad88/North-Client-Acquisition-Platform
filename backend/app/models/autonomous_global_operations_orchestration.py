"""
Phase 74: Autonomous Global Operations, Supply Network Intelligence, Logistics,
Procurement, Workforce & Enterprise Resource Orchestration Models.
Database table prefix: ops_*
"""

from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Float,
    Integer,
    Text,
    JSON,
    ForeignKey,
    Index
)
from app.models.base import Base


# -------------------------------------------------------------------
# 1. Operating Locations & Facilities
# -------------------------------------------------------------------
class OpsLocationModel(Base):
    __tablename__ = "ops_locations"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    code = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    location_type = Column(String(64), nullable=False, default="FACILITY")  # SITE, WAREHOUSE, OFFICE, FACTORY, DC
    country = Column(String(64), nullable=False, default="US")
    region = Column(String(64), nullable=True)
    city = Column(String(128), nullable=True)
    timezone = Column(String(64), nullable=False, default="UTC")
    currency = Column(String(8), nullable=False, default="USD")
    operating_hours = Column(JSON, nullable=True)
    capacity_metrics = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class OpsFacilityModel(Base):
    __tablename__ = "ops_facilities"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    location_id = Column(String(64), ForeignKey("ops_locations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    facility_type = Column(String(64), nullable=False)  # MANUFACTURING, WAREHOUSE, R&D, DATA_CENTER
    total_area_sqm = Column(Float, nullable=False, default=0.0)
    utilization_pct = Column(Float, nullable=False, default=0.0)
    energy_rating = Column(String(32), nullable=True)
    safety_compliance_score = Column(Float, nullable=False, default=100.0)
    status = Column(String(32), nullable=False, default="OPERATIONAL")
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 2. Demand & Supply Planning
# -------------------------------------------------------------------
class OpsDemandModel(Base):
    __tablename__ = "ops_demand"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    demand_type = Column(String(64), nullable=False)  # CUSTOMER, PRODUCT, SERVICE, WORKFORCE, CAPACITY
    item_code = Column(String(64), nullable=False, index=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    quantity_demanded = Column(Float, nullable=False, default=0.0)
    confidence_level = Column(Float, nullable=False, default=0.95)
    source = Column(String(64), nullable=False, default="FORECAST_ENGINE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsForecastModel(Base):
    __tablename__ = "ops_forecasts"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    item_code = Column(String(64), nullable=False, index=True)
    model_algorithm = Column(String(64), nullable=False, default="ENSEMBLE_PROBABILISTIC")
    forecast_horizon_days = Column(Integer, nullable=False, default=90)
    predicted_quantity = Column(Float, nullable=False, default=0.0)
    actual_quantity = Column(Float, nullable=True)
    variance_pct = Column(Float, nullable=True)
    error_metric_mape = Column(Float, nullable=True)
    scenario = Column(String(64), nullable=False, default="BASE_CASE")
    status = Column(String(32), nullable=False, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsSupplyPlanModel(Base):
    __tablename__ = "ops_supply_plans"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    plan_code = Column(String(64), nullable=False, unique=True)
    planning_cycle = Column(String(32), nullable=False, default="MONTHLY")
    target_service_level_pct = Column(Float, nullable=False, default=98.5)
    total_planned_spend = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    status = Column(String(32), nullable=False, default="APPROVED")  # DRAFT, APPROVED, COMMITTED
    bottlenecks_detected = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# -------------------------------------------------------------------
# 3. Suppliers, Sourcing & Procurement
# -------------------------------------------------------------------
class OpsSupplierModel(Base):
    __tablename__ = "ops_suppliers"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    vendor_code = Column(String(64), nullable=False, index=True)
    legal_name = Column(String(255), nullable=False)
    country = Column(String(64), nullable=False, default="US")
    tier_level = Column(Integer, nullable=False, default=1)  # 1, 2, 3
    overall_score = Column(Float, nullable=False, default=88.5)
    otif_rate_pct = Column(Float, nullable=False, default=96.0)  # On-Time In-Full
    quality_defect_ppm = Column(Float, nullable=False, default=15.0)
    risk_rating = Column(String(32), nullable=False, default="LOW")
    sanctions_screened = Column(Boolean, nullable=False, default=True)
    financial_health_index = Column(Float, nullable=False, default=92.0)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsSourcingEventModel(Base):
    __tablename__ = "ops_sourcing_events"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    event_code = Column(String(64), nullable=False, unique=True)
    event_type = Column(String(32), nullable=False, default="RFP")  # RFQ, RFP, AUCTION
    title = Column(String(255), nullable=False)
    budget_estimated = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    status = Column(String(32), nullable=False, default="OPEN")  # DRAFT, OPEN, EVALUATION, AWARDED
    selected_bid_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsPurchaseOrderModel(Base):
    __tablename__ = "ops_purchase_orders"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    po_number = Column(String(64), nullable=False, unique=True)
    supplier_id = Column(String(64), ForeignKey("ops_suppliers.id"), nullable=False)
    total_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    status = Column(String(32), nullable=False, default="ISSUED")  # DRAFT, PENDING_APPROVAL, ISSUED, FULFILLED, MATCHED
    three_way_match_status = Column(String(32), nullable=False, default="PENDING")  # PENDING, MATCHED, DISCREPANCY
    delivery_date_promised = Column(DateTime, nullable=True)
    approval_signer = Column(String(128), nullable=True)
    line_items = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsGoodsReceiptModel(Base):
    __tablename__ = "ops_goods_receipts"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    receipt_number = Column(String(64), nullable=False, unique=True)
    po_id = Column(String(64), ForeignKey("ops_purchase_orders.id"), nullable=False)
    received_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    received_by = Column(String(128), nullable=False)
    items_received = Column(JSON, nullable=False)
    inspection_passed = Column(Boolean, nullable=False, default=True)
    status = Column(String(32), nullable=False, default="VERIFIED")


# -------------------------------------------------------------------
# 4. Multi-Location Inventory & Warehouses
# -------------------------------------------------------------------
class OpsInventoryItemModel(Base):
    __tablename__ = "ops_inventory_items"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    sku = Column(String(64), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, default="FINISHED_GOODS")  # RAW, WIP, FINISHED, SPARE_PART
    facility_id = Column(String(64), nullable=False)
    on_hand_qty = Column(Float, nullable=False, default=0.0)
    allocated_qty = Column(Float, nullable=False, default=0.0)
    available_qty = Column(Float, nullable=False, default=0.0)
    safety_stock_qty = Column(Float, nullable=False, default=10.0)
    reorder_point = Column(Float, nullable=False, default=25.0)
    unit_cost = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    status = Column(String(32), nullable=False, default="HEALTHY")  # HEALTHY, LOW, EXCESS, CRITICAL
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsWarehouseModel(Base):
    __tablename__ = "ops_warehouses"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    code = Column(String(64), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    facility_id = Column(String(64), nullable=False)
    total_capacity_pallets = Column(Integer, nullable=False, default=10000)
    current_occupancy_pallets = Column(Integer, nullable=False, default=6500)
    occupancy_pct = Column(Float, nullable=False, default=65.0)
    dock_doors_count = Column(Integer, nullable=False, default=24)
    active_pickers_count = Column(Integer, nullable=False, default=45)
    status = Column(String(32), nullable=False, default="OPERATIONAL")


# -------------------------------------------------------------------
# 5. Orders, Logistics, Fleet & Customs
# -------------------------------------------------------------------
class OpsOrderModel(Base):
    __tablename__ = "ops_orders"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    order_number = Column(String(64), nullable=False, unique=True)
    order_type = Column(String(32), nullable=False, default="SALES")  # SALES, TRANSFER, WORK, PROJECT
    customer_or_dest_id = Column(String(64), nullable=False)
    fulfillment_status = Column(String(32), nullable=False, default="ALLOCATED")  # REQUESTED, ALLOCATED, PICKED, SHIPPED, DELIVERED
    order_value = Column(Float, nullable=False, default=0.0)
    currency = Column(String(8), nullable=False, default="USD")
    priority = Column(String(16), nullable=False, default="NORMAL")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsShipmentModel(Base):
    __tablename__ = "ops_shipments"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    tracking_number = Column(String(64), nullable=False, unique=True)
    carrier_name = Column(String(128), nullable=False)
    transport_mode = Column(String(32), nullable=False, default="ROAD")  # ROAD, RAIL, AIR, SEA, MULTIMODAL
    origin_location = Column(String(128), nullable=False)
    destination_location = Column(String(128), nullable=False)
    weight_kg = Column(Float, nullable=False, default=0.0)
    status = Column(String(32), nullable=False, default="IN_TRANSIT")  # BOOKED, DISPATCHED, IN_TRANSIT, DELIVERED, DELAYED
    eta = Column(DateTime, nullable=True)
    delay_risk_score = Column(Float, nullable=False, default=0.05)
    customs_cleared = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsVehicleModel(Base):
    __tablename__ = "ops_vehicles"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    fleet_code = Column(String(64), nullable=False, unique=True)
    vehicle_type = Column(String(64), nullable=False, default="SEMI_TRAILER")
    capacity_kg = Column(Float, nullable=False, default=24000.0)
    telemetry_status = Column(String(32), nullable=False, default="CONNECTED")
    current_lat = Column(Float, nullable=True)
    current_lon = Column(Float, nullable=True)
    fuel_pct = Column(Float, nullable=False, default=85.0)
    operational_status = Column(String(32), nullable=False, default="AVAILABLE")


# -------------------------------------------------------------------
# 6. Workforce Capacity & Scheduling Optimization
# -------------------------------------------------------------------
class OpsWorkforceCapacityModel(Base):
    __tablename__ = "ops_workforce_capacity"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    facility_id = Column(String(64), nullable=False)
    department = Column(String(64), nullable=False, default="LOGISTICS_OPS")
    total_headcount = Column(Integer, nullable=False, default=120)
    active_headcount = Column(Integer, nullable=False, default=112)
    labor_utilization_pct = Column(Float, nullable=False, default=87.5)
    critical_skill_gaps = Column(JSON, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsShiftScheduleModel(Base):
    __tablename__ = "ops_schedules"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    schedule_code = Column(String(64), nullable=False, unique=True)
    facility_id = Column(String(64), nullable=False)
    shift_name = Column(String(64), nullable=False, default="DAY_SHIFT_ALPHA")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    headcount_assigned = Column(Integer, nullable=False, default=30)
    optimization_fairness_score = Column(Float, nullable=False, default=0.96)
    status = Column(String(32), nullable=False, default="PUBLISHED")


# -------------------------------------------------------------------
# 7. Production, Quality & Assets
# -------------------------------------------------------------------
class OpsProductionOrderModel(Base):
    __tablename__ = "ops_production_orders"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    order_code = Column(String(64), nullable=False, unique=True)
    product_sku = Column(String(64), nullable=False)
    planned_quantity = Column(Float, nullable=False, default=1000.0)
    completed_quantity = Column(Float, nullable=False, default=0.0)
    work_center_id = Column(String(64), nullable=False)
    efficiency_pct = Column(Float, nullable=False, default=94.5)
    status = Column(String(32), nullable=False, default="RUNNING")  # SCHEDULED, RUNNING, COMPLETED, HALTED
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)


class OpsQualityEventModel(Base):
    __tablename__ = "ops_quality_events"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    event_code = Column(String(64), nullable=False, unique=True)
    facility_id = Column(String(64), nullable=False)
    defect_type = Column(String(64), nullable=False, default="TOLERANCE_VARIANCE")
    severity = Column(String(16), nullable=False, default="MEDIUM")
    root_cause = Column(Text, nullable=True)
    corrective_action_plan = Column(Text, nullable=True)
    disposition = Column(String(32), nullable=False, default="REWORKED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsAssetModel(Base):
    __tablename__ = "ops_assets"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    asset_tag = Column(String(64), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    facility_id = Column(String(64), nullable=False)
    condition = Column(String(32), nullable=False, default="EXCELLENT")
    health_score = Column(Float, nullable=False, default=95.0)
    mtbf_hours = Column(Float, nullable=False, default=1200.0)
    failure_probability_30d = Column(Float, nullable=False, default=0.02)
    last_maintenance = Column(DateTime, nullable=True)
    next_scheduled_maintenance = Column(DateTime, nullable=True)


# -------------------------------------------------------------------
# 8. Digital Twin, Scenarios & Operational Risk
# -------------------------------------------------------------------
class OpsDigitalTwinNodeModel(Base):
    __tablename__ = "ops_digital_twin_nodes"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    node_code = Column(String(64), nullable=False, unique=True)
    node_type = Column(String(32), nullable=False)  # SUPPLIER, FACTORY, WAREHOUSE, CARRIER, CUSTOMER
    name = Column(String(255), nullable=False)
    throughput_capacity = Column(Float, nullable=False, default=1000.0)
    current_load = Column(Float, nullable=False, default=650.0)
    resilience_score = Column(Float, nullable=False, default=90.0)
    time_to_recover_hours = Column(Float, nullable=False, default=24.0)
    time_to_survive_hours = Column(Float, nullable=False, default=72.0)


class OpsScenarioSimulationModel(Base):
    __tablename__ = "ops_simulations"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    simulation_code = Column(String(64), nullable=False, unique=True)
    scenario_type = Column(String(64), nullable=False, default="SUPPLIER_SHOCK")
    disruption_duration_days = Column(Integer, nullable=False, default=14)
    estimated_revenue_at_risk = Column(Float, nullable=False, default=150000.0)
    working_capital_impact = Column(Float, nullable=False, default=45000.0)
    mitigation_strategy = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="COMPLETED")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class OpsExceptionModel(Base):
    __tablename__ = "ops_exceptions"

    id = Column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(64), nullable=False, index=True, default="tenant-default")
    exception_code = Column(String(64), nullable=False, unique=True)
    category = Column(String(64), nullable=False, default="SUPPLY_CHAIN_BOTTLENECK")
    severity = Column(String(16), nullable=False, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    impact_description = Column(Text, nullable=False)
    financial_cost_estimate = Column(Float, nullable=False, default=0.0)
    assigned_owner = Column(String(128), nullable=False)
    recommended_action = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="OPEN")  # OPEN, MITIGATED, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# Dual-naming compatibility aliases
OpsLocation = OpsLocationModel
OpsFacility = OpsFacilityModel
OpsDemand = OpsDemandModel
OpsForecast = OpsForecastModel
OpsSupplyPlan = OpsSupplyPlanModel
OpsSupplier = OpsSupplierModel
OpsSourcingEvent = OpsSourcingEventModel
OpsPurchaseOrder = OpsPurchaseOrderModel
OpsGoodsReceipt = OpsGoodsReceiptModel
OpsInventoryItem = OpsInventoryItemModel
OpsWarehouse = OpsWarehouseModel
OpsOrder = OpsOrderModel
OpsShipment = OpsShipmentModel
OpsVehicle = OpsVehicleModel
OpsWorkforceCapacity = OpsWorkforceCapacityModel
OpsShiftSchedule = OpsShiftScheduleModel
OpsProductionOrder = OpsProductionOrderModel
OpsQualityEvent = OpsQualityEventModel
OpsAsset = OpsAssetModel
OpsDigitalTwinNode = OpsDigitalTwinNodeModel
OpsScenarioSimulation = OpsScenarioSimulationModel
OpsException = OpsExceptionModel
