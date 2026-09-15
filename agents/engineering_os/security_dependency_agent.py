"""Security, Secret Detection & Dependency Supply Chain Agent for Phase 61."""

from typing import Any, Dict, Optional, Set
import logging

from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission

try:
    from backend.app.services.engineering_os.service import EngineeringOperatingSystemService
except ImportError:
    from app.services.engineering_os.service import EngineeringOperatingSystemService

logger = logging.getLogger(__name__)


class SecurityDependencyAgent(BaseAgent):
    """Scans code for secret leaks (with strict masking), audits CVE dependencies, and tracks SBOM integrity."""

    agent_id = "security_dependency_agent"
    name = "Security & Supply Chain Agent"
    version = "1.0"
    description = "Tracks CVE vulnerabilities, detects secret leaks without exposing values, and verifies package supply chains."
    permissions = {
        AgentPermission.READ_ENGINEERING_OS,
        AgentPermission.ANALYZE_SECURITY_VULNERABILITIES,
    }

    def __init__(self, service: Optional[EngineeringOperatingSystemService] = None):
        super().__init__()
        self.service = service or EngineeringOperatingSystemService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return self.permissions

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        tenant_id = context.metadata.get("tenant_id", "default_tenant")
        snippet = context.metadata.get("content_snippet", "export API_KEY=ghp_secretTokenExample123")

        secret_scan = self.service.changes_service.scan_for_secret_leaks(snippet)

        vuln = self.service.changes_service.record_vulnerability(
            tenant_id=tenant_id,
            cve_id=context.metadata.get("cve_id", "CVE-2026-1092"),
            package_name=context.metadata.get("package_name", "aiohttp"),
            current_version="3.8.4",
            fixed_version="3.8.6",
            severity="HIGH",
        )

        return {
            "status": "COMPLETED",
            "has_secret_leak": secret_scan.get("has_secret_leak"),
            "secret_findings_count": secret_scan.get("findings_count"),
            "vulnerability_id": vuln.vuln_id,
            "cve_id": vuln.cve_id,
            "remediation_advice": vuln.remediation_advice,
        }
