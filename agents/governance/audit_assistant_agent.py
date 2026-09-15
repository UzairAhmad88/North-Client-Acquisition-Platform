"""
Audit Assistant AI Agent built on BaseAgent runtime (Section 62).
Compiles evidence packages, tracks audit requests, and drafts management summaries.
"""

from typing import Any, Dict, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from app.governance.service import GovernancePlatformService
except ImportError:
    from backend.app.governance.service import GovernancePlatformService


class AuditAssistantAgent(BaseAgent):
    """
    Advisory agent assisting human auditors with evidence package preparation.
    Strictly prohibited from certifying attestations or closing audit findings.
    """

    agent_id = "audit_assistant_agent"
    name = "Audit Assistant Agent"
    version = "1.0"
    description = "Prepares evidence packages, audits evidence freshness, and drafts audit summaries."

    def __init__(self):
        super().__init__()
        self.service = GovernancePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_AUDITS,
            AgentPermission.READ_EVIDENCE,
            AgentPermission.READ_CONTROLS,
            AgentPermission.CREATE_AUDIT_SUMMARY,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Prepares an audit summary and checks evidence packaging readiness."""
        freshness = self.service.audit_evidence_freshness()
        controls = self.service.list_controls()

        return {
            "status": "SUCCESS",
            "evidence_coverage": {
                "total_items": freshness.get("total_evidence_items", 0),
                "fresh": freshness.get("fresh_count", 0),
                "stale": freshness.get("stale_count", 0),
            },
            "auditable_controls_count": len(controls),
            "readiness_status": "READY" if freshness.get("stale_count", 0) == 0 else "STALE_EVIDENCE_DETECTED",
            "advisory_notice": "Evidence compilation for human auditor review. AI cannot sign formal attestations.",
        }
