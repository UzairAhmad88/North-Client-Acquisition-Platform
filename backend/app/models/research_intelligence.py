"""
SQLAlchemy ORM models for Phase 54 — Unified Autonomous Research, Intelligence & Continuous Discovery Engine.
"""

from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ResearchWorkspaceModel(BaseModel):
    """Core research workspace container."""
    __tablename__ = "research_workspaces"

    title = Column(String(255), nullable=False)
    research_question = Column(Text, nullable=False)
    objective = Column(Text, nullable=True)
    research_type = Column(String(64), nullable=False, default="MARKET")  # MARKET, COMPETITIVE, TECHNOLOGY, AI, SECURITY, REGULATORY
    status = Column(String(32), nullable=False, default="PLANNED")  # DRAFT, PLANNED, RESEARCHING, VALIDATING, SYNTHESIZING, REVIEW, COMPLETED, MONITORING, ARCHIVED
    owner_id = Column(String(128), nullable=False)
    scope = Column(JSON, nullable=True, default=dict)  # {"geography": ..., "time_range": ..., "entities": ...}
    confidence_score = Column(Float, nullable=False, default=0.8)
    version = Column(Integer, nullable=False, default=1)
    meta_info = Column(JSON, nullable=True, default=dict)

    # Relationships
    tasks = relationship("ResearchTaskModel", back_populates="workspace", cascade="all, delete-orphan")
    sources = relationship("ResearchSourceModel", back_populates="workspace", cascade="all, delete-orphan")
    entities = relationship("ResearchEntityModel", back_populates="workspace", cascade="all, delete-orphan")
    facts = relationship("ResearchFactModel", back_populates="workspace", cascade="all, delete-orphan")
    claims = relationship("ResearchClaimModel", back_populates="workspace", cascade="all, delete-orphan")
    conflicts = relationship("ResearchConflictModel", back_populates="workspace", cascade="all, delete-orphan")
    trends = relationship("ResearchTrendModel", back_populates="workspace", cascade="all, delete-orphan")
    syntheses = relationship("ResearchSynthesisModel", back_populates="workspace", cascade="all, delete-orphan")
    reports = relationship("ResearchReportModel", back_populates="workspace", cascade="all, delete-orphan")
    monitoring_rules = relationship("ResearchMonitoringRuleModel", back_populates="workspace", cascade="all, delete-orphan")


class ResearchTaskModel(BaseModel):
    """Sub-question research task decomposed by the planner."""
    __tablename__ = "research_tasks"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    task_type = Column(String(64), nullable=False, default="SOURCE_DISCOVERY")
    priority = Column(String(32), nullable=False, default="MEDIUM")
    assigned_worker = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="QUEUED")  # QUEUED, RUNNING, COMPLETED, FAILED, REVIEW_REQUIRED
    budget_tokens = Column(Integer, nullable=False, default=10000)
    result_summary = Column(Text, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="tasks")


class ResearchSourceModel(BaseModel):
    """Registered and validated research source with trust rating."""
    __tablename__ = "research_sources"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    url_or_reference = Column(String(512), nullable=False)
    source_type = Column(String(64), nullable=False, default="PUBLIC_WEB")  # PRIMARY, OFFICIAL, ACADEMIC, GOVERNMENT, COMMUNITY
    publisher = Column(String(255), nullable=True)
    author = Column(String(255), nullable=True)
    authority_score = Column(Float, nullable=False, default=0.7)  # 0.0 to 1.0
    reliability = Column(String(32), nullable=False, default="MEDIUM_TRUST")  # OFFICIAL, HIGH_TRUST, MEDIUM_TRUST, LOW_TRUST
    freshness = Column(String(32), nullable=False, default="CURRENT")
    content_hash = Column(String(64), nullable=True)
    status = Column(String(32), nullable=False, default="VALIDATED")
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="sources")


class ResearchEntityModel(BaseModel):
    """Resolved entity (company, product, technology, person, regulation)."""
    __tablename__ = "research_entities"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    entity_type = Column(String(64), nullable=False)  # COMPANY, PRODUCT, TECHNOLOGY, REGULATION, PERSON, MARKET
    canonical_id = Column(String(128), nullable=True)
    aliases = Column(JSON, nullable=True, default=list)
    attributes = Column(JSON, nullable=True, default=dict)
    confidence = Column(Float, nullable=False, default=0.9)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="entities")


class ResearchFactModel(BaseModel):
    """Extracted atomic fact with source provenance."""
    __tablename__ = "research_facts"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(String(64), nullable=True)
    claim = Column(Text, nullable=False)
    value_extracted = Column(Text, nullable=True)
    fact_status = Column(String(32), nullable=False, default="VERIFIED")  # OBSERVED, VERIFIED, CORROBORATED, CONFLICTED, OUTDATED
    confidence = Column(Float, nullable=False, default=0.85)
    provenance = Column(String(255), nullable=True)
    observed_date = Column(String(32), nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="facts")


class ResearchClaimModel(BaseModel):
    """Synthesized claim subject to independent corroboration."""
    __tablename__ = "research_claims"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    claim_text = Column(Text, nullable=False)
    verification_status = Column(String(32), nullable=False, default="SUPPORTED")  # SUPPORTED, PARTIALLY_SUPPORTED, CONFLICTED, UNSUPPORTED, UNKNOWN
    independent_sources_count = Column(Integer, nullable=False, default=1)
    confidence = Column(Float, nullable=False, default=0.8)
    supporting_evidence = Column(JSON, nullable=True, default=list)
    contradicting_evidence = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="claims")


class ResearchConflictModel(BaseModel):
    """Explicitly detected contradiction between research sources."""
    __tablename__ = "research_conflicts"
    __table_args__ = {"extend_existing": True}

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    source_a_id = Column(String(64), nullable=False)
    claim_a = Column(Text, nullable=False)
    source_b_id = Column(String(64), nullable=False)
    claim_b = Column(Text, nullable=False)
    possible_explanation = Column(Text, nullable=True)
    resolution_status = Column(String(32), nullable=False, default="SURFACED")  # SURFACED, RESOLVED, ACCEPTED_UNCERTAINTY
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="conflicts")


class ResearchTrendModel(BaseModel):
    """Detected market or technology trend."""
    __tablename__ = "research_trends"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    trend_name = Column(String(255), nullable=False)
    trend_type = Column(String(64), nullable=False, default="EMERGING")  # EMERGING, ACCELERATING, STABLE, DECLINING, STRUCTURAL
    momentum_score = Column(Float, nullable=False, default=0.7)
    key_drivers = Column(JSON, nullable=True, default=list)
    impact_assessment = Column(Text, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="trends")


class ResearchCompetitorProfileModel(BaseModel):
    """Structured competitive intelligence profile."""
    __tablename__ = "research_competitor_profiles"

    company_name = Column(String(255), nullable=False, unique=True)
    market_position = Column(String(64), nullable=False, default="CHALLENGER")  # LEADER, CHALLENGER, NICHE, EMERGING
    products_offered = Column(JSON, nullable=True, default=list)
    pricing_signals = Column(JSON, nullable=True, default=dict)
    strengths = Column(JSON, nullable=True, default=list)
    weaknesses = Column(JSON, nullable=True, default=list)
    recent_changes = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)


class ResearchMarketSignalModel(BaseModel):
    """Quantitative or qualitative market demand signal."""
    __tablename__ = "research_market_signals"

    market_segment = Column(String(128), nullable=False)
    signal_type = Column(String(64), nullable=False)  # DEMAND_SURGE, PRICING_PRESSURE, REGULATORY_SHIFT, TECH_DISRUPTION
    description = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False, default=0.85)
    source_reference = Column(String(255), nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)


class ResearchMonitoringRuleModel(BaseModel):
    """Continuous intelligence watch rule."""
    __tablename__ = "research_monitoring_rules"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    target_entity = Column(String(255), nullable=False)
    watch_frequency = Column(String(32), nullable=False, default="DAILY")  # HOURLY, DAILY, WEEKLY, MONTHLY
    topics_monitored = Column(JSON, nullable=True, default=list)
    alert_significance_threshold = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    active = Column(Boolean, nullable=False, default=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="monitoring_rules")


class ResearchIntelligenceEventModel(BaseModel):
    """Emitted intelligence event when meaningful changes occur."""
    __tablename__ = "research_intelligence_events"

    event_type = Column(String(64), nullable=False)  # NEW, CHANGED, REMOVED, EMERGING, RISK, OPPORTUNITY
    target_entity = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    significance = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    confidence = Column(Float, nullable=False, default=0.85)
    evidence_payload = Column(JSON, nullable=True, default=dict)
    meta_info = Column(JSON, nullable=True, default=dict)


class ResearchSynthesisModel(BaseModel):
    """Synthesized intelligence findings and actionable implications."""
    __tablename__ = "research_syntheses"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    executive_summary = Column(Text, nullable=False)
    key_findings = Column(JSON, nullable=True, default=list)
    strategic_implications = Column(JSON, nullable=True, default=list)
    recommended_actions = Column(JSON, nullable=True, default=list)
    uncertainties_and_limitations = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="syntheses")


class ResearchReportModel(BaseModel):
    """Generated research report artifact."""
    __tablename__ = "research_reports"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    report_markdown = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True, default=list)
    confidence_rating = Column(String(32), nullable=False, default="HIGH")
    generated_at = Column(String(32), nullable=False)
    meta_info = Column(JSON, nullable=True, default=dict)

    workspace = relationship("ResearchWorkspaceModel", back_populates="reports")


class ResearchGapModel(BaseModel):
    """Identified research gap or unanswered sub-question."""
    __tablename__ = "research_gaps"

    workspace_id = Column(String(64), ForeignKey("research_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    gap_description = Column(Text, nullable=False)
    importance = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH
    recommended_investigation = Column(Text, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)


class ResearchQualityScoreModel(BaseModel):
    """Automated research quality and grounding scorecard."""
    __tablename__ = "research_quality_scores"

    workspace_id = Column(String(64), nullable=False, index=True)
    source_quality_score = Column(Float, nullable=False, default=0.85)
    evidence_coverage_score = Column(Float, nullable=False, default=0.80)
    citation_accuracy_score = Column(Float, nullable=False, default=0.95)
    conflict_handling_score = Column(Float, nullable=False, default=0.90)
    composite_quality_score = Column(Float, nullable=False, default=0.875)
    meta_info = Column(JSON, nullable=True, default=dict)
