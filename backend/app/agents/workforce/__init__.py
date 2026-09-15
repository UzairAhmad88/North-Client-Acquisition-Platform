"""
Phase 85 Workforce Agents Directory
"""

from app.agents.workforce.workforce_orchestrator import WorkforceOrchestratorAgent
from app.agents.workforce.hr_agent import HrAgentAgent
from app.agents.workforce.team_lead_agent import TeamLeadAgentAgent
from app.agents.workforce.performance_agent import PerformanceAgentAgent
from app.agents.workforce.safety_agent import SafetyAgentAgent
from app.agents.workforce.consensus_agent import ConsensusAgentAgent
from app.agents.workforce.workforce_copilot import WorkforceCopilotAgent

__all__ = [
    "WorkforceOrchestratorAgent",
    "HrAgentAgent",
    "TeamLeadAgentAgent",
    "PerformanceAgentAgent",
    "SafetyAgentAgent",
    "ConsensusAgentAgent",
    "WorkforceCopilotAgent",
]
