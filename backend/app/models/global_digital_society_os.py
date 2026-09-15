"""
Phase 93 — Global Digital Society, Autonomous Organizations, AI-Native Institutions & Networked Economic Coordination Models
"""

import uuid
import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class DigitalIdentityNode(Base):
    """Interoperable digital identities for people, organizations, agents, services, devices, and projects."""
    __tablename__ = "digital_identity_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    entity_name = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False, default="person")  # person, organization, agent, service, device, project
    verification_level = Column(String, default="STRONG_VERIFIED")  # UNVERIFIED, VERIFIED, ORG_VERIFIED, CREDENTIAL_VERIFIED, STRONG_VERIFIED
    verifiable_credentials = Column(JSON, default=list)
    ssi_disclosure_policy = Column(JSON, default=dict)
    owner_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalPersonaConfig(Base):
    """User AI representation settings, action levels, and mandatory representation disclosure flags."""
    __tablename__ = "digital_persona_configs"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    persona_name = Column(String, nullable=False)
    action_level = Column(String, default="REQUEST_APPROVAL")  # OBSERVE, SUGGEST, DRAFT, REQUEST_APPROVAL, EXECUTE
    allowed_domains = Column(JSON, default=list)  # Communication, Scheduling, Research, Negotiation, Admin
    explicit_permissions = Column(JSON, default=dict)
    representation_disclosure_required = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AiNativeOrgNode(Base):
    """AI-native organization graph, department hierarchy, dynamic org chart, and RACI matrix."""
    __tablename__ = "ai_native_org_nodes"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    org_name = Column(String, nullable=False, index=True)
    departments = Column(JSON, default=list)
    roles_matrix = Column(JSON, default=list)  # RACI Responsibility Matrix
    ai_roles = Column(JSON, default=list)  # Research Agent, Finance Analyst, Ops Agent, Support Agent, Engineering Agent, Compliance Agent
    policy_hierarchy_level = Column(String, default="ORG_POLICY")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AutonomousWorkflowContract(Base):
    """Autonomous workflow contracts, triggers, permissions, spending caps, and kill-switch state."""
    __tablename__ = "autonomous_workflow_contracts"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    org_id = Column(String, nullable=False, index=True)
    workflow_name = Column(String, nullable=False)
    trigger_type = Column(String, default="EVENT_TRIGGERED")
    budget_limit_usd = Column(Float, default=10000.0)
    sandbox_simulated = Column(Boolean, default=True)
    human_approval_required = Column(Boolean, default=True)
    is_paused = Column(Boolean, default=False)
    global_kill_switch_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalGovernancePolicy(Base):
    """Governance policies, dual-approval (four-eyes) rules, segregation of duties, and proposals."""
    __tablename__ = "digital_governance_policies"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    policy_name = Column(String, nullable=False)
    policy_scope = Column(String, default="GLOBAL")  # GLOBAL, ORG, DEPT, PROJECT, AGENT
    four_eyes_required = Column(Boolean, default=True)
    segregation_of_duties = Column(JSON, default=dict)
    proposals_history = Column(JSON, default=list)
    effective_date = Column(DateTime, default=datetime.datetime.utcnow)

class AgentEconomyMarketplaceRecord(Base):
    """Agent-to-service marketplace transactions, agent budgets, fraud alerts, and digital escrow."""
    __tablename__ = "agent_economy_marketplace_records"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, nullable=False, index=True)
    service_id = Column(String, nullable=False)
    transaction_amount_usd = Column(Float, default=0.0)
    agent_budget_cap_usd = Column(Float, default=5000.0)
    fraud_risk_score = Column(Float, default=0.02)
    escrow_status = Column(String, default="RELEASED")  # PENDING, HELD, RELEASED, DISPUTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class DigitalSocietyGovernanceAudit(Base):
    """Algorithmic accountability, agent quarantine records, digital immune alerts, and emergency audit trails."""
    __tablename__ = "digital_society_governance_audits"
    __table_args__ = {"extend_existing": True}

    id = Column(String, primary_key=True, default=generate_uuid)
    event_type = Column(String, nullable=False)  # ALGORITHMIC_ACCOUNTABILITY, AGENT_QUARANTINE, IMMUNE_ALERT, EMERGENCY_MODE
    target_entity_id = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    human_override_engaged = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
