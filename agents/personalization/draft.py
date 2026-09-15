"""Draft generator producing channel-specific personalized outreach drafts."""

import hashlib
from typing import Any, Dict, List, Optional
from agents.personalization.schemas import CommunicationAngle, OutreachDraftPayload, VerifiedSignal


class DraftGenerator:
    """Generates channel-specific personalized communication drafts with low-pressure CTAs."""

    @staticmethod
    def generate_draft(
        business_name: str,
        lead_name: Optional[str],
        primary_angle: CommunicationAngle,
        signals: List[VerifiedSignal],
        channel: str = "EMAIL",
        tone: str = "PROFESSIONAL",
        depth: str = "STANDARD",
        objective: str = "INTRODUCE_SERVICE",
    ) -> OutreachDraftPayload:
        contact_greeting = f"Hi {lead_name.split()[0]}" if lead_name else "Hello"
        biz_display = business_name or "your team"

        # 1. Subject Generation
        if channel == "EMAIL":
            subject = f"A quick observation for {biz_display}"
            if primary_angle.angle_type == "BOOKING":
                subject = f"Online booking idea for {biz_display}"
            elif primary_angle.angle_type == "WEBSITE_IMPROVEMENT":
                subject = f"Digital presence observation for {biz_display}"
            elif primary_angle.angle_type == "LEAD_CAPTURE":
                subject = f"Inquiry flow idea for {biz_display}"
        else:
            subject = None

        # 2. Body Generation based on channel & tone
        if channel == "WHATSAPP" or channel == "SMS":
            body = (
                f"{contact_greeting}, I noticed {biz_display}'s public profile. "
                f"{primary_angle.problem_statement} "
                f"We help local businesses with {primary_angle.value_proposition.lower()} "
                f"Would you be open to a quick 5-minute chat to explore if this could be helpful?"
            )
        elif channel == "LINKEDIN":
            body = (
                f"{contact_greeting},\n\n"
                f"I came across {biz_display} and noticed your work. "
                f"{primary_angle.problem_statement} "
                f"We specialize in {primary_angle.title.lower()} to {primary_angle.value_proposition.lower()}\n\n"
                f"Would it be helpful if I shared a simple example tailored for {biz_display}?"
            )
        else:  # EMAIL (Default)
            obs_detail = ""
            if depth == "DEEP" and len(signals) > 1:
                obs_detail = f"\n\nSpecifically, from your public details: {signals[0].description}."

            body = (
                f"{contact_greeting},\n\n"
                f"I hope you are having a great week. I was reviewing public details for {biz_display} "
                f"and noticed an opportunity regarding your {primary_angle.title.lower()}.\n\n"
                f"{primary_angle.problem_statement}{obs_detail}\n\n"
                f"At North's, we help businesses implement {primary_angle.value_proposition.lower()} "
                f"without complicated setups.\n\n"
                f"Would you be open to a brief conversation next week to see if this could be useful for {biz_display}?\n\n"
                f"Best regards,\nNorth's Development Team"
            )

        # 3. Calculate Content Hash
        content_bytes = f"{subject or ''}:{body}".encode("utf-8")
        content_hash = hashlib.sha256(content_bytes).hexdigest()

        return OutreachDraftPayload(
            channel=channel,
            tone=tone,
            language="en",
            personalization_depth=depth,
            objective=objective,
            subject=subject,
            body=body,
            claims=[],
            risk_level="LOW",
            outreach_readiness="READY",
            approval_status="PENDING_APPROVAL",
            version=1,
            content_hash=content_hash,
        )
