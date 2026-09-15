"""Software Bill of Materials (SBOM) Scanning Service."""
import uuid
from typing import List, Dict, Any, Optional, Optional
from datetime import datetime, timezone

class SbomService:
    def __init__(self, db: Optional[Any] = None):
        self.db = db
        self._components: List[Dict[str, Any]] = []

    def scan_sbom(self, application_name: str, packages: List[Dict[str, str]], tenant_id: str = "default_tenant") -> Dict[str, Any]:
        findings = []
        for pkg in packages:
            name = pkg.get("name", "")
            ver = pkg.get("version", "")
            has_vuln = "vulnerable" in name.lower() or ver.startswith("0.0.")
            rec = {
                "id": f"sbom_{uuid.uuid4().hex[:12]}",
                "tenant_id": tenant_id,
                "application_name": application_name,
                "component_name": name,
                "version": ver,
                "license": pkg.get("license", "MIT"),
                "vulnerabilities_count": 1 if has_vuln else 0,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            self._components.append(rec)
            if has_vuln:
                findings.append(rec)

        return {
            "application": application_name,
            "scanned_packages": len(packages),
            "vulnerable_packages": len(findings),
            "findings": findings,
        }
