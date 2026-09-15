"""Channel and recipient format compatibility validator rule."""

import re
from typing import Any, Dict, Optional
from agents.core.risk.models import RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class ChannelRecipientFormatRule(RiskRule):
    rule_id = "R-CHANNEL-FORMAT-MISMATCH"
    category = "CHANNEL"
    severity = "CRITICAL"
    description = "Enforces channel-recipient format compatibility (e.g. EMAIL requires email syntax, SMS requires phone number format)."

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        channel = (artifact.channel or "EMAIL").upper()
        recipient_val = (
            artifact.metadata.get("recipient_email")
            or artifact.metadata.get("recipient_phone")
            or artifact.metadata.get("recipient")
            or ""
        )

        if channel == "EMAIL":
            if recipient_val and ("@" not in recipient_val or "." not in recipient_val.split("@")[-1]):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message=f"Channel 'EMAIL' requires a valid email recipient, got '{recipient_val}'.",
                    evidence_reference="Email regex validation failure",
                    remediation="Provide a valid email address as recipient for EMAIL channel outreach.",
                )

        elif channel in ("SMS", "WHATSAPP"):
            if recipient_val and "@" in recipient_val:
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message=f"Channel '{channel}' requires a phone number recipient, got email address '{recipient_val}'.",
                    evidence_reference="Phone recipient mismatch",
                    remediation=f"Provide a valid phone number as recipient for {channel} channel outreach.",
                )

        return None
