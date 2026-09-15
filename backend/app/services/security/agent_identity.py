"""Autonomous AI Agent Identity & Security Governance Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

class AgentSecurityGovernanceService:
    def __init__(self, db: Optional[Session] = None):
        self.db = db
        self._agents: List[Dict[str, Any]] = []

    def register_agent(self, agent_id: str, agent_name: str, allowed_tools: List[str], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        record = {
            "id": f"agtid_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "agent_id": agent_id,
            "agent_name": agent_name,
            "allowed_tools": allowed_tools,
            "max_risk_tolerance": 0.5,
            "requires_human_approval": True,
            "is_sandboxed": True,
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._agents.append(record)
        return record

    def is_tool_authorized(self, agent_id: str, tool_name: str, tenant_id: str = "default_tenant") -> bool:
        for a in self._agents:
            if a["agent_id"] == agent_id and a["tenant_id"] == tenant_id:
                return tool_name in a.get("allowed_tools", []) or "*" in a.get("allowed_tools", [])
        return False
