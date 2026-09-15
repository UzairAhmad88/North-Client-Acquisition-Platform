"""
Phase 87: Enterprise AI Federation, Cross-Organization Agent Networks, Autonomous B2B Collaboration & Agent-to-Agent Commerce Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class FederatedOrganization(Base):
    __tablename__ = "federated_organizations"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=False)
    industry = Column(String, default="Technology & Enterprise Services")
    federation_status = Column(String, default="ACTIVE") # Requested, Pending, Approved, Active, Restricted, Suspended
    trust_score = Column(Float, default=99.1)
    verification_status = Column(String, default="VERIFIED")
    security_attestation = Column(String, default="ISO27001_SOC2_TYPE2")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class FederatedIdentity(Base):
    __tablename__ = "federated_identities"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("federated_organizations.id"), nullable=False)
    agent_id = Column(String, nullable=False, index=True)
    agent_name = Column(String, nullable=False)
    credential_type = Column(String, default="MTLS_JWT_CERTIFICATE")
    scopes = Column(JSON, default=list)
    status = Column(String, default="ACTIVE")
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FederationContract(Base):
    __tablename__ = "federation_contracts"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    contract_number = Column(String, nullable=False, index=True)
    buyer_org_id = Column(String, ForeignKey("federated_organizations.id"), nullable=False)
    seller_org_id = Column(String, ForeignKey("federated_organizations.id"), nullable=False)
    service_scope = Column(Text, nullable=False)
    max_value_usd = Column(Float, default=10000.00)
    sla_target_percent = Column(Float, default=99.9)
    human_approval_required = Column(Boolean, default=True)
    status = Column(String, default="ACTIVE") # DRAFT, NEGOTIATING, APPROVED, ACTIVE, EXPIRED, TERMINATED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FederationNegotiation(Base):
    __tablename__ = "federation_negotiations"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    contract_id = Column(String, ForeignKey("federation_contracts.id"), nullable=True)
    buyer_agent_id = Column(String, nullable=False)
    seller_agent_id = Column(String, nullable=False)
    proposed_price_usd = Column(Float, default=50.00)
    proposed_deadline_hours = Column(Integer, default=24)
    negotiation_status = Column(String, default="AGREED") # OFFER, COUNTER, AGREED, REJECTED, ESCALATED
    confidence_score = Column(Float, default=0.98)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class FederationWorkOrder(Base):
    __tablename__ = "federation_work_orders"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    work_order_number = Column(String, nullable=False, index=True)
    contract_id = Column(String, ForeignKey("federation_contracts.id"), nullable=False)
    executing_agent_id = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    price_usd = Column(Float, default=50.00)
    status = Column(String, default="DELIVERED") # CREATED, ACCEPTED, RUNNING, DELIVERED, SETTLED, DISPUTED
    output_sanitized = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class FederationPayment(Base):
    __tablename__ = "federation_payments"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    work_order_id = Column(String, ForeignKey("federation_work_orders.id"), nullable=False)
    amount_usd = Column(Float, default=50.00)
    payment_status = Column(String, default="SETTLED") # PENDING, AUTHORIZED, SETTLED, REFUNDED, DISPUTED
    transaction_reference = Column(String, nullable=False)
    processed_at = Column(DateTime, default=datetime.datetime.utcnow)

class FederationAgentTask(Base):
    __tablename__ = "federation_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_level = Column(Integer, default=2)
    status = Column(String, default="COMPLETED")
    target_scope = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
