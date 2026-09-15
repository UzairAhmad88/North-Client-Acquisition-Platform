"""Audit output validator defending against fact fabrication in AI model outputs."""

from typing import Any, Dict, List
from agents.audit.schemas import AuditFindingItem


class AuditOutputValidator:
    """Defends against unsupported AI claims and validates audit findings structure."""

    ALLOWED_SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH"}
    ALLOWED_CONFIDENCES = {"HIGH", "MEDIUM", "LOW"}
    ALLOWED_CATEGORIES = {
        "website_health",
        "seo",
        "mobile",
        "lead_capture",
        "contact_information",
        "business_consistency",
        "security",
        "digital_presence",
    }

    @classmethod
    def validate_audit_output(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        raw_findings = data.get("findings", [])
        validated_findings: List[Dict[str, Any]] = []

        for f in raw_findings:
            if not isinstance(f, dict):
                continue

            # Ensure valid category
            cat = str(f.get("category", "website_health")).lower()
            if cat not in cls.ALLOWED_CATEGORIES:
                cat = "website_health"

            # Ensure valid severity and confidence
            sev = str(f.get("severity", "INFO")).upper()
            if sev not in cls.ALLOWED_SEVERITIES:
                sev = "INFO"

            conf = str(f.get("confidence", "HIGH")).upper()
            if conf not in cls.ALLOWED_CONFIDENCES:
                conf = "MEDIUM"

            title = str(f.get("title", "Digital Presence Observation")).strip()
            desc = str(f.get("description", "No details provided.")).strip()

            validated_findings.append({
                "finding_id": f.get("finding_id", ""),
                "category": cat,
                "title": title,
                "description": desc,
                "severity": sev,
                "confidence": conf,
                "evidence": f.get("evidence", []),
                "affected_area": f.get("affected_area", "General Digital Presence"),
                "limitations": f.get("limitations", []),
            })

        data["findings"] = validated_findings
        return data
