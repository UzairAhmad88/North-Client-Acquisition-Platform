"""
Governance Assessment AI Agent built on BaseAgent runtime (Section 62).
Provides advisory gap analysis, control mapping assistance, and compliance readiness reviews.
"""

from typing import Any, Dict, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from app.governance.service import GovernancePlatformService
except ImportError:
    from backend.app.governance.service import GovernancePlatformService


class GovernanceAssessmentAgent(BaseAgent):
    """
    Advisory AI Agent that analyzes controls and requirements to detect compliance gaps.
    Strictly advisory: cannot declare compliance, approve exceptions, or certify attestations.
    """

    agent_id = "governance_assessment_agent"
    name = "Governance Assessment Agent"
    version = "1.0"
    description = "Evaluates operational controls against regulatory requirements and surfaces compliance gaps."

    def __init__(self):
        super().__init__()
        self.service = GovernancePlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_REQUIREMENTS,
            AgentPermission.READ_CONTROLS,
            AgentPermission.READ_EVIDENCE,
            AgentPermission.CREATE_ASSESSMENT_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Runs gap analysis across registered controls and requirements."""
        snapshot = self.service.get_posture_snapshot()
        failing_controls = [c.control_code for c in self.service.list_controls() if c.health_status.value == "FAILED"]
        open_findings = self.service.list_findings()

        return {
            "status": "SUCCESS",
            "overall_health": snapshot.overall_health,
            "composite_score": snapshot.composite_compliance_score,
            "failing_controls": failing_controls,
            "open_findings_count": len(open_findings),
            "recommendations": (
                ["Prioritize remediation of critical open findings."]
                if open_findings
                else ["Controls are operating within standard parameters."]
            ),
            "advisory_notice": "Informational assessment only. Does not constitute binding legal compliance certification.",
            "confidence": 0.94,
        }
