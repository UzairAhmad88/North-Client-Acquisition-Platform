"""
Phase 86: Enterprise AI Workforce Marketplace, Agent Skills, Capability Exchange & Autonomous Service Economy Database Models.
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime
import uuid

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class MarketplaceCapabilityListing(Base):
    __tablename__ = "marketplace_capability_listings"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False) # AI Employees, Agents, Agent Teams, Skills, Services, Workflows
    description = Column(Text, nullable=True)
    provider_id = Column(String, nullable=False)
    version = Column(String, default="v1.0.0")
    certification_status = Column(String, default="CERTIFIED") # Unverified, Tested, Certified, Restricted, Suspended
    trust_score = Column(Float, default=98.5)
    hourly_rate_usd = Column(Float, default=0.0)
    per_task_cost_usd = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")
    rating = Column(Float, default=4.9)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class MarketplaceSkill(Base):
    __tablename__ = "marketplace_skills"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False) # Research, Coding, Data Analysis, Security, Operations
    description = Column(Text, nullable=True)
    author = Column(String, nullable=False)
    version = Column(String, default="v1.0.0")
    required_tools = Column(JSON, default=list)
    success_rate = Column(Float, default=99.4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MarketplaceService(Base):
    __tablename__ = "marketplace_services"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    service_name = Column(String, nullable=False, index=True)
    purpose = Column(Text, nullable=False)
    input_schema = Column(JSON, default=dict)
    output_schema = Column(JSON, default=dict)
    sla_target_mins = Column(Float, default=15.0)
    pricing_model = Column(String, default="PER_TASK") # FIXED_PRICE, PER_TASK, PER_TOKEN, SUBSCRIPTION
    price_usd = Column(Float, default=5.00)
    owner = Column(String, nullable=False)
    status = Column(String, default="PUBLISHED")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MarketplaceAgentTeam(Base):
    __tablename__ = "marketplace_agent_teams"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    team_name = Column(String, nullable=False, index=True)
    objective = Column(Text, nullable=False)
    manager_agent_id = Column(String, nullable=False)
    member_agent_ids = Column(JSON, default=list)
    monthly_budget_cap_usd = Column(Float, default=5000.00)
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MarketplaceOrder(Base):
    __tablename__ = "marketplace_orders"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    service_id = Column(String, ForeignKey("marketplace_services.id"), nullable=False)
    requester = Column(String, nullable=False)
    assigned_agent_id = Column(String, nullable=False)
    total_cost_usd = Column(Float, default=5.00)
    status = Column(String, default="DELIVERED") # ORDERED, PROCESSING, VERIFYING, DELIVERED, DISPUTED
    sla_met = Column(Boolean, default=True)
    ordered_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class MarketplaceCertification(Base):
    __tablename__ = "marketplace_certifications"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    capability_id = Column(String, ForeignKey("marketplace_capability_listings.id"), nullable=False)
    certification_level = Column(String, default="ENTERPRISE_GOLD")
    security_score = Column(Float, default=99.8)
    safety_score = Column(Float, default=100.0)
    certified_by = Column(String, default="Uzaii AI Governance Board")
    certified_at = Column(DateTime, default=datetime.datetime.utcnow)

class MarketplaceAgentTask(Base):
    __tablename__ = "marketplace_agent_tasks"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)
    autonomy_level = Column(Integer, default=2)
    status = Column(String, default="COMPLETED")
    target_scope = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
