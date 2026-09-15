"""
Base domain types and schemas for Phase 53 — Unified Human-AI Collaboration, Decision Room & Augmented Intelligence Platform.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DecisionStatus(str, Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    ANALYSIS = "ANALYSIS"
    REVIEW = "REVIEW"
    DECISION_REQUIRED = "DECISION_REQUIRED"
    DECIDED = "DECIDED"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
    CANCELLED = "CANCELLED"
    ON_HOLD = "ON_HOLD"


class DecisionType(str, Enum):
    STRATEGIC = "STRATEGIC"
    FINANCIAL = "FINANCIAL"
    PRODUCT = "PRODUCT"
    CLIENT = "CLIENT"
    SALES = "SALES"
    PROJECT = "PROJECT"
    RESOURCE = "RESOURCE"
    TECHNICAL = "TECHNICAL"
    AI = "AI"
    SECURITY = "SECURITY"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"
    HIRING = "HIRING"
    PRICING = "PRICING"
    PROCESS = "PROCESS"
    INVESTMENT = "INVESTMENT"
    VENDOR = "VENDOR"
    INFRASTRUCTURE = "INFRASTRUCTURE"


class DecisionImportance(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EvidenceType(str, Enum):
    DATABASE = "DATABASE"
    DOCUMENT = "DOCUMENT"
    MESSAGE = "MESSAGE"
    CLIENT_INPUT = "CLIENT_INPUT"
    METRIC = "METRIC"
    FORECAST = "FORECAST"
    SIMULATION = "SIMULATION"
    KNOWLEDGE = "KNOWLEDGE"
    POLICY = "POLICY"
    AUDIT = "AUDIT"
    SECURITY_EVENT = "SECURITY_EVENT"
    PROJECT_DATA = "PROJECT_DATA"
    FINANCIAL_DATA = "FINANCIAL_DATA"
    AI_ANALYSIS = "AI_ANALYSIS"
    HUMAN_NOTE = "HUMAN_NOTE"


class StatementCategory(str, Enum):
    FACT = "FACT"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    RECOMMENDATION = "RECOMMENDATION"
    UNKNOWN = "UNKNOWN"
    CONFLICTED = "CONFLICTED"


class DisagreementCategory(str, Enum):
    FACTUAL = "FACTUAL"
    ASSUMPTION = "ASSUMPTION"
    INTERPRETATION = "INTERPRETATION"
    PREFERENCE = "PREFERENCE"
    STRATEGIC = "STRATEGIC"
    RISK = "RISK"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WAIVED = "WAIVED"


class ActionExecutionStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    AUTHORIZED = "AUTHORIZED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SpecialistRole(str, Enum):
    FINANCE = "FINANCE"
    SECURITY = "SECURITY"
    OPERATIONS = "OPERATIONS"
    STRATEGY = "STRATEGY"
    CUSTOMER_SUCCESS = "CUSTOMER_SUCCESS"
    TECHNICAL = "TECHNICAL"
    COMPLIANCE = "COMPLIANCE"


class EvidenceItem(BaseModel):
    id: str
    evidence_type: EvidenceType
    source: str
    claim: str
    provenance: Optional[str] = None
    authority: str = "OFFICIAL"
    statement_category: StatementCategory = StatementCategory.FACT
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    freshness: str = "CURRENT"
    meta_info: Dict[str, Any] = Field(default_factory=dict)


class AssumptionItem(BaseModel):
    id: str
    statement: str
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    validated: bool = False
    validator_role: Optional[str] = None
    impact_if_false: str = "MEDIUM"
    meta_info: Dict[str, Any] = Field(default_factory=dict)


class UnknownItem(BaseModel):
    id: str
    question: str
    impact: str = "MEDIUM"
    resolution_path: Optional[str] = None
    resolved: bool = False
    resolved_value: Optional[str] = None


class DecisionOption(BaseModel):
    id: str
    name: str
    description: str
    benefits: List[str] = Field(default_factory=list)
    costs: float = 0.0
    risks: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    resources_required: List[str] = Field(default_factory=list)
    expected_outcome: Optional[str] = None
    uncertainty_level: str = "MEDIUM"
    reversibility: str = "REVERSIBLE"
    composite_score: float = 0.0
    version: int = 1


class DecisionCriterion(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    weight: float = Field(default=1.0, gt=0.0)
    criterion_type: str = "BENEFIT"  # BENEFIT or COST


class DecisionScore(BaseModel):
    id: str
    option_id: str
    criterion_id: str
    raw_score: float = Field(default=0.0, ge=0.0, le=100.0)
    weighted_score: float = 0.0
    justification: Optional[str] = None
    scored_by: str = "AI_ANALYST"


class TradeoffItem(BaseModel):
    id: str
    option_a_id: str
    option_b_id: str
    tradeoff_summary: str
    gains_in_a: List[str] = Field(default_factory=list)
    sacrifices_in_a: List[str] = Field(default_factory=list)


class DecisionRisk(BaseModel):
    id: str
    option_id: Optional[str] = None
    risk_category: str
    description: str
    probability: float = Field(default=0.3, ge=0.0, le=1.0)
    impact: float = Field(default=0.5, ge=0.0, le=1.0)
    risk_score: float = 0.15
    mitigation: Optional[str] = None
    blast_radius: str = "TEAM"


class SpecialistAnalysis(BaseModel):
    id: str
    specialist_role: SpecialistRole
    worker_id: Optional[str] = None
    summary: str
    recommendations: List[str] = Field(default_factory=list)
    key_findings: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    facts: List[str] = Field(default_factory=list)
    inferences: List[str] = Field(default_factory=list)


class AdversarialReview(BaseModel):
    id: str
    reviewer_role: str = "CRITICAL_ANALYST"
    target_option_id: Optional[str] = None
    critique_summary: str
    weak_assumptions: List[str] = Field(default_factory=list)
    unintended_consequences: List[str] = Field(default_factory=list)
    hidden_costs: List[str] = Field(default_factory=list)
    data_gaps: List[str] = Field(default_factory=list)


class DisagreementItem(BaseModel):
    id: str
    topic: str
    disagreement_category: DisagreementCategory
    party_a: str
    view_a: str
    party_b: str
    view_b: str
    status: str = "SURFACED"
    resolution_notes: Optional[str] = None


class DecisionApprovalStep(BaseModel):
    id: str
    step_name: str
    required_role: str
    approver_id: Optional[str] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    decision_notes: Optional[str] = None
    reviewed_at: Optional[datetime] = None


class DecisionActionItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    target_system: str
    target_payload: Dict[str, Any] = Field(default_factory=dict)
    assigned_to: Optional[str] = None
    execution_status: ActionExecutionStatus = ActionExecutionStatus.PENDING_APPROVAL


class PostDecisionReview(BaseModel):
    id: str
    decision_quality_score: float = Field(default=80.0, ge=0.0, le=100.0)
    outcome_rating: str = "NEUTRAL"
    prediction_error: Optional[str] = None
    assumption_error: Optional[str] = None
    execution_error: Optional[str] = None
    model_error: Optional[str] = None
    lessons_learned: List[str] = Field(default_factory=list)
    feed_to_organizational_memory: bool = True
    reviewed_by: str
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)
