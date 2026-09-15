"""Engineering Operating System AI Agents for Phase 61."""

from agents.engineering_os.architecture_agent import ArchitectureAgent
from agents.engineering_os.code_review_agent import CodeReviewAgent
from agents.engineering_os.cicd_deployment_agent import CicdDeploymentAgent
from agents.engineering_os.testing_quality_agent import TestingQualityAgent
from agents.engineering_os.sre_observability_agent import SreObservabilityAgent
from agents.engineering_os.incident_response_agent import IncidentResponseAgent
from agents.engineering_os.security_dependency_agent import SecurityDependencyAgent
from agents.engineering_os.dora_finops_agent import DoraFinopsAgent
from agents.engineering_os.developer_copilot_agent import DeveloperCopilotAgent

DoraFinOpsAgent = DoraFinopsAgent

__all__ = [
    "ArchitectureAgent",
    "CodeReviewAgent",
    "CicdDeploymentAgent",
    "TestingQualityAgent",
    "SreObservabilityAgent",
    "IncidentResponseAgent",
    "SecurityDependencyAgent",
    "DoraFinopsAgent",
    "DoraFinOpsAgent",
    "DeveloperCopilotAgent",
]
