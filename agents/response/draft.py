"""Response draft generator creating professional consultative response drafts."""

from typing import Any, Dict, Optional, Tuple


class ResponseDraftGenerator:
    """Generates human-reviewable response drafts based on intent and context."""

    @staticmethod
    def generate_draft(
        intent: str, next_action: str, context: Dict[str, Any]
    ) -> Tuple[Optional[str], Optional[str]]:
        """Returns (subject, body)."""
        biz_name = context.get("business_name", "Team")

        if next_action == "SCHEDULE_MEETING":
            subject = f"Re: Discussion with {biz_name}"
            body = (
                f"Hi {biz_name} team,\n\n"
                f"Thank you for your interest! We would be delighted to schedule a brief 10-minute call to discuss your goals.\n\n"
                f"Would any of the following times work for you next week?\n"
                f"- Tuesday at 10:00 AM\n- Wednesday at 2:00 PM\n\n"
                f"Best regards,\nNorth's Development Team"
            )
            return subject, body

        if next_action == "PROVIDE_PRICE_RANGE":
            subject = f"Re: Service Overview & Pricing for {biz_name}"
            body = (
                f"Hi {biz_name} team,\n\n"
                f"Thank you for asking about our pricing. Our custom service solutions typically range from basic "
                f"package options to comprehensive full-service implementations depending on your specific requirements.\n\n"
                f"To provide an accurate estimate, could you let us know if you have a specific target timeline or key features in mind?\n\n"
                f"Best regards,\nNorth's Development Team"
            )
            return subject, body

        if next_action == "REPLY_WITH_DETAILS":
            subject = f"Re: Additional Information for {biz_name}"
            body = (
                f"Hi {biz_name} team,\n\n"
                f"Thank you for connecting with us! We specialize in digital presence optimization, automated lead management, "
                f"and business growth systems designed specifically for growing companies.\n\n"
                f"Would you be open to a brief call to see how we can assist your team?\n\n"
                f"Best regards,\nNorth's Development Team"
            )
            return subject, body

        return None, None
