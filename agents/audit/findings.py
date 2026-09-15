"""Audit finding classifier mapping observable technical signals to categories and severity."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from agents.audit.schemas import AuditEvidenceItem, AuditFindingItem


class AuditFindingCollector:
    """Classifies and structures audit findings with explicit severity and evidence grounding."""

    SEVERITY_MAP = {
        "NO_HTTPS": "HIGH",
        "SITE_DOWN": "HIGH",
        "MISSING_VIEWPORT": "MEDIUM",
        "NO_CONTACT_CTA": "MEDIUM",
        "PHONE_DISCREPANCY": "MEDIUM",
        "MISSING_META_DESC": "LOW",
        "MISSING_TITLE": "MEDIUM",
        "FORM_DETECTED": "INFO",
        "BOOKING_LINK_DETECTED": "INFO",
        "SECURITY_HEADER_MISSING": "LOW",
    }

    @classmethod
    def create_finding(
        cls,
        code: str,
        category: str,
        title: str,
        description: str,
        evidence_url: Optional[str] = None,
        affected_area: Optional[str] = None,
        severity_override: Optional[str] = None,
        confidence: str = "HIGH",
        details: Optional[str] = None,
    ) -> AuditFindingItem:
        severity = severity_override or cls.SEVERITY_MAP.get(code, "INFO")
        now_str = datetime.now(timezone.utc).isoformat()

        evidence_items = []
        if evidence_url:
            evidence_items.append(
                AuditEvidenceItem(
                    source_url=evidence_url,
                    source_type="WEBSITE",
                    observed_at=now_str,
                    confidence=confidence,
                    details=details or f"Observable signal on {evidence_url}",
                )
            )

        return AuditFindingItem(
            category=category,
            title=title,
            description=description,
            severity=severity,
            confidence=confidence,
            evidence=evidence_items,
            affected_area=affected_area or evidence_url or "General Digital Presence",
        )
