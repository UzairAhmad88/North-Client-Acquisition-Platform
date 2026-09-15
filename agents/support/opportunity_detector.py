"""Opportunity Detector Engine for identifying commercial expansion signals from support dialogues."""

from typing import Optional
from agents.support.models import OpportunityDetectionResult


class OpportunityDetectorEngine:
    """Detects legitimate commercial opportunities from client inquiries and drafts opportunity signals for human review."""

    def detect_opportunity(
        self,
        project_id: str,
        title: str,
        description: str,
    ) -> OpportunityDetectionResult:
        """Scan client message for new feature requests, automation needs, or expansion opportunities."""
        full_text = f"{title.lower()} {description.lower()}"

        if any(kw in full_text for kw in ["mobile app", "ios", "android", "flutter"]):
            return OpportunityDetectionResult(
                project_id=project_id,
                opportunity_detected=True,
                opportunity_type="NEW_PROJECT",
                title=f"New Mobile Application Project: {title[:40]}",
                description="Client inquired about mobile app development for iOS and Android.",
                estimated_value_range="PKR 500,000 - 1,200,000",
                confidence=0.92,
                requires_sales_review=True,
            )

        if any(kw in full_text for kw in ["automate", "cron", "automatic report", "whatsapp notification", "crm integration"]):
            return OpportunityDetectionResult(
                project_id=project_id,
                opportunity_detected=True,
                opportunity_type="AUTOMATION",
                title=f"Workflow Automation Enhancement: {title[:40]}",
                description="Client requested automated notification or background data sync workflow.",
                estimated_value_range="PKR 75,000 - 200,000",
                confidence=0.88,
                requires_sales_review=True,
            )

        if any(kw in full_text for kw in ["new feature", "add page", "extra portal", "dashboard upgrade"]):
            return OpportunityDetectionResult(
                project_id=project_id,
                opportunity_detected=True,
                opportunity_type="NEW_FEATURE",
                title=f"Feature Expansion: {title[:40]}",
                description="Client requested functional expansion beyond original deliverables.",
                estimated_value_range="PKR 50,000 - 150,000",
                confidence=0.85,
                requires_sales_review=True,
            )

        return OpportunityDetectionResult(
            project_id=project_id,
            opportunity_detected=False,
            opportunity_type="NEW_FEATURE",
            title="No Expansion Signal",
            description="Routine support inquiry without commercial expansion signals.",
            confidence=0.95,
            requires_sales_review=False,
        )
