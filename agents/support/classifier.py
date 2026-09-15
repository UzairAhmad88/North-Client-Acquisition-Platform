"""Support Request Classifier & Triage Engine."""

from typing import Optional
from agents.support.models import SupportClassificationResult


class SupportClassifierEngine:
    """Classifies client support tickets into explicit operational buckets."""

    def classify_request(
        self,
        request_id: Optional[str],
        title: str,
        description: str,
        category: str = "APPLICATION",
    ) -> SupportClassificationResult:
        """Classify incoming client request into DEFECT, SUPPORT, MAINTENANCE, INCIDENT, CHANGE_REQUEST, NEW_PROJECT, QUESTION, TRAINING, BILLING."""
        title_lower = title.lower()
        desc_lower = description.lower()
        full_text = f"{title_lower} {desc_lower}"

        # 1. New Project Detection
        if any(kw in full_text for kw in ["build a new app", "separate system", "new mobile app", "new website", "complete redesign", "another portal"]):
            return SupportClassificationResult(
                request_id=request_id,
                title=title,
                category=category,
                classification="NEW_PROJECT",
                priority="HIGH",
                severity="LOW",
                confidence=0.92,
                reasoning="Request describes a major standalone application outside the scope of the delivered system. Routed to Opportunity & Discovery workflow.",
                is_new_project=True,
            )

        # 2. Scope Change Detection
        if any(kw in full_text for kw in ["add feature", "new feature", "add whatsapp", "add integration", "change requirement", "modify layout", "we also need"]):
            return SupportClassificationResult(
                request_id=request_id,
                title=title,
                category=category,
                classification="CHANGE_REQUEST",
                priority="MEDIUM",
                severity="LOW",
                confidence=0.90,
                reasoning="Request requests modifying or adding new functionality to the approved baseline. Routed to Phase 28 Change Management.",
                is_change_request=True,
            )

        # 3. Incident Outage Detection
        if any(kw in full_text for kw in ["outage", "down", "site is down", "database down", "fatal crash", "production unavailable", "security breach", "payment down"]):
            return SupportClassificationResult(
                request_id=request_id,
                title=title,
                category=category,
                classification="INCIDENT",
                priority="CRITICAL",
                severity="CRITICAL",
                confidence=0.95,
                reasoning="Critical production service disruption or outage detected. Escalated as Operational Incident.",
                is_incident=True,
            )

        # 4. Defect Detection (Broken baseline functionality)
        if any(kw in full_text for kw in ["bug", "broken", "error 500", "not working", "crash", "fails to save", "incorrect calculation", "login stops working"]):
            return SupportClassificationResult(
                request_id=request_id,
                title=title,
                category=category,
                classification="DEFECT",
                priority="HIGH",
                severity="HIGH",
                confidence=0.88,
                reasoning="Flaw or malfunction in previously approved functionality. Handled under warranty / defect remediation.",
            )

        # 5. Question / Support / Training
        if any(kw in full_text for kw in ["how do i", "how to", "where is", "help with", "guide", "tutorial", "instructions"]):
            return SupportClassificationResult(
                request_id=request_id,
                title=title,
                category=category,
                classification="SUPPORT",
                priority="MEDIUM",
                severity="LOW",
                confidence=0.85,
                reasoning="General operational guidance or user account assistance.",
            )

        # 6. Maintenance Task
        if any(kw in full_text for kw in ["backup", "upgrade php", "update dependencies", "renew certificate", "routine check"]):
            return SupportClassificationResult(
                request_id=request_id,
                title=title,
                category=category,
                classification="MAINTENANCE",
                priority="MEDIUM",
                severity="LOW",
                confidence=0.88,
                reasoning="Routine maintenance or operational housekeeping task.",
            )

        # Default fallback
        return SupportClassificationResult(
            request_id=request_id,
            title=title,
            category=category,
            classification="SUPPORT",
            priority="MEDIUM",
            severity="MEDIUM",
            confidence=0.75,
            reasoning="Standard support inquiry.",
        )
