"""Vulnerability Prioritization & Management Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional

class VulnerabilityManagementService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._vulns: List[Dict[str, Any]] = []

    def record_vulnerability(self, cve_id: str, title: str, cvss_score: float, affected_asset_id: str, exploitability: str = "FUNCTIONAL", tenant_id: str = "default_tenant") -> Dict[str, Any]:
        # Composite Prioritization: CVSS + Exploitability Weight
        weight = 1.3 if exploitability == "HIGH" else 1.1 if exploitability == "FUNCTIONAL" else 0.9
        composite_score = min(10.0, round(cvss_score * weight, 1))
        severity = "CRITICAL" if composite_score >= 9.0 else "HIGH" if composite_score >= 7.0 else "MEDIUM"

        vuln = {
            "id": f"vuln_{uuid.uuid4().hex[:12]}",
            "tenant_id": tenant_id,
            "cve_id": cve_id,
            "title": title,
            "cvss_score": cvss_score,
            "composite_score": composite_score,
            "severity": severity,
            "affected_asset_id": affected_asset_id,
            "exploitability": exploitability,
            "remediation_status": "OPEN",
        }
        self._vulns.append(vuln)
        return vuln

    def list_vulnerabilities(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        return [v for v in self._vulns if v["tenant_id"] == tenant_id]
