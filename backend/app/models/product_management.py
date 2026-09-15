"""
SQLAlchemy ORM models for Phase 56 — Unified Product Lifecycle, Product Management & Continuous Delivery Intelligence Platform.
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
from sqlalchemy.orm import relationship, foreign, remote
from app.models.base import BaseModel


class ProductModel(BaseModel):
    """Core product portfolio entity representing a software system, AI agent, service, or platform."""
    __tablename__ = "products"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    product_type = Column(String(64), nullable=False, default="SOFTWARE_PRODUCT")  # PRODUCT, SERVICE, PLATFORM, INTERNAL, AI_PRODUCT, AUTOMATION
    lifecycle_stage = Column(String(64), nullable=False, default="DISCOVERY")  # DISCOVERY, CONCEPT, STRATEGY, PLANNING, VALIDATION, DEVELOPMENT, TESTING, RELEASE, LAUNCH, ADOPTION, OPTIMIZATION, MATURITY, SUNSET
    owner_id = Column(String(128), nullable=False)
    team_name = Column(String(128), nullable=True)
    vision_statement = Column(Text, nullable=True)
    target_market = Column(String(255), nullable=True)
    customer_segments = Column(JSON, nullable=True, default=list)
    north_star_metric = Column(String(255), nullable=True)
    health_status = Column(String(32), nullable=False, default="HEALTHY")  # HEALTHY, STABLE, WATCH, AT_RISK, CRITICAL
    health_score = Column(Float, nullable=False, default=0.88)
    status = Column(String(32), nullable=False, default="ACTIVE")  # ACTIVE, PAUSED, ON_HOLD, CANCELLED, DEPRECATED, ARCHIVED
    version = Column(Integer, nullable=False, default=1)
    meta_info = Column(JSON, nullable=True, default=dict)

    # Relationships
    # objectives = relationship("app.models.product_management.ProductObjectiveModel", primaryjoin=lambda: ProductModel.id == ProductObjectiveModel.__table__.c.product_id, foreign_keys=lambda: [ProductObjectiveModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # metrics = relationship("ProductMetricModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os
    # feedback = relationship("app.models.product_management.ProductFeedbackModel", primaryjoin=lambda: ProductModel.id == ProductFeedbackModel.__table__.c.product_id, foreign_keys=lambda: [ProductFeedbackModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # requirements = relationship("ProductRequirementModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os
    # epics = relationship("ProductEpicModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os
    # features = relationship("app.models.product_management.ProductFeatureModel", primaryjoin=lambda: ProductModel.id == ProductFeatureModel.__table__.c.product_id, foreign_keys=lambda: [ProductFeatureModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # backlog_items = relationship("ProductBacklogItemModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os
    # roadmaps = relationship("app.models.product_management.ProductRoadmapModel", primaryjoin=lambda: ProductModel.id == ProductRoadmapModel.__table__.c.product_id, foreign_keys=lambda: [ProductRoadmapModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # sprints = relationship("app.models.product_management.ProductSprintModel", primaryjoin=lambda: ProductModel.id == ProductSprintModel.__table__.c.product_id, foreign_keys=lambda: [ProductSprintModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # releases = relationship("app.models.product_management.ProductReleaseModel", primaryjoin=lambda: ProductModel.id == ProductReleaseModel.__table__.c.product_id, foreign_keys=lambda: [ProductReleaseModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # feature_flags = relationship("app.models.product_management.ProductFeatureFlagModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os
    # launches = relationship("app.models.product_management.ProductLaunchModel", primaryjoin=lambda: ProductModel.id == ProductLaunchModel.__table__.c.product_id, foreign_keys=lambda: [ProductLaunchModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # experiments = relationship("app.models.product_management.ProductExperimentModel", primaryjoin=lambda: ProductModel.id == ProductExperimentModel.__table__.c.product_id, foreign_keys=lambda: [ProductExperimentModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # health_records = relationship("ProductHealthModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os
    # sunset_plans = relationship("ProductSunsetModel", back_populates="product", cascade="all, delete-orphan")  # disabled to prevent collision with product_os


class ProductObjectiveModel(BaseModel):
    """Measurable product objective or key result tied to business goals."""
    __tablename__ = "product_objectives"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    metric_name = Column(String(128), nullable=False)
    baseline_value = Column(Float, nullable=False, default=0.0)
    target_value = Column(Float, nullable=False, default=1.0)
    current_value = Column(Float, nullable=False, default=0.0)
    unit = Column(String(32), nullable=True, default="%")
    time_window = Column(String(64), nullable=True, default="Q3 2026")
    owner_id = Column(String(128), nullable=False)
    confidence = Column(Float, nullable=False, default=0.85)
    status = Column(String(32), nullable=False, default="ON_TRACK")  # ON_TRACK, AT_RISK, BEHIND, ACHIEVED

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductObjectiveModel.__table__.c.product_id, foreign_keys=lambda: [ProductObjectiveModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductMetricModel(BaseModel):
    """Registry item for business, customer, or operational product metrics."""
    __tablename__ = "product_metrics"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False, default="ENGAGEMENT")  # ACQUISITION, ACTIVATION, ENGAGEMENT, RETENTION, REVENUE, RELIABILITY
    definition = Column(Text, nullable=True)
    formula = Column(String(255), nullable=True)
    source = Column(String(128), nullable=True)
    current_value = Column(Float, nullable=False, default=0.0)
    target_value = Column(Float, nullable=True)
    unit = Column(String(32), nullable=True, default="count")
    time_window = Column(String(64), nullable=True, default="30d")
    version = Column(Integer, nullable=False, default=1)

    # product = relationship("ProductModel", back_populates="metrics")  # disabled to prevent collision with product_os


class ProductFeedbackModel(BaseModel):
    """Customer, sales, support, and survey feedback items with classification and clustering."""
    __tablename__ = "product_feedback"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    source = Column(String(64), nullable=False, default="CLIENT")  # CLIENT, SUPPORT, SALES, SURVEY, ANALYTICS, USER_INTERVIEW, AI_AGENT
    feedback_type = Column(String(64), nullable=False, default="FEATURE_REQUEST")  # BUG, FEATURE_REQUEST, USABILITY, PERFORMANCE, PRICING, PRAISE, COMPLAINT
    raw_text = Column(Text, nullable=False)
    customer_segment = Column(String(128), nullable=True)
    revenue_impact_usd = Column(Float, nullable=True, default=0.0)
    sentiment_score = Column(Float, nullable=False, default=0.0)  # -1.0 to 1.0
    theme_cluster = Column(String(128), nullable=True)
    severity = Column(String(32), nullable=False, default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    status = Column(String(32), nullable=False, default="NEW")  # NEW, TRIAGED, LINKED_TO_BACKLOG, RESOLVED, DISMISSED

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductFeedbackModel.__table__.c.product_id, foreign_keys=lambda: [ProductFeedbackModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductRequirementModel(BaseModel):
    """PRD requirement specification with functional, non-functional, security, and traceability links."""
    __tablename__ = "product_requirements"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    requirement_code = Column(String(64), nullable=False)  # e.g., REQ-001
    title = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, default="FUNCTIONAL")  # FUNCTIONAL, NON_FUNCTIONAL, SECURITY, PERFORMANCE, COMPLIANCE, AI, INTEGRATION
    description = Column(Text, nullable=False)
    priority = Column(String(32), nullable=False, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    acceptance_criteria = Column(JSON, nullable=True, default=list)
    source_evidence = Column(JSON, nullable=True, default=list)
    dependencies = Column(JSON, nullable=True, default=list)
    linked_problem_id = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="DRAFT")  # DRAFT, APPROVED, IN_DEVELOPMENT, VERIFIED, DEPRECATED
    version = Column(Integer, nullable=False, default=1)

    # product = relationship("ProductModel", back_populates="requirements")  # disabled to prevent collision with product_os


class ProductEpicModel(BaseModel):
    """High-level architectural initiative and epic grouping."""
    __tablename__ = "product_epics"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    objective = Column(Text, nullable=True)
    target_release_id = Column(String(36), nullable=True)
    business_value_score = Column(Float, nullable=False, default=8.0)
    status = Column(String(32), nullable=False, default="PLANNED")  # PLANNED, IN_PROGRESS, COMPLETED, BLOCKED

    # product = relationship("ProductModel", back_populates="epics")  # disabled to prevent collision with product_os
    # features = relationship("app.models.product_management.ProductFeatureModel", primaryjoin=lambda: ProductModel.id == ProductFeatureModel.__table__.c.product_id, foreign_keys=lambda: [ProductFeatureModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductFeatureModel(BaseModel):
    """Product feature specification linked to requirements and user stories."""
    __tablename__ = "product_features"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    epic_id = Column(String(36), ForeignKey("product_epics.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_story = Column(Text, nullable=True)  # As a [user], I want [capability] so that [outcome]
    acceptance_criteria = Column(JSON, nullable=True, default=list)
    effort_points = Column(Integer, nullable=False, default=5)
    priority = Column(String(32), nullable=False, default="MEDIUM")
    status = Column(String(32), nullable=False, default="READY")  # BACKLOG, READY, IN_DEV, QA, RELEASED

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductFeatureModel.__table__.c.product_id, foreign_keys=lambda: [ProductFeatureModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # epic = relationship("ProductEpicModel", back_populates="features")  # disabled to prevent collision with product_os


class ProductBacklogItemModel(BaseModel):
    """Unified backlog work item (Story, Task, Bug, Spike, Tech Debt)."""
    __tablename__ = "product_backlog_items"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    item_type = Column(String(32), nullable=False, default="STORY")  # STORY, TASK, BUG, TECH_DEBT, SPIKE, RESEARCH
    description = Column(Text, nullable=True)
    priority = Column(String(32), nullable=False, default="MEDIUM")
    business_value = Column(Float, nullable=False, default=7.0)
    customer_value = Column(Float, nullable=False, default=7.0)
    effort_estimate = Column(Float, nullable=False, default=3.0)
    risk_score = Column(Float, nullable=False, default=2.0)
    assigned_sprint_id = Column(String(36), nullable=True)
    status = Column(String(32), nullable=False, default="BACKLOG")  # BACKLOG, SPRINT_READY, IN_PROGRESS, CODE_REVIEW, QA_TESTING, DONE
    assignee_id = Column(String(128), nullable=True)

    # product = relationship("ProductModel", back_populates="backlog_items")  # disabled to prevent collision with product_os


class ProductPrioritizationScoreModel(BaseModel):
    """Prioritization calculation record (RICE, WSJF, MoSCoW, Value vs Effort)."""
    __tablename__ = "product_prioritization_scores"

    item_id = Column(String(36), nullable=False, index=True)
    framework = Column(String(32), nullable=False, default="RICE")  # RICE, WSJF, MOSCOW, VALUE_VS_EFFORT, CUSTOM_WEIGHTED
    score = Column(Float, nullable=False, default=0.0)
    formula_breakdown = Column(JSON, nullable=False, default=dict)
    calculated_at = Column(DateTime, nullable=True)


class ProductRoadmapModel(BaseModel):
    """Product roadmap plan supporting Now/Next/Later, Quarterly, and Scenario views."""
    __tablename__ = "product_roadmaps"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    scenario_type = Column(String(64), nullable=False, default="BASE_PLAN")  # BASE_PLAN, ACCELERATED, CONSTRAINED, GROWTH, RISK_REDUCED
    confidence_level = Column(Float, nullable=False, default=0.85)
    version = Column(Integer, nullable=False, default=1)

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductRoadmapModel.__table__.c.product_id, foreign_keys=lambda: [ProductRoadmapModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os
    # items = relationship("app.models.product_management.ProductRoadmapItemModel", back_populates="roadmap", cascade="all, delete-orphan")  # disabled to prevent collision with product_os


class ProductRoadmapItemModel(BaseModel):
    """Individual item on the product roadmap timeline or horizon column."""
    __tablename__ = "product_roadmap_items"

    roadmap_id = Column(String(36), ForeignKey("product_roadmaps.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    horizon = Column(String(32), nullable=False, default="NOW")  # NOW, NEXT, LATER, Q3_2026, Q4_2026
    theme = Column(String(128), nullable=True)
    expected_outcome = Column(Text, nullable=True)
    confidence = Column(Float, nullable=False, default=0.80)
    dependencies = Column(JSON, nullable=True, default=list)
    estimated_weeks = Column(Integer, nullable=False, default=4)

    # roadmap = relationship("app.models.product_management.ProductRoadmapModel", back_populates="items")  # disabled to prevent collision with product_os


class ProductCapacityPlanModel(BaseModel):
    """Team role capacity and engineering allocation model."""
    __tablename__ = "product_capacity_plans"

    product_id = Column(String(36), nullable=False, index=True)
    engineering_fte = Column(Float, nullable=False, default=4.0)
    design_fte = Column(Float, nullable=False, default=1.0)
    qa_fte = Column(Float, nullable=False, default=1.0)
    ai_ml_fte = Column(Float, nullable=False, default=1.0)
    devops_fte = Column(Float, nullable=False, default=0.5)
    bottleneck_role = Column(String(64), nullable=True)
    utilization_rate = Column(Float, nullable=False, default=0.82)


class ProductSprintModel(BaseModel):
    """Sprint / Iteration execution cycle."""
    __tablename__ = "product_sprints"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)  # Sprint 14
    sprint_goal = Column(Text, nullable=True)
    capacity_points = Column(Integer, nullable=False, default=40)
    committed_points = Column(Integer, nullable=False, default=36)
    completed_points = Column(Integer, nullable=False, default=0)
    status = Column(String(32), nullable=False, default="PLANNING")  # PLANNING, READY, ACTIVE, REVIEW, RETROSPECTIVE, COMPLETED

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductSprintModel.__table__.c.product_id, foreign_keys=lambda: [ProductSprintModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductReleaseModel(BaseModel):
    """Release container with scope, readiness gates, and rollback plans."""
    __tablename__ = "product_releases"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    version_tag = Column(String(64), nullable=False)  # v1.2.0
    release_name = Column(String(255), nullable=False)
    scope_summary = Column(Text, nullable=True)
    readiness_status = Column(String(32), nullable=False, default="IN_PROGRESS")  # IN_PROGRESS, READY_FOR_SIGN_OFF, APPROVED, REJECTED, RELEASED
    readiness_score = Column(Float, nullable=False, default=0.70)
    critical_defects_count = Column(Integer, nullable=False, default=0)
    qa_sign_off = Column(Boolean, nullable=False, default=False)
    security_sign_off = Column(Boolean, nullable=False, default=False)
    rollback_plan = Column(Text, nullable=True)
    released_at = Column(DateTime, nullable=True)

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductReleaseModel.__table__.c.product_id, foreign_keys=lambda: [ProductReleaseModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductFeatureFlagModel(BaseModel):
    """Controlled rollout feature flag state."""
    __tablename__ = "product_feature_flags"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    flag_key = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String(32), nullable=False, default="OFF")  # OFF, SHADOW, INTERNAL, CANARY, PERCENTAGE, SEGMENT, FULL
    rollout_percentage = Column(Integer, nullable=False, default=0)
    target_segments = Column(JSON, nullable=True, default=list)

    # product = relationship("ProductModel", back_populates="feature_flags")  # disabled to prevent collision with product_os


class ProductLaunchModel(BaseModel):
    """Product launch workspace, positioning, and checklist."""
    __tablename__ = "product_launches"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    launch_name = Column(String(255), nullable=False)
    target_audience = Column(String(255), nullable=True)
    value_messaging = Column(Text, nullable=True)
    checklist_status = Column(JSON, nullable=False, default=dict)
    is_launch_approved = Column(Boolean, nullable=False, default=False)
    approved_by = Column(String(128), nullable=True)
    status = Column(String(32), nullable=False, default="PREPARING")  # PREPARING, READY, LAUNCHED, POST_LAUNCH

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductLaunchModel.__table__.c.product_id, foreign_keys=lambda: [ProductLaunchModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductExperimentModel(BaseModel):
    """Product A/B test and UX experiment with guardrail metrics."""
    __tablename__ = "product_experiments"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    hypothesis = Column(Text, nullable=False)
    primary_metric = Column(String(128), nullable=False)
    guardrail_metrics = Column(JSON, nullable=True, default=list)
    control_variant = Column(String(128), nullable=False, default="Control")
    treatment_variants = Column(JSON, nullable=False, default=list)
    p_value = Column(Float, nullable=True)
    is_statistically_significant = Column(Boolean, nullable=False, default=False)
    status = Column(String(32), nullable=False, default="RUNNING")  # DRAFT, RUNNING, COMPLETED, CANCELLED

    # product = relationship("ProductModel", primaryjoin=lambda: ProductModel.id == ProductExperimentModel.__table__.c.product_id, foreign_keys=lambda: [ProductExperimentModel.__table__.c.product_id], viewonly=True)  # disabled to prevent collision with product_os


class ProductHealthModel(BaseModel):
    """Multi-dimensional health snapshot for product reliability and adoption."""
    __tablename__ = "product_health_records"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    health_score = Column(Float, nullable=False, default=0.85)  # 0.0 to 1.0
    adoption_score = Column(Float, nullable=False, default=0.85)
    satisfaction_score = Column(Float, nullable=False, default=0.90)
    reliability_score = Column(Float, nullable=False, default=0.99)
    security_score = Column(Float, nullable=False, default=0.95)
    delivery_score = Column(Float, nullable=False, default=0.80)
    health_state = Column(String(32), nullable=False, default="HEALTHY")  # HEALTHY, STABLE, WATCH, AT_RISK, CRITICAL
    findings = Column(JSON, nullable=True, default=list)

    # product = relationship("ProductModel", back_populates="health_records")  # disabled to prevent collision with product_os


class ProductSunsetModel(BaseModel):
    """Product sunset, deprecation, and customer migration plan."""
    __tablename__ = "product_sunset_plans"

    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    sunset_reason = Column(Text, nullable=False)
    migration_target_product_id = Column(String(36), nullable=True)
    affected_customers_count = Column(Integer, nullable=False, default=0)
    financial_impact_usd = Column(Float, nullable=False, default=0.0)
    deprecation_date = Column(DateTime, nullable=True)
    sunset_date = Column(DateTime, nullable=True)
    governance_approved = Column(Boolean, nullable=False, default=False)
    status = Column(String(32), nullable=False, default="ANALYSIS")  # ANALYSIS, APPROVED, DEPRECATED, MIGRATING, SUNSET_COMPLETED

    # product = relationship("ProductModel", back_populates="sunset_plans")  # disabled to prevent collision with product_os
