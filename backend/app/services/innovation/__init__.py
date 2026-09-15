"""
Phase 55: Unified Product & Innovation Intelligence, Idea Discovery, Validation & R&D Platform Services module.
"""

from backend.app.services.innovation.base import (
    InnovationStage,
    HorizonLevel,
    ProblemStatus,
    IdeaStatus,
    HypothesisStatus,
    ExperimentType,
    ExperimentStatus,
    StatisticalOutcome,
    GateStage,
    GateDecision,
    PivotAction,
)
from backend.app.services.innovation.workspaces import InnovationWorkspaceManager
from backend.app.services.innovation.problems_opportunities import ProblemOpportunityManager
from backend.app.services.innovation.ideas import IdeaManager
from backend.app.services.innovation.hypotheses_assumptions import HypothesisAssumptionManager
from backend.app.services.innovation.experiments_validation import ExperimentValidationManager
from backend.app.services.innovation.concepts_business_cases import ProductConceptBusinessCaseManager
from backend.app.services.innovation.portfolios_gates import PortfolioGateManager
from backend.app.services.innovation.service import (
    InnovationPlatformService,
    global_innovation_service,
)

__all__ = [
    "InnovationStage",
    "HorizonLevel",
    "ProblemStatus",
    "IdeaStatus",
    "HypothesisStatus",
    "ExperimentType",
    "ExperimentStatus",
    "StatisticalOutcome",
    "GateStage",
    "GateDecision",
    "PivotAction",
    "InnovationWorkspaceManager",
    "ProblemOpportunityManager",
    "IdeaManager",
    "HypothesisAssumptionManager",
    "ExperimentValidationManager",
    "ProductConceptBusinessCaseManager",
    "PortfolioGateManager",
    "InnovationPlatformService",
    "global_innovation_service",
]
