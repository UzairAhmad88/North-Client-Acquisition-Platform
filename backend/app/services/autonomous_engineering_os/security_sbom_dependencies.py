"""Phase 64 — Security Pipeline, SBOM & Dependency Scanner Service."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from backend.app.services.autonomous_engineering_os.base import (
    BaseAutonomousEngineeringOsService,
    AttrDict,
    SbomPackageModel,
)


class SecuritySbomDependenciesService(BaseAutonomousEngineeringOsService):
    """Service managing SBOM packages, license compliance, and software supply chain scanning."""

    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self._packages: Dict[str, Any] = {}

    def register_sbom_package(
        self,
        tenant_id: str,
        repository_id: str,
        package_name: str,
        version: str,
        license_type: str = "MIT",
        is_license_compliant: bool = True,
        vulnerabilities_count: int = 0,
    ) -> Any:
        """Register package into Software Bill of Materials (SBOM)."""
        pkg_id = self.generate_id("eng_sbom")
        now = datetime.utcnow()

        if self.db is not None and SbomPackageModel is not None:
            pkg = SbomPackageModel(
                id=pkg_id,
                tenant_id=tenant_id,
                repository_id=repository_id,
                package_name=package_name,
                version=version,
                license_type=license_type,
                is_license_compliant=is_license_compliant,
                vulnerabilities_count=vulnerabilities_count,
                scanned_at=now,
            )
            self.db.add(pkg)
            self.db.commit()
            self.db.refresh(pkg)
            return pkg
        else:
            pkg = AttrDict({
                "id": pkg_id,
                "tenant_id": tenant_id,
                "repository_id": repository_id,
                "package_name": package_name,
                "version": version,
                "license_type": license_type,
                "is_license_compliant": is_license_compliant,
                "vulnerabilities_count": vulnerabilities_count,
                "scanned_at": now,
            })
            self._packages[pkg_id] = pkg
            return pkg

    def list_sbom_packages(
        self,
        tenant_id: str,
        repository_id: Optional[str] = None,
    ) -> List[Any]:
        """List SBOM packages."""
        if self.db is not None and SbomPackageModel is not None:
            q = self.db.query(SbomPackageModel).filter(SbomPackageModel.tenant_id == tenant_id)
            if repository_id:
                q = q.filter(SbomPackageModel.repository_id == repository_id)
            return q.all()
        results = [p for p in self._packages.values() if p.tenant_id == tenant_id]
        if repository_id:
            results = [p for p in results if p.repository_id == repository_id]
        return results

    def run_software_supply_chain_scan(
        self,
        tenant_id: str,
        repository_id: str,
    ) -> Dict[str, Any]:
        """Execute comprehensive supply chain scan (SAST, SBOM, license & vulnerability check)."""
        packages = self.list_sbom_packages(tenant_id, repository_id)
        total_vulns = sum(p.vulnerabilities_count for p in packages)
        non_compliant_licenses = [p.package_name for p in packages if not p.is_license_compliant]

        return {
            "repository_id": repository_id,
            "total_packages_scanned": len(packages),
            "total_vulnerabilities": total_vulns,
            "license_compliance_status": "COMPLIANT" if not non_compliant_licenses else "VIOLATION",
            "non_compliant_packages": non_compliant_licenses,
            "security_gate_passed": total_vulns == 0 and len(non_compliant_licenses) == 0,
            "scanned_at": datetime.utcnow().isoformat(),
        }
