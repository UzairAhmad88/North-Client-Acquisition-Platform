"""
Base Domain Enums and Data Types for Phase 56:
Unified Product Lifecycle, Product Management & Continuous Delivery Intelligence Platform.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ProductType(str, Enum):
    SOFTWARE_PRODUCT = "SOFTWARE_PRODUCT"
    SERVICE = "SERVICE"
    PLATFORM = "PLATFORM"
    INTERNAL_TOOL = "INTERNAL_TOOL"
    AI_PRODUCT = "AI_PRODUCT"
    AUTOMATION = "AUTOMATION"


class LifecycleStage(str, Enum):
    DISCOVERY = "DISCOVERY"
    CONCEPT = "CONCEPT"
    STRATEGY = "STRATEGY"
    PLANNING = "PLANNING"
    VALIDATION = "VALIDATION"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    RELEASE = "RELEASE"
    LAUNCH = "LAUNCH"
    ADOPTION = "ADOPTION"
    OPTIMIZATION = "OPTIMIZATION"
    MATURITY = "MATURITY"
    SUNSET = "SUNSET"
    # Exceptional states
    PAUSED = "PAUSED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class FeedbackType(str, Enum):
    BUG = "BUG"
    FEATURE_REQUEST = "FEATURE_REQUEST"
    USABILITY = "USABILITY"
    PERFORMANCE = "PERFORMANCE"
    PRICING = "PRICING"
    DOCUMENTATION = "DOCUMENTATION"
    SUPPORT = "SUPPORT"
    COMPLAINT = "COMPLAINT"
    PRAISE = "PRAISE"
    IDEA = "IDEA"
    UNKNOWN = "UNKNOWN"


class RequirementPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RequirementCategory(str, Enum):
    FUNCTIONAL = "FUNCTIONAL"
    NON_FUNCTIONAL = "NON_FUNCTIONAL"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    RELIABILITY = "RELIABILITY"
    ACCESSIBILITY = "ACCESSIBILITY"
    COMPLIANCE = "COMPLIANCE"
    AI = "AI"
    INTEGRATION = "INTEGRATION"
    OPERATIONAL = "OPERATIONAL"


class BacklogItemType(str, Enum):
    INITIATIVE = "INITIATIVE"
    EPIC = "EPIC"
    FEATURE = "FEATURE"
    STORY = "STORY"
    TASK = "TASK"
    BUG = "BUG"
    TECH_DEBT = "TECH_DEBT"
    RESEARCH = "RESEARCH"
    SPIKE = "SPIKE"


class PrioritizationFramework(str, Enum):
    RICE = "RICE"
    WSJF = "WSJF"
    MOSCOW = "MOSCOW"
    VALUE_VS_EFFORT = "VALUE_VS_EFFORT"
    COST_OF_DELAY = "COST_OF_DELAY"
    CUSTOM_WEIGHTED = "CUSTOM_WEIGHTED"


class RoadmapHorizon(str, Enum):
    NOW = "NOW"
    NEXT = "NEXT"
    LATER = "LATER"
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class RoadmapScenario(str, Enum):
    BASE_PLAN = "BASE_PLAN"
    ACCELERATED = "ACCELERATED"
    CONSTRAINED = "CONSTRAINED"
    GROWTH = "GROWTH"
    RISK_REDUCED = "RISK_REDUCED"


class SprintStatus(str, Enum):
    PLANNING = "PLANNING"
    READY = "READY"
    ACTIVE = "ACTIVE"
    REVIEW = "REVIEW"
    RETROSPECTIVE = "RETROSPECTIVE"
    COMPLETED = "COMPLETED"


class ReleaseReadinessStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    READY_FOR_SIGN_OFF = "READY_FOR_SIGN_OFF"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RELEASED = "RELEASED"


class FeatureFlagState(str, Enum):
    OFF = "OFF"
    SHADOW = "SHADOW"
    INTERNAL = "INTERNAL"
    CANARY = "CANARY"
    PERCENTAGE = "PERCENTAGE"
    SEGMENT = "SEGMENT"
    FULL = "FULL"


class ProductHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    STABLE = "STABLE"
    WATCH = "WATCH"
    AT_RISK = "AT_RISK"
    CRITICAL = "CRITICAL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class SunsetStage(str, Enum):
    CANDIDATE = "CANDIDATE"
    ANALYSIS = "ANALYSIS"
    GOVERNANCE_REVIEW = "GOVERNANCE_REVIEW"
    APPROVED = "APPROVED"
    DEPRECATION = "DEPRECATION"
    MIGRATION = "MIGRATION"
    SUNSET_COMPLETED = "SUNSET_COMPLETED"
