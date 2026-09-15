"""
SQLAlchemy ORM models for Phase 55 — Unified Product & Innovation Intelligence, Idea Discovery, Validation & R&D Platform.
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


class InnovationWorkspaceModel(BaseModel):
    """Core innovation workspace container for discovering, validating, and developing new products/services."""
    __tablename__ = "innovation_workspaces"

    title = Column(String(255), nullable=False)
    theme = Column(String(128), nullable=False, default="PRODUCT_INNOVATION")  # PRODUCT, SERVICE, SOFTWARE, AI, AUTOMATION, BUSINESS_MODEL, PROCESS
    objective = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="DISCOVERY")  # DRAFT, DISCOVERY, RESEARCH, VALIDATION, EXPERIMENTATION, EVALUATION, APPROVED, DEVELOPMENT, LAUNCH, MONITORING, COMPLETED, ARCHIVED
    owner_id = Column(String(128), nullable=False)
    target_market = Column(String(128), nullable=True)
    horizon = Column(String(16), nullable=False, default="H1")  # H1 (Core), H2 (Adjacent), H3 (Transformational)
    stage_gate = Column(String(32), nullable=False, default="GATE_0_IDEA")
    confidence_score = Column(Float, nullable=False, default=0.75)
    version = Column(Integer, nullable=False, default=1)
    meta_info = Column(JSON, nullable=True, default=dict)

    # Relationships
    problems = relationship("InnovationProblemModel", back_populates="workspace", cascade="all, delete-orphan")
    opportunities = relationship("InnovationOpportunityModel", back_populates="workspace", cascade="all, delete-orphan")
    ideas = relationship("InnovationIdeaModel", back_populates="workspace", cascade="all, delete-orphan")
    hypotheses = relationship("InnovationHypothesisModel", back_populates="workspace", cascade="all, delete-orphan")
    experiments = relationship("InnovationExperimentModel", back_populates="workspace", cascade="all, delete-orphan")
    product_concepts = relationship("InnovationProductConceptModel", back_populates="workspace", cascade="all, delete-orphan")
    service_concepts = relationship("InnovationServiceConceptModel", back_populates="workspace", cascade="all, delete-orphan")
    business_cases = relationship("InnovationBusinessCaseModel", back_populates="workspace", cascade="all, delete-orphan")
    gate_reviews = relationship("InnovationGateReviewModel", back_populates="workspace", cascade="all, delete-orphan")


class InnovationProblemModel(BaseModel):
    """Real-world user or market problem with frequency, severity, and willingness-to-pay evidence."""
    __tablename__ = "innovation_problems"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    statement = Column(Text, nullable=False)
    affected_users = Column(String(255), nullable=True)
    frequency = Column(String(64), nullable=False, default="DAILY")  # HOURLY, DAILY, WEEKLY, MONTHLY, OCCASIONAL
    severity = Column(String(32), nullable=False, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    existing_solutions = Column(JSON, nullable=True, default=list)  # ["Manual spreadsheets", "Legacy ERP"]
    willingness_to_pay_signal = Column(Float, nullable=True)  # Estimated budget / willingness in USD
    urgency_score = Column(Float, nullable=False, default=0.8)
    confidence_score = Column(Float, nullable=False, default=0.7)
    status = Column(String(32), nullable=False, default="OBSERVED")  # OBSERVED, RESEARCHING, VALIDATED, UNVALIDATED, REJECTED, SUPERSEDED
    evidence_sources = Column(JSON, nullable=True, default=list)

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="problems")


class InnovationOpportunityModel(BaseModel):
    """Evaluated business opportunity converted from validated customer problems."""
    __tablename__ = "innovation_opportunities"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    market_potential = Column(String(32), nullable=False, default="HIGH")  # HIGH, MEDIUM, LOW, UNKNOWN
    revenue_potential_usd = Column(Float, nullable=True)
    competitive_intensity = Column(String(32), nullable=False, default="MEDIUM")  # HIGH, MEDIUM, LOW
    technical_feasibility = Column(String(32), nullable=False, default="FEASIBLE")  # FEASIBLE, FEASIBLE_WITH_RISK, EXPERIMENT_REQUIRED, NOT_FEASIBLE
    strategic_alignment_score = Column(Float, nullable=False, default=0.85)
    time_to_market_months = Column(Float, nullable=False, default=3.0)
    risk_level = Column(String(32), nullable=False, default="MEDIUM")
    status = Column(String(32), nullable=False, default="OPEN")

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="opportunities")


class InnovationIdeaModel(BaseModel):
    """Innovation idea with origin tracking and transparent 11-factor weighted score."""
    __tablename__ = "innovation_ideas"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(String(64), nullable=True)
    opportunity_id = Column(String(64), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    origin_source = Column(String(128), nullable=False, default="HUMAN")  # HUMAN, AI_WORKER, CLIENT, SUPPORT_TICKET, RESEARCH, COMPETITOR_ANALYSIS, PROCESS_INTELLIGENCE, STRATEGY
    target_users = Column(String(255), nullable=True)
    proposed_value = Column(Text, nullable=True)
    assumptions_summary = Column(JSON, nullable=True, default=list)
    
    # 11-factor Transparent Scoring Formula
    customer_value_score = Column(Float, nullable=False, default=0.8)
    market_potential_score = Column(Float, nullable=False, default=0.8)
    strategic_fit_score = Column(Float, nullable=False, default=0.85)
    revenue_potential_score = Column(Float, nullable=False, default=0.75)
    profitability_score = Column(Float, nullable=False, default=0.8)
    differentiation_score = Column(Float, nullable=False, default=0.7)
    technical_feasibility_score = Column(Float, nullable=False, default=0.85)
    execution_complexity_score = Column(Float, nullable=False, default=0.5)  # lower is simpler
    risk_score = Column(Float, nullable=False, default=0.4)  # lower is safer
    time_to_value_score = Column(Float, nullable=False, default=0.7)
    evidence_strength_score = Column(Float, nullable=False, default=0.6)
    composite_score = Column(Float, nullable=False, default=0.76)

    status = Column(String(32), nullable=False, default="IDEA")  # IDEA, SHORTLISTED, RESEARCHING, VALIDATING, EXPERIMENTING, PROMISING, REJECTED, DEFERRED, APPROVED
    version = Column(Integer, nullable=False, default=1)

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="ideas")
    hypotheses = relationship("InnovationHypothesisModel", back_populates="idea", cascade="all, delete-orphan")


class InnovationHypothesisModel(BaseModel):
    """Testable prediction tied to an innovation idea with defined success metric."""
    __tablename__ = "innovation_hypotheses"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    idea_id = Column(String(64), ForeignKey("innovation_ideas.id", ondelete="CASCADE"), nullable=False, index=True)
    statement = Column(Text, nullable=False)  # "We believe that X..."
    prediction = Column(Text, nullable=False)  # "We expect Y to happen..."
    metric_name = Column(String(128), nullable=False)  # e.g. "Conversion Rate", "Click-through rate"
    baseline_value = Column(Float, nullable=False, default=0.0)
    target_value = Column(Float, nullable=False, default=0.2)
    confidence = Column(Float, nullable=False, default=0.7)
    status = Column(String(32), nullable=False, default="DRAFTED")  # DRAFTED, TESTING, VALIDATED, REFUTED, INCONCLUSIVE

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="hypotheses")
    idea = relationship("InnovationIdeaModel", back_populates="hypotheses")
    assumptions = relationship("InnovationAssumptionModel", back_populates="hypothesis", cascade="all, delete-orphan")
    experiments = relationship("InnovationExperimentModel", back_populates="hypothesis", cascade="all, delete-orphan")


class InnovationAssumptionModel(BaseModel):
    """Mapped assumption categorized by impact vs uncertainty 2x2 grid."""
    __tablename__ = "innovation_assumptions"

    hypothesis_id = Column(String(64), ForeignKey("innovation_hypotheses.id", ondelete="CASCADE"), nullable=False, index=True)
    assumption_text = Column(Text, nullable=False)
    category = Column(String(64), nullable=False, default="CUSTOMER")  # CUSTOMER, MARKET, PRICING, TECHNOLOGY, BEHAVIOR, OPERATIONAL, FINANCIAL, REGULATORY
    impact_level = Column(String(16), nullable=False, default="HIGH")  # HIGH, LOW
    uncertainty_level = Column(String(16), nullable=False, default="HIGH")  # HIGH, LOW
    validation_priority = Column(String(32), nullable=False, default="CRITICAL")  # CRITICAL, HIGH, MEDIUM, LOW
    is_validated = Column(Boolean, nullable=False, default=False)

    # Relationships
    hypothesis = relationship("InnovationHypothesisModel", back_populates="assumptions")


class InnovationExperimentModel(BaseModel):
    """Rigorous experiment (A/B test, landing page, pricing test, prototype) with governance approval."""
    __tablename__ = "innovation_experiments"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    hypothesis_id = Column(String(64), ForeignKey("innovation_hypotheses.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    experiment_type = Column(String(64), nullable=False, default="PROTOTYPE")  # EXPLORATORY, DESCRIPTIVE, COMPARATIVE, AB_TEST, PILOT, PROTOTYPE, PRICING, SURVEY
    objective = Column(Text, nullable=True)
    target_population = Column(String(255), nullable=True)
    sample_size = Column(Integer, nullable=False, default=100)
    duration_days = Column(Integer, nullable=False, default=14)
    status = Column(String(32), nullable=False, default="DESIGNED")  # DESIGNED, APPROVED, RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED
    risk_review_passed = Column(Boolean, nullable=False, default=True)
    governance_approved = Column(Boolean, nullable=False, default=False)
    statistical_method = Column(String(64), nullable=False, default="TWO_SAMPLE_T_TEST")

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="experiments")
    hypothesis = relationship("InnovationHypothesisModel", back_populates="experiments")
    results = relationship("InnovationExperimentResultModel", back_populates="experiment", cascade="all, delete-orphan")


class InnovationExperimentResultModel(BaseModel):
    """Empirical observed experiment results with statistical effect size and significance."""
    __tablename__ = "innovation_experiment_results"

    experiment_id = Column(String(64), ForeignKey("innovation_experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    observed_sample_size = Column(Integer, nullable=False, default=0)
    control_mean = Column(Float, nullable=False, default=0.0)
    treatment_mean = Column(Float, nullable=False, default=0.0)
    delta_percentage = Column(Float, nullable=False, default=0.0)
    p_value = Column(Float, nullable=True)
    is_statistically_significant = Column(Boolean, nullable=False, default=False)
    conclusion = Column(String(32), nullable=False, default="SUPPORTED")  # SUPPORTED, PARTIALLY_SUPPORTED, NOT_SUPPORTED, INCONCLUSIVE, INSUFFICIENT_DATA
    limitations = Column(Text, nullable=True)
    raw_data_summary = Column(JSON, nullable=True, default=dict)

    # Relationships
    experiment = relationship("InnovationExperimentModel", back_populates="results")


class InnovationLearningModel(BaseModel):
    """Structured organizational learning derived from completed experiments."""
    __tablename__ = "innovation_learnings"

    workspace_id = Column(String(64), nullable=False, index=True)
    hypothesis_id = Column(String(64), nullable=True)
    experiment_id = Column(String(64), nullable=True)
    insight_statement = Column(Text, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    strategic_implication = Column(Text, nullable=True)
    recorded_at_date = Column(DateTime, nullable=True)


class InnovationProductConceptModel(BaseModel):
    """Synthesized product concept with value proposition, features, and architecture."""
    __tablename__ = "innovation_product_concepts"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    idea_id = Column(String(64), nullable=True)
    name = Column(String(255), nullable=False)
    target_customer_persona = Column(String(255), nullable=False)
    value_proposition = Column(Text, nullable=False)
    core_features = Column(JSON, nullable=True, default=list)
    differentiators = Column(JSON, nullable=True, default=list)
    business_model_type = Column(String(64), nullable=False, default="SUBSCRIPTION")  # SUBSCRIPTION, USAGE_BASED, TIERED, PER_PROJECT, FREEMIUM
    technical_architecture_notes = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="DRAFT")

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="product_concepts")


class InnovationServiceConceptModel(BaseModel):
    """Synthesized service concept with delivery model, SLA, and pricing structure."""
    __tablename__ = "innovation_service_concepts"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    idea_id = Column(String(64), nullable=True)
    service_name = Column(String(255), nullable=False)
    target_client_profile = Column(String(255), nullable=False)
    service_deliverables = Column(JSON, nullable=True, default=list)
    delivery_model = Column(String(64), nullable=False, default="HYBRID_AI_HUMAN")  # FULLY_AUTOMATED, HYBRID_AI_HUMAN, MANAGED_SERVICE
    pricing_model = Column(String(64), nullable=False, default="MONTHLY_RETAINER")
    status = Column(String(32), nullable=False, default="DRAFT")

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="service_concepts")


class InnovationBusinessCaseModel(BaseModel):
    """Financial and strategic business case evaluating TAM, payback, and break-even."""
    __tablename__ = "innovation_business_cases"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    concept_id = Column(String(64), nullable=False)
    target_tam_usd = Column(Float, nullable=False, default=1000000.0)
    projected_year1_revenue_usd = Column(Float, nullable=False, default=250000.0)
    estimated_development_cost_usd = Column(Float, nullable=False, default=50000.0)
    estimated_cac_usd = Column(Float, nullable=False, default=1200.0)
    estimated_ltv_usd = Column(Float, nullable=False, default=7200.0)
    payback_months = Column(Float, nullable=False, default=4.5)
    break_even_customers_count = Column(Integer, nullable=False, default=25)
    gross_margin_percentage = Column(Float, nullable=False, default=82.0)
    recommendation = Column(String(32), nullable=False, default="PROCEED_TO_MVP")

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="business_cases")


class InnovationEconomicsModel(BaseModel):
    """Unit economics model capturing COGS, AI model tokens, compute, and margin."""
    __tablename__ = "innovation_economics"

    concept_id = Column(String(64), nullable=False, index=True)
    price_per_unit_usd = Column(Float, nullable=False, default=199.0)
    direct_labor_cost_usd = Column(Float, nullable=False, default=20.0)
    ai_compute_cost_usd = Column(Float, nullable=False, default=12.5)
    infrastructure_cost_usd = Column(Float, nullable=False, default=8.0)
    gross_profit_per_unit_usd = Column(Float, nullable=False, default=158.5)
    gross_margin_percentage = Column(Float, nullable=False, default=79.6)


class InnovationPrototypeModel(BaseModel):
    """Prototype lifecycle record tracking feedback and iterations."""
    __tablename__ = "innovation_prototypes"

    concept_id = Column(String(64), nullable=False, index=True)
    prototype_name = Column(String(255), nullable=False)
    version = Column(String(32), nullable=False, default="v0.1")
    prototype_url_or_repo = Column(String(255), nullable=True)
    user_feedback_summary = Column(Text, nullable=True)
    usability_score = Column(Float, nullable=False, default=8.5)  # 1 to 10
    iteration_notes = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, TESTED, PROMOTED_TO_MVP, ARCHIVED


class InnovationPRDModel(BaseModel):
    """Product Requirements Document draft generated from validated concept."""
    __tablename__ = "innovation_prds"

    concept_id = Column(String(64), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    problem_summary = Column(Text, nullable=False)
    target_personas = Column(JSON, nullable=True, default=list)
    user_stories = Column(JSON, nullable=True, default=list)
    functional_requirements = Column(JSON, nullable=True, default=list)
    non_functional_requirements = Column(JSON, nullable=True, default=list)
    security_privacy_requirements = Column(JSON, nullable=True, default=list)
    success_metrics = Column(JSON, nullable=True, default=list)
    human_approved = Column(Boolean, nullable=False, default=False)


class InnovationGateReviewModel(BaseModel):
    """Stage-Gate review record enforcing evidence requirements before capital or dev allocation."""
    __tablename__ = "innovation_gate_reviews"

    workspace_id = Column(String(64), ForeignKey("innovation_workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    gate_stage = Column(String(32), nullable=False)  # GATE_0_IDEA, GATE_1_PROBLEM, GATE_2_OPPORTUNITY, GATE_3_SOLUTION, GATE_4_BUSINESS, GATE_5_MVP, GATE_6_LAUNCH, GATE_7_SCALE_PIVOT
    reviewer_id = Column(String(128), nullable=False)
    evidence_completeness_score = Column(Float, nullable=False, default=0.85)
    decision = Column(String(32), nullable=False, default="PENDING")  # PROCEED, PIVOT, PAUSE, STOP, REVISE_EVIDENCE, PENDING
    review_notes = Column(Text, nullable=True)
    decision_timestamp = Column(DateTime, nullable=True)

    # Relationships
    workspace = relationship("InnovationWorkspaceModel", back_populates="gate_reviews")


class InnovationPortfolioModel(BaseModel):
    """Innovation portfolio allocating budget and resources across Horizons 1, 2, and 3."""
    __tablename__ = "innovation_portfolios"

    portfolio_name = Column(String(255), nullable=False)
    horizon_1_budget_percentage = Column(Float, nullable=False, default=70.0)  # Core
    horizon_2_budget_percentage = Column(Float, nullable=False, default=20.0)  # Adjacent
    horizon_3_budget_percentage = Column(Float, nullable=False, default=10.0)  # Transformational
    total_active_initiatives = Column(Integer, nullable=False, default=0)
    portfolio_expected_roi = Column(Float, nullable=False, default=3.4)
    meta_info = Column(JSON, nullable=True, default=dict)
