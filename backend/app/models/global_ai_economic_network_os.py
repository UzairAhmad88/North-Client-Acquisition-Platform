"""
Phase 88: Global AI Economic Network, Autonomous Enterprise-to-Enterprise Ecosystem & Machine-Native Business Infrastructure Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class EconomicNetworkEntity(Base):
    __tablename__ = "economic_network_entities"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    entity_type = Column(String, default="ORGANIZATION") # ORGANIZATION, AGENT, SUPPLIER, CUSTOMER, PROVIDER
    domain = Column(String, nullable=False)
    trust_score = Column(Float, default=99.5)
    resilience_score = Column(Float, default=98.4)
    active_contracts_count = Column(Integer, default=12)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class EconomicProductCatalog(Base):
    __tablename__ = "economic_product_catalogs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    sku = Column(String, nullable=False, index=True)
    provider_entity_id = Column(String, ForeignKey("economic_network_entities.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, default="AI_SERVICE") # AI_SERVICE, DIGITAL_PRODUCT, COMPUTE, DATA_SERVICE, OUTCOME_CONTRACT
    pricing_model = Column(String, default="DYNAMIC_USAGE") # FIXED, USAGE, DYNAMIC, OUTCOME_BASED
    base_price_usd = Column(Float, default=120.00)
    sla_guarantee_percent = Column(Float, default=99.9)
    status = Column(String, default="AVAILABLE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EconomicCommerceOrder(Base):
    __tablename__ = "economic_commerce_orders"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    order_number = Column(String, nullable=False, index=True)
    buyer_entity_id = Column(String, ForeignKey("economic_network_entities.id"), nullable=False)
    seller_entity_id = Column(String, ForeignKey("economic_network_entities.id"), nullable=False)
    product_id = Column(String, ForeignKey("economic_product_catalogs.id"), nullable=False)
    agreed_price_usd = Column(Float, default=120.00)
    autonomy_tier = Column(Integer, default=4) # Tier 0 (Human) to Tier 5 (High Autonomy)
    status = Column(String, default="FULFILLED") # DRAFT, NEGOTIATING, SUBMITTED, ACCEPTED, FULFILLED, SETTLED, DISPUTED
    is_synthetic_simulation = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EconomicRiskGraphNode(Base):
    __tablename__ = "economic_risk_graph_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    entity_id = Column(String, ForeignKey("economic_network_entities.id"), nullable=False)
    risk_category = Column(String, default="CONCENTRATION_RISK") # CONCENTRATION, COUNTERPARTY, FX, SUPPLY_CHAIN, CYBER
    risk_score = Column(Float, default=15.2) # Low score is good
    financial_exposure_usd = Column(Float, default=45000.00)
    mitigation_strategy = Column(String, default="MULTI_PROVIDER_FAILOVER")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EconomicSupplyChainTwin(Base):
    __tablename__ = "economic_supply_chain_twins"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    node_name = Column(String, nullable=False)
    upstream_provider_id = Column(String, nullable=False)
    downstream_consumer_id = Column(String, nullable=False)
    dependency_criticality = Column(String, default="HIGH") # CRITICAL, HIGH, MODERATE, LOW
    simulation_state = Column(JSON, default=dict)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class EconomicDisputeEvidence(Base):
    __tablename__ = "economic_dispute_evidences"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, ForeignKey("economic_commerce_orders.id"), nullable=False)
    claimant_entity_id = Column(String, nullable=False)
    evidence_hash = Column(String, nullable=False)
    resolution_recommendation = Column(String, default="REFUND_CREDIT")
    status = Column(String, default="UNDER_HUMAN_REVIEW")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EconomicAgentTask(Base):
    __tablename__ = "economic_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_tier = Column(Integer, default=4)
    status = Column(String, default="COMPLETED")
    governance_result = Column(String, default="PASSED_POLICY_CHECK")
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
