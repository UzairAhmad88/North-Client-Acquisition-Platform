"""
Phase 92 — Global Human-AI Collaboration Network, Collective Intelligence, Expert Networks & Civilization-Scale Problem Solving Models
"""

import uuid
from datetime import datetime, timezone
from app.models.base import Base
from sqlalchemy import Column, String, DateTime, Float, Boolean, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship


class CollaborationIdentityNode(Base):
    """Universal participant identity for humans, experts, organizations, and AI agents."""
    __tablename__ = "collaboration_identity_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    participant_name = Column(String(255), nullable=False)
    participant_type = Column(String(64), nullable=False, default="human")  # human, expert, team, organization, ai_agent, research_group, community
    organization_id = Column(String(255), nullable=True)
    capabilities = Column(JSON, default=list)  # list of skill/capability strings
    roles = Column(JSON, default=list)  # researcher, analyst, planner, reviewer, engineer, coordinator, auditor
    permissions = Column(JSON, default=dict)
    verification_status = Column(String(64), default="unverified")  # self_declared, documented, demonstrated, verified, institutional
    availability_status = Column(String(64), default="available")  # available, busy, offline, contracting_only
    trust_score = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class ExpertiseGraphNode(Base):
    """Global expertise network mapping experts to domains, research, publications, and verified evidence."""
    __tablename__ = "expertise_graph_nodes"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    expert_identity_id = Column(String(36), nullable=False)
    domain = Column(String(255), nullable=False)
    subdomain = Column(String(255), nullable=True)
    skill_level = Column(String(64), default="expert")  # learner, practitioner, advanced_practitioner, expert, researcher_leader
    evidence_score = Column(Float, default=0.95)
    verification_level = Column(String(64), default="verified")
    publications_count = Column(Float, default=0.0)
    projects_count = Column(Float, default=0.0)
    conflict_constraints = Column(JSON, default=list)  # non-compete, organizational conflicts
    complementarity_tags = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CollaborationWorkspaceRoom(Base):
    """Shared collaboration workspaces and project rooms connecting questions, decisions, tasks, and results."""
    __tablename__ = "collaboration_workspace_rooms"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_name = Column(String(255), nullable=False)
    project_scope = Column(String(255), nullable=False)  # scientific_research, product_dev, strategic_planning, civilization_workbench
    owner_identity_id = Column(String(36), nullable=False)
    participant_ids = Column(JSON, default=list)
    agent_ids = Column(JSON, default=list)
    knowledge_graph_snapshot = Column(JSON, default=dict)  # Question -> Discussion -> Decision -> Task -> Result -> Evidence
    collaborative_memory = Column(JSON, default=dict)
    memory_owner_id = Column(String(36), nullable=True)
    memory_access_policy = Column(JSON, default=dict)
    memory_version = Column(String(32), default="1.0.0")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class StructuredDecisionRecord(Base):
    """Structured decision records capturing options, evidence, assumptions, approvals, quality score, and revisions."""
    __tablename__ = "structured_decision_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), nullable=False)
    decision_title = Column(String(255), nullable=False)
    options_evaluated = Column(JSON, default=list)
    chosen_option = Column(String(255), nullable=False)
    evidence_attached = Column(JSON, default=list)
    assumptions_recorded = Column(JSON, default=list)
    participants_signed = Column(JSON, default=list)
    human_approved = Column(Boolean, default=True)
    decision_quality_score = Column(Float, default=0.92)
    revision_history = Column(JSON, default=list)
    status = Column(String(64), default="active")  # active, under_revision, superseded, revoked
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class ContributionAttributionRecord(Base):
    """Tracks Human, AI, and Hybrid contributions, collaborative edit suggestions, dissent, and argument maps."""
    __tablename__ = "contribution_attribution_records"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), nullable=False)
    artifact_id = Column(String(255), nullable=False)
    contribution_type = Column(String(64), nullable=False)  # human, ai, hybrid
    author_id = Column(String(36), nullable=False)
    agent_id = Column(String(36), nullable=True)
    attribution_hash = Column(String(128), nullable=False)
    argument_map = Column(JSON, default=dict)  # Claim, Evidence, Counterargument, Response, Conclusion
    dissent_records = Column(JSON, default=list)  # Preserved minority opinions
    fact_opinion_breakdown = Column(JSON, default=dict)  # Fact, Inference, Opinion, Hypothesis
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class FederatedSimulationWorkspace(Base):
    """Cross-institution collaboration, federated scientific computation, digital twin scenarios & Red/Blue team synthesis."""
    __tablename__ = "federated_simulation_workspaces"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_name = Column(String(255), nullable=False)
    participating_institutions = Column(JSON, default=list)
    data_isolation_rules = Column(JSON, default=dict)
    federated_compute_jobs = Column(JSON, default=list)
    shared_digital_twin_id = Column(String(255), nullable=True)
    scenario_type = Column(String(64), default="baseline")  # baseline, alternative, stress, extreme, recovery
    scenario_assumptions = Column(JSON, default=list)
    red_blue_team_synthesis = Column(JSON, default=dict)  # Strengths, Weaknesses, Risks, Mitigations
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class CollaborationGovernanceAudit(Base):
    """Zero-trust collaboration security, data room audit log, MCDA weight transparency, secret voting, and postmortems."""
    __tablename__ = "collaboration_governance_audits"
    __table_args__ = {'extend_existing': True}

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = Column(String(36), nullable=True)
    event_type = Column(String(128), nullable=False)  # zero_trust_access, data_room_audit, mcda_vote, postmortem_logged, workbench_run
    participant_id = Column(String(36), nullable=False)
    details = Column(JSON, default=dict)
    human_oversight_verified = Column(Boolean, default=True)
    zero_trust_validated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
