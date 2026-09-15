"""
Phase 71: Autonomous Supply Chain, Logistics Intelligence, Warehousing,
Fleet Operations & Global Physical Commerce Models.
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


# 1. Suppliers & Performance
class ScSupplierModel(Base):
    """Tier 1/2/3 commercial suppliers, global manufacturers, and distributors."""
    __tablename__ = "sc_suppliers"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    supplier_code = Column(String(64), nullable=False, unique=True, index=True)
    company_name = Column(String(128), nullable=False)
    tier = Column(String(16), nullable=False, default="TIER_1")  # TIER_1, TIER_2, TIER_3
    country_code = Column(String(8), nullable=False, default="US")
    on_time_delivery_rate = Column(Float, nullable=False, default=96.5)
    quality_defect_rate_ppm = Column(Float, nullable=False, default=18.0)
    risk_score = Column(Float, nullable=False, default=14.2)  # 0 to 100 (lower is better)
    financial_health_rating = Column(String(16), nullable=False, default="AAA")
    compliance_status = Column(String(32), nullable=False, default="COMPLIANT")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScSupplierContractModel(Base):
    """Supplier procurement contracts, terms, and minimum order commitments."""
    __tablename__ = "sc_supplier_contracts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    contract_code = Column(String(64), nullable=False, unique=True, index=True)
    supplier_id = Column(String(64), nullable=False, index=True)
    currency = Column(String(8), nullable=False, default="USD")
    annual_committed_spend = Column(Float, nullable=False, default=500000.0)
    payment_terms_days = Column(Integer, nullable=False, default=30)
    lead_time_days = Column(Integer, nullable=False, default=14)
    is_active = Column(Boolean, nullable=False, default=True)
    valid_until = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 2. Products, Materials & Bill of Materials (BOM)
class ScProductModel(Base):
    """Finished goods, SKUs, physical commerce catalog items."""
    __tablename__ = "sc_products"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    sku = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False, default="ELECTRONICS")
    unit_of_measure = Column(String(16), nullable=False, default="EACH")
    weight_kg = Column(Float, nullable=False, default=1.2)
    volume_cbm = Column(Float, nullable=False, default=0.004)
    storage_temp_min_c = Column(Float, nullable=True)
    storage_temp_max_c = Column(Float, nullable=True)
    base_price_usd = Column(Float, nullable=False, default=199.99)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScBillOfMaterialsModel(Base):
    """Multi-level BOM mapping finished products to sub-assemblies and raw materials."""
    __tablename__ = "sc_bom"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    parent_product_id = Column(String(64), nullable=False, index=True)
    component_sku = Column(String(64), nullable=False, index=True)
    quantity_required = Column(Float, nullable=False, default=1.0)
    scrap_rate_pct = Column(Float, nullable=False, default=1.5)
    bom_level = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 3. Procurement & Purchase Orders
class ScPurchaseOrderModel(Base):
    """Commercial purchase orders issued to suppliers."""
    __tablename__ = "sc_purchase_orders"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    po_number = Column(String(64), nullable=False, unique=True, index=True)
    supplier_id = Column(String(64), nullable=False, index=True)
    destination_warehouse_id = Column(String(64), nullable=False, index=True)
    total_amount_usd = Column(Float, nullable=False, default=0.0)
    approval_status = Column(String(32), nullable=False, default="PENDING")  # PENDING, APPROVED, REJECTED
    order_status = Column(String(32), nullable=False, default="DRAFT")  # DRAFT, ISSUED, IN_TRANSIT, FULFILLED
    expected_delivery_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 4. Inventory, Lots & Movements
class ScInventoryItemModel(Base):
    """Real-time inventory levels across multi-echelon network nodes."""
    __tablename__ = "sc_inventory"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    sku = Column(String(64), nullable=False, index=True)
    warehouse_id = Column(String(64), nullable=False, index=True)
    quantity_on_hand = Column(Float, nullable=False, default=0.0)
    quantity_reserved = Column(Float, nullable=False, default=0.0)
    quantity_available = Column(Float, nullable=False, default=0.0)
    quantity_in_transit = Column(Float, nullable=False, default=0.0)
    safety_stock_level = Column(Float, nullable=False, default=50.0)
    reorder_point = Column(Float, nullable=False, default=120.0)
    stockout_risk_score = Column(Float, nullable=False, default=0.05)
    last_counted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScInventoryMovementModel(Base):
    """Immutable ledger of all inventory picks, receipts, transfers, and adjustments."""
    __tablename__ = "sc_inventory_movements"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    movement_type = Column(String(32), nullable=False)  # RECEIPT, PUTAWAY, PICK, SHIP, TRANSFER, ADJUSTMENT
    sku = Column(String(64), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    source_location = Column(String(64), nullable=True)
    destination_location = Column(String(64), nullable=True)
    reference_id = Column(String(64), nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 5. Demand & Forecasting
class ScDemandForecastModel(Base):
    """AI-generated multi-horizon demand projections with confidence bands."""
    __tablename__ = "sc_demand_forecasts"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    sku = Column(String(64), nullable=False, index=True)
    region = Column(String(32), nullable=False, default="GLOBAL")
    forecast_horizon_days = Column(Integer, nullable=False, default=30)
    forecasted_units_p50 = Column(Float, nullable=False)
    forecasted_units_p10 = Column(Float, nullable=False)
    forecasted_units_p90 = Column(Float, nullable=False)
    forecast_accuracy_mape = Column(Float, nullable=False, default=4.2)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 6. Warehouses & Fulfillment Tasks
class ScWarehouseModel(Base):
    """Fulfillment centers, regional distribution hubs, and automated cross-docks."""
    __tablename__ = "sc_warehouses"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    warehouse_code = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    total_capacity_cbm = Column(Float, nullable=False, default=120000.0)
    used_capacity_cbm = Column(Float, nullable=False, default=84000.0)
    utilization_pct = Column(Float, nullable=False, default=70.0)
    has_robotics_fleet = Column(Boolean, nullable=False, default=True)
    has_cold_storage = Column(Boolean, nullable=False, default=True)
    status = Column(String(32), nullable=False, default="OPERATIONAL")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScPickTaskModel(Base):
    """Automated and worker wave/batch pick tasks inside fulfillment centers."""
    __tablename__ = "sc_pick_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    task_code = Column(String(64), nullable=False, unique=True, index=True)
    order_id = Column(String(64), nullable=False, index=True)
    sku = Column(String(64), nullable=False, index=True)
    quantity = Column(Float, nullable=False, default=1.0)
    bin_location = Column(String(64), nullable=False)
    assigned_entity = Column(String(64), nullable=False, default="AMR_ROBOT_04")
    priority = Column(String(16), nullable=False, default="HIGH")
    status = Column(String(32), nullable=False, default="QUEUED")  # QUEUED, IN_PROGRESS, PICKED, VERIFIED
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 7. Transportation, Fleet & Shipments
class ScCarrierModel(Base):
    """Logistics carriers, 3PL partners, rail, maritime, and air freight providers."""
    __tablename__ = "sc_carriers"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    carrier_code = Column(String(64), nullable=False, unique=True, index=True)
    name = Column(String(128), nullable=False)
    transport_mode = Column(String(32), nullable=False, default="ROAD_FREIGHT")  # ROAD, AIR, OCEAN, RAIL
    on_time_transit_pct = Column(Float, nullable=False, default=97.8)
    claims_rate_pct = Column(Float, nullable=False, default=0.12)
    average_rate_per_km_usd = Column(Float, nullable=False, default=1.85)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScVehicleModel(Base):
    """Fleet vehicles, semi-trucks, electric vans, and autonomous freight haulers."""
    __tablename__ = "sc_vehicles"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    vehicle_vin = Column(String(64), nullable=False, unique=True, index=True)
    vehicle_type = Column(String(32), nullable=False, default="ELECTRIC_SEMI")
    fuel_or_battery_pct = Column(Float, nullable=False, default=88.5)
    max_payload_kg = Column(Float, nullable=False, default=24000.0)
    telemetry_connected = Column(Boolean, nullable=False, default=True)
    operational_status = Column(String(32), nullable=False, default="EN_ROUTE")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScShipmentModel(Base):
    """Consolidated customer shipments, manifest, and tracking lifecycle."""
    __tablename__ = "sc_shipments"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    tracking_number = Column(String(64), nullable=False, unique=True, index=True)
    order_id = Column(String(64), nullable=False, index=True)
    carrier_id = Column(String(64), nullable=False, index=True)
    origin_hub = Column(String(64), nullable=False)
    destination_address = Column(String(256), nullable=False)
    current_status = Column(String(32), nullable=False, default="IN_TRANSIT")
    is_cold_chain = Column(Boolean, nullable=False, default=False)
    estimated_arrival = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 8. Sales Orders, Allocations & Returns
class ScSalesOrderModel(Base):
    """Customer sales orders, fulfillment priority, and payment status."""
    __tablename__ = "sc_orders"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    order_number = Column(String(64), nullable=False, unique=True, index=True)
    customer_id = Column(String(64), nullable=False, index=True)
    total_value_usd = Column(Float, nullable=False, default=0.0)
    service_level_target = Column(String(32), nullable=False, default="SAME_DAY")
    fulfillment_status = Column(String(32), nullable=False, default="ALLOCATED")
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScReturnRequestModel(Base):
    """RMA return requests, inspection grading, and reverse logistics disposition."""
    __tablename__ = "sc_returns"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    return_code = Column(String(64), nullable=False, unique=True, index=True)
    order_id = Column(String(64), nullable=False, index=True)
    return_reason = Column(String(64), nullable=False)
    disposition_state = Column(String(32), nullable=False, default="RESTOCK")  # RESTOCK, REFURBISH, RECYCLE, DISPOSE
    refund_issued = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# 9. Disruption, Resilience & Digital Twin
class ScSupplyChainDisruptionModel(Base):
    """Real-time supply chain disruptions (weather, strikes, geopolitical, port congestion)."""
    __tablename__ = "sc_disruptions"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    disruption_code = Column(String(64), nullable=False, unique=True, index=True)
    severity = Column(String(16), nullable=False, default="HIGH")
    category = Column(String(32), nullable=False)  # PORT_CONGESTION, SEVERE_WEATHER, SUPPLIER_INSOLVENCY, LABOR_STRIKE
    impacted_nodes_count = Column(Integer, nullable=False, default=3)
    estimated_revenue_at_risk_usd = Column(Float, nullable=False, default=450000.0)
    mitigation_plan_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScDigitalTwinModel(Base):
    """End-to-end supply chain digital twin modeling flows, buffers, and transit times."""
    __tablename__ = "sc_digital_twins"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    twin_version = Column(String(32), nullable=False, default="v2.0")
    synchronization_status = Column(String(32), nullable=False, default="SYNCHRONIZED")
    network_nodes_count = Column(Integer, nullable=False, default=84)
    active_shipments_simulated = Column(Integer, nullable=False, default=3420)
    resilience_score = Column(Float, nullable=False, default=94.6)
    last_synchronized_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


class ScAgentRunModel(Base):
    """Autonomous supply chain agent decision records and audit traces."""
    __tablename__ = "sc_agent_runs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(64), primary_key=True)
    tenant_id = Column(String(64), nullable=False, index=True)
    agent_name = Column(String(64), nullable=False, index=True)
    action_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="COMPLETED")
    dry_run = Column(Boolean, nullable=False, default=True)
    execution_result = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))


# Convenience Aliases
ScSupplier = ScSupplierModel
ScSupplierContract = ScSupplierContractModel
ScProduct = ScProductModel
ScBillOfMaterials = ScBillOfMaterialsModel
ScPurchaseOrder = ScPurchaseOrderModel
ScInventoryItem = ScInventoryItemModel
ScInventoryMovement = ScInventoryMovementModel
ScDemandForecast = ScDemandForecastModel
ScWarehouse = ScWarehouseModel
ScPickTask = ScPickTaskModel
ScCarrier = ScCarrierModel
ScVehicle = ScVehicleModel
ScShipment = ScShipmentModel
ScSalesOrder = ScSalesOrderModel
ScReturnRequest = ScReturnRequestModel
ScSupplyChainDisruption = ScSupplyChainDisruptionModel
ScDigitalTwin = ScDigitalTwinModel
ScAgentRun = ScAgentRunModel
