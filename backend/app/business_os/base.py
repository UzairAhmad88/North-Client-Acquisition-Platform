"""Base domain models, enums, and dataclasses for Business OS & Executive Intelligence."""

from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# --- Strategy & OKR Enums ---

class ObjectivePriority(str, Enum):
    P0_CRITICAL = "P0_CRITICAL"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_LOW = "P3_LOW"


class ObjectiveStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    AT_RISK = "AT_RISK"
    OFF_TRACK = "OFF_TRACK"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


class KeyResultStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    OFF_TRACK = "OFF_TRACK"
    ACHIEVED = "ACHIEVED"
    MISSED = "MISSED"
    CANCELLED = "CANCELLED"


class InitiativeStatus(str, Enum):
    IDEA = "IDEA"
    EVALUATION = "EVALUATION"
    APPROVED = "APPROVED"
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    AT_RISK = "AT_RISK"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"


class StrategicDependencyState(str, Enum):
    AVAILABLE = "AVAILABLE"
    AT_RISK = "AT_RISK"
    BLOCKED = "BLOCKED"
    RESOLVED = "RESOLVED"
    UNKNOWN = "UNKNOWN"


# --- KPI & Scorecard Enums ---

class KPICategory(str, Enum):
    FINANCIAL = "FINANCIAL"
    SALES = "SALES"
    CLIENT = "CLIENT"
    DELIVERY = "DELIVERY"
    SUPPORT = "SUPPORT"
    AI = "AI"
    OPERATIONS = "OPERATIONS"


class ScorecardStatus(str, Enum):
    EXCEEDING = "EXCEEDING"
    ON_TRACK = "ON_TRACK"
    AT_RISK = "AT_RISK"
    OFF_TRACK = "OFF_TRACK"
    UNKNOWN = "UNKNOWN"


# --- Risk Register Enums ---

class RiskCategory(str, Enum):
    FINANCIAL = "FINANCIAL"
    SALES = "SALES"
    CLIENT = "CLIENT"
    PROJECT = "PROJECT"
    DELIVERY = "DELIVERY"
    SUPPORT = "SUPPORT"
    SECURITY = "SECURITY"
    AI = "AI"
    DATA = "DATA"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONAL = "OPERATIONAL"
    TECHNOLOGY = "TECHNOLOGY"
    RESOURCE = "RESOURCE"
    STRATEGIC = "STRATEGIC"
    REPUTATIONAL = "REPUTATIONAL"


class RiskProbability(str, Enum):
    RARE = "RARE"                   # 1
    UNLIKELY = "UNLIKELY"           # 2
    POSSIBLE = "POSSIBLE"           # 3
    LIKELY = "LIKELY"               # 4
    ALMOST_CERTAIN = "ALMOST_CERTAIN" # 5


class RiskImpact(str, Enum):
    MINOR = "MINOR"                 # 1
    MODERATE = "MODERATE"           # 2
    MAJOR = "MAJOR"                 # 3
    SEVERE = "SEVERE"               # 4
    CRITICAL = "CRITICAL"           # 5


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskLifecycleStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    ASSESSED = "ASSESSED"
    MITIGATION_PLANNED = "MITIGATION_PLANNED"
    MONITORED = "MONITORED"
    MITIGATED = "MITIGATED"
    CLOSED = "CLOSED"
    ACCEPTED = "ACCEPTED"
    TRANSFERRED = "TRANSFERRED"
    ESCALATED = "ESCALATED"


# --- Decision Queue Enums ---

class DecisionStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER_REVIEW"
    DECISION_REQUIRED = "DECISION_REQUIRED"
    DECIDED = "DECIDED"
    IMPLEMENTING = "IMPLEMENTING"
    COMPLETED = "COMPLETED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    CLOSED = "CLOSED"


class DecisionPriority(str, Enum):
    P0_URGENT = "P0_URGENT"
    P1_HIGH = "P1_HIGH"
    P2_MEDIUM = "P2_MEDIUM"
    P3_LOW = "P3_LOW"


# --- Scenario & What-If Enums ---

class ScenarioType(str, Enum):
    BASE = "BASE"
    UPSIDE = "UPSIDE"
    DOWNSIDE = "DOWNSIDE"
    CUSTOM = "CUSTOM"


# --- Business Health & Briefing Enums ---

class BusinessHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    STABLE = "STABLE"
    WATCH = "WATCH"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class BriefingFrequency(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


class AlertSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    TRIGGERED = "TRIGGERED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"


# --- Core Pydantic DTOs ---

class KPISnapshot(BaseModel):
    kpi_id: str
    name: str
    category: KPICategory
    value: Decimal
    previous_value: Optional[Decimal] = None
    target_value: Optional[Decimal] = None
    variance: Optional[Decimal] = None
    variance_pct: Optional[Decimal] = None
    unit: str = ""
    currency: str = "PKR"
    source_domain: str
    version: str = "1.0"
    freshness_seconds: int = 0
    is_stale: bool = False
    status: ScorecardStatus = ScorecardStatus.ON_TRACK
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class HealthDimensionScore(BaseModel):
    dimension_name: str
    score: Decimal  # 0.00 - 100.00
    weight_pct: Decimal  # e.g. 20.00
    status: BusinessHealthStatus
    positive_drivers: List[str] = Field(default_factory=list)
    negative_drivers: List[str] = Field(default_factory=list)
    signals_count: int = 0


class BusinessHealthReport(BaseModel):
    overall_health_score: Decimal  # 0.00 - 100.00
    overall_status: BusinessHealthStatus
    dimensions: Dict[str, HealthDimensionScore] = Field(default_factory=dict)
    key_strengths: List[str] = Field(default_factory=list)
    critical_risks: List[str] = Field(default_factory=list)
    reconciliation_alerts: List[str] = Field(default_factory=list)
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DecisionOption(BaseModel):
    option_id: str
    title: str
    description: str
    expected_benefits: List[str] = Field(default_factory=list)
    expected_costs: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    estimated_impact: str = ""
    confidence: str = "MEDIUM"
    evidence_references: List[str] = Field(default_factory=list)


class ScenarioSimulationResult(BaseModel):
    scenario_id: str
    scenario_name: str
    scenario_type: ScenarioType
    simulated_revenue: Decimal
    simulated_profit: Decimal
    simulated_margin_pct: Decimal
    capacity_utilization_pct: Decimal
    cash_requirement: Decimal
    risk_level: str
    assumptions_applied: Dict[str, Any] = Field(default_factory=dict)
    sensitivity_rankings: List[Dict[str, Any]] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_production_isolated: bool = True
