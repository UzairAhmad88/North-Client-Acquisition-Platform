"""AI Coding Agents Workspace & Boundary Manager Service."""
from typing import Dict, Any, List, Optional

class AiCodingAgentsManagerService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db

    def list_registered_agents(self) -> List[Dict[str, Any]]:
        return [
            {"agent_id": "planner_agent", "role": "PLANNER", "action_limit": "LOW_RISK_WRITE"},
            {"agent_id": "coding_agent", "role": "CODER", "action_limit": "MEDIUM_RISK_WRITE"},
            {"agent_id": "review_agent", "role": "REVIEWER", "action_limit": "READ"},
            {"agent_id": "sre_agent", "role": "SRE", "action_limit": "MEDIUM_RISK_WRITE"},
        ]
