"""
Canonical base types, enums, and domain schemas for Phase 51: Autonomous Business Strategy, Planning & Goal Optimization Engine.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class StrategicPillar(str, Enum):
    GROWTH = "GROWTH"
    PROFITABILITY = "PROFITABILITY"
    INNOVATION = "INNOVATION"
    CUSTOMER_SUCCESS = "CUSTOMER_SUCCESS"
    OPERATIONAL_EXCELLENCE = "OPERATIONAL_EXCELLENCE"
    TECHNOLOGY = "TECHNOLOGY"
    AI = "AI"
    SECURITY = "SECURITY"
    RELIABILITY = "RELIABILITY"
    MARKET_EXPANSION = "MARKET_EXPANSION"
    TALENT = "TALENT"
    SUSTAINABILITY = "SUSTAINABILITY"


class PlanHorizon(str, Enum):
    SHORT_TERM = "SHORT_TERM"      # 0-3 months
    MEDIUM_TERM = "MEDIUM_TERM"    # 3-12 months
    LONG_TERM = "LONG_TERM"        # 1-3 years
    STRATEGIC = "STRATEGIC"        # 3-5+ years


class ObjectiveStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    OFF_TRACK = "OFF_TRACK"
    ACHIEVED = "ACHIEVED"
    MISSED = "MISSED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"


class InitiativeStatus(str, Enum):
    IDEA = "IDEA"
    EVALUATION = "EVALUATION"
    SIMULATION = "SIMULATION"
    PRIORITIZATION = "PRIORITIZATION"
    APPROVED = "APPROVED"
    PLANNING = "PLANNING"
    EXECUTION = "EXECUTION"
    MONITORING = "MONITORING"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"


class FeasibilityLevel(str, Enum):
    FEASIBLE = "FEASIBLE"
    LIKELY = "LIKELY"
    UNCERTAIN = "UNCERTAIN"
    CHALLENGING = "CHALLENGING"
    UNLIKELY = "UNLIKELY"
    INFEASIBLE = "INFEASIBLE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ConflictSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# --- Pydantic Schemas ---

class StrategicObjective(BaseModel):
    id: Optional[str] = None
    objective_code: str = Field(default_factory=lambda: f"OBJ-{uuid.uuid4().hex[:6].upper()}")
    name: str
    description: Optional[str] = None
    strategic_pillar: StrategicPillar = StrategicPillar.GROWTH
    owner: str = "executive_team"
    priority: str = "HIGH"
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    target_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    baseline_value: float = 0.0
    target_value: float
    current_value: float = 0.0
    unit: str = "USD"
    status: ObjectiveStatus = ObjectiveStatus.ACTIVE
    confidence_score: float = 1.0
    progress_percentage: float = 0.0
    evidence_summary: Optional[str] = None
    version: int = 1


class KeyResult(BaseModel):
    id: Optional[str] = None
    kr_code: str = Field(default_factory=lambda: f"KR-{uuid.uuid4().hex[:6].upper()}")
    objective_id: str
    name: str
    baseline_value: float = 0.0
    target_value: float
    current_value: float = 0.0
    unit: str = "PERCENT"
    progress_percentage: float = 0.0
    measurement_method: str = "AUTOMATED_TELEMETRY"
    source_metric: Optional[str] = None
    owner: str
    confidence: float = 1.0
    deadline: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class StrategicInitiative(BaseModel):
    id: Optional[str] = None
    initiative_code: str = Field(default_factory=lambda: f"INIT-{uuid.uuid4().hex[:6].upper()}")
    title: str
    description: Optional[str] = None
    category: str = "GROWTH"
    owner: str
    status: InitiativeStatus = InitiativeStatus.IDEA
    expected_value_usd: float = 0.0
    estimated_cost_usd: float = 0.0
    required_fte_capacity: float = 1.0
    estimated_duration_weeks: float = 4.0
    priority_score: float = 0.0
    risk_score: float = 0.0
    feasibility_score: float = 1.0
    is_funded: bool = False
    version: int = 1


class StrategicPlan(BaseModel):
    id: Optional[str] = None
    plan_code: str = Field(default_factory=lambda: f"PLAN-{uuid.uuid4().hex[:6].upper()}")
    title: str
    vision_statement: str
    mission_statement: Optional[str] = None
    planning_horizon: PlanHorizon = PlanHorizon.MEDIUM_TERM
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    objectives: List[StrategicObjective] = Field(default_factory=list)
    initiatives: List[StrategicInitiative] = Field(default_factory=list)
    constraints: List[Dict[str, Any]] = Field(default_factory=list)
    assumptions: List[Dict[str, Any]] = Field(default_factory=list)
    total_budget_usd: float = 0.0
    status: str = "DRAFT"
    version: int = 1


class ParetoPlan(BaseModel):
    plan_code: str
    title: str
    growth_score: float
    profitability_score: float
    risk_score: float
    selected_initiatives: List[str]
    total_cost_usd: float
    expected_net_benefit_usd: float
    is_pareto_optimal: bool = True


class StrategicDecision(BaseModel):
    id: Optional[str] = None
    decision_code: str = Field(default_factory=lambda: f"STRAT-DEC-{uuid.uuid4().hex[:6].upper()}")
    question: str
    context_summary: str
    selected_option: Dict[str, Any]
    rejected_options: List[Dict[str, Any]] = Field(default_factory=list)
    rationale: str
    decision_owner: str
    approved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    plan_version: int = 1
