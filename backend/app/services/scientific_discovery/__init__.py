"""
Scientific Discovery Engine Services Package Export (Phase 97)
"""

from app.services.scientific_discovery.question_literature_engine import QuestionLiteratureEngineService
from app.services.scientific_discovery.hypothesis_experiment_design import HypothesisExperimentDesignService
from app.services.scientific_discovery.digital_lab_reproducibility import DigitalLabReproducibilityService
from app.services.scientific_discovery.ai_scientist_network import AiScientistNetworkService
from app.services.scientific_discovery.simulation_causal_math_engine import SimulationCausalMathEngineService
from app.services.scientific_discovery.replication_meta_analysis import ReplicationMetaAnalysisService
from app.services.scientific_discovery.discovery_copilot_governance import DiscoveryCopilotGovernanceService

__all__ = [
    "QuestionLiteratureEngineService",
    "HypothesisExperimentDesignService",
    "DigitalLabReproducibilityService",
    "AiScientistNetworkService",
    "SimulationCausalMathEngineService",
    "ReplicationMetaAnalysisService",
    "DiscoveryCopilotGovernanceService",
]
