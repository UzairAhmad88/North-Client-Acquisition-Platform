"""
Agents for Phase 49: Unified Process Intelligence & Operations.
"""

from agents.process_intelligence.automation import AutomationCandidateAgent
from agents.process_intelligence.discovery import ProcessIntelligenceAgent
from agents.process_intelligence.optimization import ProcessOptimizationAgent

# Phase 78 Process Intelligence Agents
from app.agents.process import (
    ProcessOrchestrator,
    DiscoveryAgent,
    ConformanceAgent,
    BottleneckAgent,
    RootCauseAgent,
    ProcessAnalystAgent,
    SimulationAgent,
    OptimizationAgent,
    AutomationAgent,
    ProcessRiskAgent,
    ProcessComplianceAgent,
    CaseRoutingAgent,
    ProcessChangeAgent,
    ProcessCopilot,
)

__all__ = [
    "ProcessIntelligenceAgent",
    "ProcessOptimizationAgent",
    "AutomationCandidateAgent",
    "ProcessOrchestrator",
    "DiscoveryAgent",
    "ConformanceAgent",
    "BottleneckAgent",
    "RootCauseAgent",
    "ProcessAnalystAgent",
    "SimulationAgent",
    "OptimizationAgent",
    "AutomationAgent",
    "ProcessRiskAgent",
    "ProcessComplianceAgent",
    "CaseRoutingAgent",
    "ProcessChangeAgent",
    "ProcessCopilot",
]

