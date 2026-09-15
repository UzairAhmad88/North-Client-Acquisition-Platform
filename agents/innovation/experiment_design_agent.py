"""
Experiment Design Agent for Phase 55.
Designs empirical validation experiments (A/B tests, prototypes, pricing tests, surveys).
"""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )
except ImportError:
    from app.services.innovation.service import (
        InnovationPlatformService,
        global_innovation_service,
    )

logger = logging.getLogger(__name__)


class ExperimentDesignAgent(BaseAgent):
    """Designs bounded empirical experiments with sample sizes and statistical parameters."""

    agent_id = "experiment_design_agent"
    name = "Experiment Design Agent"
    version = "1.0"
    description = "Formulates rigorous validation experiments with target populations and duration parameters."
    permissions = {
        AgentPermission.READ_INNOVATION,
        AgentPermission.DESIGN_EXPERIMENT,
    }

    def __init__(self, service: Optional[InnovationPlatformService] = None):
        super().__init__()
        self.service = service or global_innovation_service

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        ws_id = context.metadata.get("workspace_id")
        hyp_id = context.metadata.get("hypothesis_id", "hyp_default")
        title = context.metadata.get("title", "Empirical Validation Test")
        exp_type = context.metadata.get("experiment_type", "AB_TEST")
        sample_size = context.metadata.get("sample_size", 200)

        exp = self.service.experiments.design_experiment(
            workspace_id=ws_id,
            hypothesis_id=hyp_id,
            title=title,
            sample_size=sample_size,
        )
        return {"status": "SUCCESS", "experiment": exp}
