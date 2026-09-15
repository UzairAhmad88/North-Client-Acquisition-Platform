"""
Findings Management Engine (Section 40).
Tracks compliance deficiencies, severity levels, root cause analysis, and remediation progress.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from backend.app.governance.base import (
    FindingSeverity,
    FindingStatus,
    GovernanceFinding,
)


class FindingManager:
    """Manages compliance findings raised from audits, control tests, or security incidents."""

    def __init__(self):
        self._findings: Dict[str, GovernanceFinding] = {}

    def raise_finding(
        self,
        finding_code: str,
        control_code: str,
        title: str,
        description: str,
        severity: FindingSeverity,
        owner_id: str,
        due_date: datetime,
        root_cause: Optional[str] = None,
        evidence_ids: Optional[List[str]] = None
    ) -> GovernanceFinding:
        """Raises a new compliance deficiency finding."""
        if not owner_id:
            raise ValueError("All compliance findings must have an assigned owner.")

        finding = GovernanceFinding(
            finding_code=finding_code,
            control_code=control_code,
            title=title,
            description=description,
            severity=severity,
            root_cause=root_cause,
            owner_id=owner_id,
            status=FindingStatus.OPEN,
            due_date=due_date,
            evidence_ids=evidence_ids or []
        )
        self._findings[finding_code] = finding
        return finding

    def get_finding(self, finding_code: str) -> Optional[GovernanceFinding]:
        return self._findings.get(finding_code)

    def list_findings(self, severity: Optional[FindingSeverity] = None, status: Optional[FindingStatus] = None) -> List[GovernanceFinding]:
        findings = list(self._findings.values())
        if severity:
            findings = [f for f in findings if f.severity == severity]
        if status:
            findings = [f for f in findings if f.status == status]
        return findings

    def update_status(self, finding_code: str, status: FindingStatus) -> GovernanceFinding:
        finding = self._findings.get(finding_code)
        if not finding:
            raise KeyError(f"Finding '{finding_code}' not found.")
        finding.status = status
        return finding
