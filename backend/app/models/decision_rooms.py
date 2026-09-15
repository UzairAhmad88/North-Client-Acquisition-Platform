"""
SQLAlchemy ORM models for Phase 53 — Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
"""

import uuid
from datetime import datetime
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
    Index,
)
from sqlalchemy.orm import relationship
try:
    from app.models.base import BaseModel
except ImportError:
    from app.models.base import BaseModel


class DecisionRoomModel(BaseModel):
    """Core collaborative workspace for human-AI decision intelligence."""
    __tablename__ = "decision_rooms"

    title = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    objective = Column(Text, nullable=True)
    decision_type = Column(String(64), nullable=False, default="STRATEGIC")  # STRATEGIC, FINANCIAL, PRODUCT, HIRING, PRICING, etc.
    importance = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(32), nullable=False, default="OPEN")  # DRAFT, OPEN, ANALYSIS, REVIEW, DECISION_REQUIRED, DECIDED, APPROVED, EXECUTING, COMPLETED, ARCHIVED
    owner_id = Column(String(128), nullable=False)
    selected_option_id = Column(String(64), nullable=True)
    decision_summary = Column(Text, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    decided_by = Column(String(128), nullable=True)
    version = Column(Integer, nullable=False, default=1)
    meta_info = Column(JSON, nullable=True, default=dict)

    # Relationships
    context = relationship("DecisionContextModel", back_populates="room", cascade="all, delete-orphan")
    evidence_items = relationship("DecisionEvidenceModel", back_populates="room", cascade="all, delete-orphan")
    assumptions = relationship("DecisionAssumptionModel", back_populates="room", cascade="all, delete-orphan")
    unknowns = relationship("DecisionUnknownModel", back_populates="room", cascade="all, delete-orphan")
    hypotheses = relationship("DecisionHypothesisModel", back_populates="room", cascade="all, delete-orphan")
    options = relationship("DecisionOptionModel", back_populates="room", cascade="all, delete-orphan")
    criteria = relationship("DecisionCriteriaModel", back_populates="room", cascade="all, delete-orphan")
    scores = relationship("DecisionScoreModel", back_populates="room", cascade="all, delete-orphan")
    tradeoffs = relationship("DecisionTradeoffModel", back_populates="room", cascade="all, delete-orphan")
    scenarios = relationship("DecisionScenarioModel", back_populates="room", cascade="all, delete-orphan")
    risks = relationship("DecisionRiskModel", back_populates="room", cascade="all, delete-orphan")
    analyses = relationship("DecisionAnalysisModel", back_populates="room", cascade="all, delete-orphan")
    reviews = relationship("DecisionReviewModel", back_populates="room", cascade="all, delete-orphan")
    disagreements = relationship("DecisionDisagreementModel", back_populates="room", cascade="all, delete-orphan")
    discussions = relationship("DecisionDiscussionModel", back_populates="room", cascade="all, delete-orphan")
    approvals = relationship("DecisionApprovalModel", back_populates="room", cascade="all, delete-orphan")
    actions = relationship("DecisionActionModel", back_populates="room", cascade="all, delete-orphan")
    outcomes = relationship("DecisionOutcomeModel", back_populates="room", cascade="all, delete-orphan")
    post_reviews = relationship("DecisionPostReviewModel", back_populates="room", cascade="all, delete-orphan")


class DecisionContextModel(BaseModel):
    """Background context and organizational memory inputs for a decision room."""
    __tablename__ = "decision_contexts"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    background = Column(Text, nullable=False)
    current_state = Column(Text, nullable=True)
    constraints = Column(JSON, nullable=True, default=list)  # list of constraint strings
    entities_involved = Column(JSON, nullable=True, default=list)  # list of entity ids/names
    policies_applicable = Column(JSON, nullable=True, default=list)
    memory_references = Column(JSON, nullable=True, default=list)  # Phase 48 memory IDs
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="context")


class DecisionEvidenceModel(BaseModel):
    """Structured evidence item supporting or challenging a decision."""
    __tablename__ = "decision_evidence"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type = Column(String(64), nullable=False)  # DATABASE, METRIC, FORECAST, SIMULATION, KNOWLEDGE, POLICY, AUDIT, HUMAN_NOTE
    source = Column(String(255), nullable=False)
    claim = Column(Text, nullable=False)
    provenance = Column(String(255), nullable=True)
    authority = Column(String(64), nullable=False, default="OFFICIAL")  # OFFICIAL, HIGH_TRUST, MEDIUM_TRUST, LOW_TRUST, INFERRED
    statement_category = Column(String(64), nullable=False, default="FACT")  # FACT, INFERENCE, HYPOTHESIS, RECOMMENDATION, UNKNOWN, CONFLICTED
    confidence = Column(Float, nullable=False, default=1.0)
    freshness = Column(String(64), nullable=True, default="CURRENT")
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="evidence_items")


class DecisionAssumptionModel(BaseModel):
    """Explicit assumption made during decision formulation."""
    __tablename__ = "decision_assumptions"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    statement = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False, default=0.7)
    validated = Column(Boolean, nullable=False, default=False)
    validator_role = Column(String(64), nullable=True)
    validation_evidence_id = Column(String(64), nullable=True)
    impact_if_false = Column(String(64), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="assumptions")


class DecisionUnknownModel(BaseModel):
    """Explicit known-unknown identified in a decision room."""
    __tablename__ = "decision_unknowns"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    impact = Column(String(64), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    resolution_path = Column(Text, nullable=True)
    resolved = Column(Boolean, nullable=False, default=False)
    resolved_value = Column(Text, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="unknowns")


class DecisionHypothesisModel(BaseModel):
    """Testable hypothesis proposed in the decision room."""
    __tablename__ = "decision_hypotheses"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    statement = Column(Text, nullable=False)
    test_criteria = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="PROPOSED")  # PROPOSED, TESTING, CONFIRMED, REFUTED
    confidence = Column(Float, nullable=False, default=0.5)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="hypotheses")


class DecisionOptionModel(BaseModel):
    """Candidate decision option / alternative."""
    __tablename__ = "decision_options"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    benefits = Column(JSON, nullable=True, default=list)  # list of string benefits
    costs = Column(Float, nullable=False, default=0.0)
    risks = Column(JSON, nullable=True, default=list)  # list of risk descriptions
    dependencies = Column(JSON, nullable=True, default=list)
    resources_required = Column(JSON, nullable=True, default=list)
    expected_outcome = Column(Text, nullable=True)
    uncertainty_level = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH
    reversibility = Column(String(32), nullable=False, default="REVERSIBLE")  # REVERSIBLE, PARTIALLY_REVERSIBLE, IRREVERSIBLE
    composite_score = Column(Float, nullable=False, default=0.0)
    version = Column(Integer, nullable=False, default=1)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="options")


class DecisionCriteriaModel(BaseModel):
    """Evaluation criterion with explicit weight."""
    __tablename__ = "decision_criteria"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(128), nullable=False)  # e.g., Financial Return, Strategic Alignment, Risk, Speed
    description = Column(Text, nullable=True)
    weight = Column(Float, nullable=False, default=1.0)  # Relative weight > 0
    criterion_type = Column(String(64), nullable=False, default="BENEFIT")  # BENEFIT (higher is better), COST (lower is better)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="criteria")


class DecisionScoreModel(BaseModel):
    """Score for a specific option against a criterion."""
    __tablename__ = "decision_scores"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    option_id = Column(String(64), nullable=False, index=True)
    criterion_id = Column(String(64), nullable=False, index=True)
    raw_score = Column(Float, nullable=False, default=0.0)  # 0.0 to 100.0
    weighted_score = Column(Float, nullable=False, default=0.0)
    justification = Column(Text, nullable=True)
    scored_by = Column(String(128), nullable=False, default="AI_ANALYST")
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="scores")


class DecisionTradeoffModel(BaseModel):
    """Explicit trade-off explanation between options."""
    __tablename__ = "decision_tradeoffs"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    option_a_id = Column(String(64), nullable=False)
    option_b_id = Column(String(64), nullable=False)
    tradeoff_summary = Column(Text, nullable=False)
    gains_in_a = Column(JSON, nullable=True, default=list)
    sacrifices_in_a = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="tradeoffs")


class DecisionScenarioModel(BaseModel):
    """Simulation scenario linked to options."""
    __tablename__ = "decision_scenarios"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    option_id = Column(String(64), nullable=True)
    name = Column(String(128), nullable=False)
    scenario_type = Column(String(64), nullable=False, default="BASELINE")  # BASELINE, OPTIMISTIC, PESSIMISTIC, STRESS_CASE
    assumptions_applied = Column(JSON, nullable=True, default=dict)
    projected_metrics = Column(JSON, nullable=True, default=dict)  # e.g., {"revenue_delta": +15000, "cost": -8000}
    second_order_effects = Column(JSON, nullable=True, default=list)
    confidence_interval = Column(JSON, nullable=True, default=dict)  # {"p10": ..., "p50": ..., "p90": ...}
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="scenarios")


class DecisionRiskModel(BaseModel):
    """Multi-factor risk assessment for the decision."""
    __tablename__ = "decision_risks"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    option_id = Column(String(64), nullable=True)
    risk_category = Column(String(64), nullable=False)  # FINANCIAL, OPERATIONAL, SECURITY, COMPLIANCE, CLIENT, STRATEGIC
    description = Column(Text, nullable=False)
    probability = Column(Float, nullable=False, default=0.3)  # 0.0 to 1.0
    impact = Column(Float, nullable=False, default=0.5)  # 0.0 to 1.0
    risk_score = Column(Float, nullable=False, default=0.15)  # probability * impact
    mitigation = Column(Text, nullable=True)
    blast_radius = Column(String(64), nullable=False, default="TEAM")  # TEAM, DEPARTMENT, COMPANY, CLIENTS
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="risks")


class DecisionAnalysisModel(BaseModel):
    """Specialist domain AI analysis record."""
    __tablename__ = "decision_analyses"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    specialist_role = Column(String(64), nullable=False)  # FINANCE, SECURITY, OPERATIONS, STRATEGY, CUSTOMER_SUCCESS, TECH
    worker_id = Column(String(64), nullable=True)
    summary = Column(Text, nullable=False)
    recommendations = Column(JSON, nullable=True, default=list)
    key_findings = Column(JSON, nullable=True, default=list)
    confidence = Column(Float, nullable=False, default=0.8)
    facts = Column(JSON, nullable=True, default=list)
    inferences = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="analyses")


class DecisionReviewModel(BaseModel):
    """Adversarial critique / challenger review."""
    __tablename__ = "decision_reviews"
    __table_args__ = {"extend_existing": True}

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    reviewer_role = Column(String(64), nullable=False, default="CRITICAL_ANALYST")  # CRITICAL_ANALYST, FACT_CHECKER, RISK_ANALYST
    target_option_id = Column(String(64), nullable=True)
    critique_summary = Column(Text, nullable=False)
    weak_assumptions = Column(JSON, nullable=True, default=list)
    unintended_consequences = Column(JSON, nullable=True, default=list)
    hidden_costs = Column(JSON, nullable=True, default=list)
    data_gaps = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="reviews")


class DecisionDisagreementModel(BaseModel):
    """Detected disagreement between humans, AI workers, or forecasts."""
    __tablename__ = "decision_disagreements"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    disagreement_category = Column(String(64), nullable=False)  # FACTUAL, ASSUMPTION, INTERPRETATION, PREFERENCE, STRATEGIC, RISK
    party_a = Column(String(128), nullable=False)
    view_a = Column(Text, nullable=False)
    party_b = Column(String(128), nullable=False)
    view_b = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, default="SURFACED")  # SURFACED, DISCUSSED, RESOLVED, ACCEPTED_RISK
    resolution_notes = Column(Text, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="disagreements")


class DecisionDiscussionModel(BaseModel):
    """Human discussion comment or annotation in the room."""
    __tablename__ = "decision_discussions"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(String(128), nullable=False)
    author_role = Column(String(64), nullable=False, default="HUMAN_DECISION_MAKER")
    content = Column(Text, nullable=False)
    is_human = Column(Boolean, nullable=False, default=True)
    parent_id = Column(String(64), nullable=True)
    mentions = Column(JSON, nullable=True, default=list)
    annotations = Column(JSON, nullable=True, default=list)  # Feedback tags e.g. ["NEEDS_EVIDENCE", "CORRECT"]
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="discussions")


class DecisionApprovalModel(BaseModel):
    """Multi-step approval record enforcing separation of duties."""
    __tablename__ = "decision_approvals"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    step_name = Column(String(128), nullable=False)  # RISK_REVIEW, SECURITY_REVIEW, GOVERNANCE_REVIEW, EXECUTIVE_APPROVAL
    required_role = Column(String(64), nullable=False)  # e.g., SECURITY_LEAD, CFO, CEO, GRC_OFFICER
    approver_id = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="PENDING")  # PENDING, APPROVED, REJECTED, WAIVED
    decision_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="approvals")


class DecisionActionModel(BaseModel):
    """Controlled actionable outcome derived from the decision."""
    __tablename__ = "decision_actions"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_system = Column(String(64), nullable=False)  # WORKFORCE_TASK, STRATEGY_INITIATIVE, PROJECT, CHANGE_REQUEST
    target_payload = Column(JSON, nullable=True, default=dict)
    assigned_to = Column(String(128), nullable=True)
    execution_status = Column(String(32), nullable=False, default="PENDING_APPROVAL")  # PENDING_APPROVAL, AUTHORIZED, EXECUTING, COMPLETED, FAILED
    dispatched_at = Column(DateTime, nullable=True)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="actions")


class DecisionOutcomeModel(BaseModel):
    """Measured real-world outcome following decision execution."""
    __tablename__ = "decision_outcomes"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name = Column(String(128), nullable=False)
    expected_value = Column(Float, nullable=False)
    actual_value = Column(Float, nullable=False)
    variance_pct = Column(Float, nullable=False, default=0.0)
    measured_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="outcomes")


class DecisionPostReviewModel(BaseModel):
    """Post-decision retrospective analysis and organizational learning."""
    __tablename__ = "decision_post_reviews"

    room_id = Column(String(64), ForeignKey("decision_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    decision_quality_score = Column(Float, nullable=False, default=80.0)  # 0 to 100 process quality
    outcome_rating = Column(String(32), nullable=False, default="NEUTRAL")  # SUCCESSFUL, NEUTRAL, UNFAVORABLE
    prediction_error = Column(Text, nullable=True)
    assumption_error = Column(Text, nullable=True)
    execution_error = Column(Text, nullable=True)
    model_error = Column(Text, nullable=True)
    lessons_learned = Column(JSON, nullable=True, default=list)
    feed_to_organizational_memory = Column(Boolean, nullable=False, default=True)
    reviewed_by = Column(String(128), nullable=False)
    reviewed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    meta_info = Column(JSON, nullable=True, default=dict)

    room = relationship("DecisionRoomModel", back_populates="post_reviews")


class DecisionTemplateModel(BaseModel):
    """Reusable template for structured decision workflows."""
    __tablename__ = "decision_templates"

    name = Column(String(128), nullable=False, unique=True)
    decision_type = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)
    default_criteria = Column(JSON, nullable=True, default=list)
    default_specialists = Column(JSON, nullable=True, default=list)
    default_approval_steps = Column(JSON, nullable=True, default=list)
    meta_info = Column(JSON, nullable=True, default=dict)
