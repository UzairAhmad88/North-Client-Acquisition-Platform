"""Unified Customer Success & Client Relationship Intelligence Subsystem (Phase 41)."""

from app.customer_success.base import (
    ClientLifecycleStage,
    RelationshipStrength,
    DecisionRole,
    HealthBand,
    RiskCategory,
    OpportunityType,
    RenewalStatus,
    SurveyType,
    SentimentLabel,
    GoalStatus,
    SuccessPlanStatus,
    HealthFactorScore,
    HealthCalculationResult,
    TimelineEventData,
)
from app.customer_success.health_engine import HealthScoringEngine
from app.customer_success.timeline import ClientTimelineAggregator
from app.customer_success.client_360 import Client360Synthesizer
from app.customer_success.authorization import CustomerSuccessAuthorizationManager
from app.customer_success.service import CustomerSuccessPlatformService

__all__ = [
    "ClientLifecycleStage",
    "RelationshipStrength",
    "DecisionRole",
    "HealthBand",
    "RiskCategory",
    "OpportunityType",
    "RenewalStatus",
    "SurveyType",
    "SentimentLabel",
    "GoalStatus",
    "SuccessPlanStatus",
    "HealthFactorScore",
    "HealthCalculationResult",
    "TimelineEventData",
    "HealthScoringEngine",
    "ClientTimelineAggregator",
    "Client360Synthesizer",
    "CustomerSuccessAuthorizationManager",
    "CustomerSuccessPlatformService",
]
