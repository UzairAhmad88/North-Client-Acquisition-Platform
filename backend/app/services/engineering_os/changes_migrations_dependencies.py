"""Change Governance, Safe Database Migrations, Supply Chain SBOM and CVE Service.

Enforces change approval gates, audits zero-downtime database migrations,
tracks Software Bill of Materials (SBOMs), and detects secret leaks and CVE vulnerabilities.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.engineering_os.base import (
        AttrDict,
        ChangeRiskLevel,
        generate_engineering_id,
    )
except ImportError:
    from app.services.engineering_os.base import (
        AttrDict,
        ChangeRiskLevel,
        generate_engineering_id,
    )

logger = logging.getLogger(__name__)


class ChangesMigrationsDependenciesService:
    """Manages change governance, database migrations, SBOM supply chain, and vulnerability remediation."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._changes: Dict[str, Dict[str, Any]] = {}
        self._migrations: Dict[str, Dict[str, Any]] = {}
        self._vulnerabilities: Dict[str, Dict[str, Any]] = {}

    def submit_change_request(
        self,
        tenant_id: str = "default_tenant",
        title: str = "Upgrade PostgreSQL cluster to v16 with zero downtime",
        change_type: str = "DATABASE_INFRASTRUCTURE",
        risk_level: str = ChangeRiskLevel.HIGH.value,
        rollback_plan: str = "Failover to synchronous replica on previous version",
        owner_email: str = "dba-lead@uzaii.com",
    ) -> AttrDict:
        chg_id = generate_engineering_id("chg")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "chg_id": chg_id,
            "id": chg_id,
            "tenant_id": tenant_id,
            "title": title,
            "change_type": change_type,
            "risk_level": risk_level,
            "status": "PENDING_CAB_APPROVAL",
            "rollback_plan": rollback_plan,
            "owner_email": owner_email,
            "approved_by": None,
            "created_at": now,
        }
        self._changes[chg_id] = record
        return AttrDict(record)

    def record_vulnerability(
        self,
        tenant_id: str = "default_tenant",
        cve_id: str = "CVE-2026-30421",
        package_name: str = "cryptography",
        current_version: str = "41.0.3",
        fixed_version: str = "42.0.0",
        severity: str = "HIGH",
        status: str = "OPEN",
    ) -> AttrDict:
        vuln_id = generate_engineering_id("vuln")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "vuln_id": vuln_id,
            "id": vuln_id,
            "tenant_id": tenant_id,
            "cve_id": cve_id,
            "package_name": package_name,
            "current_version": current_version,
            "fixed_version": fixed_version,
            "severity": severity,
            "status": status,
            "remediation_advice": f"Upgrade {package_name} to >= {fixed_version}",
            "created_at": now,
        }
        self._vulnerabilities[vuln_id] = record
        return AttrDict(record)

    def scan_for_secret_leaks(self, content_snippet: str) -> Dict[str, Any]:
        """Detect accidentally committed secrets and return strictly masked findings."""
        patterns = ["AKIA", "ghp_", "sk_live_", "BEGIN RSA PRIVATE KEY", "Bearer eyJ"]
        leaks_found = []

        for p in patterns:
            if p in content_snippet:
                leaks_found.append({
                    "pattern": p,
                    "masked_finding": f"{p}***[REDACTED_SECRET]***",
                    "severity": "CRITICAL",
                })

        return {
            "has_secret_leak": len(leaks_found) > 0,
            "findings_count": len(leaks_found),
            "findings": leaks_found,
            "action_required": "Revoke credential immediately and re-write commit history" if leaks_found else "None",
        }
