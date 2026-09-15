"""Recipient and Business consistency validator rule."""

from typing import Any, Dict, Optional
from agents.core.risk.models import RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class RecipientBusinessMismatchRule(RiskRule):
    rule_id = "R-RECIPIENT-MISMATCH"
    category = "RECIPIENT"
    severity = "CRITICAL"
    description = "Detects when recipient email or contact belongs to a different business than the targeted lead/business."

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        expected_business_id = str(artifact.business_id) if artifact.business_id else None
        context_business_id = str(context.get("business_id")) if context.get("business_id") else None

        if expected_business_id and context_business_id and expected_business_id != context_business_id:
            return RiskFindingDetail(
                rule_id=self.rule_id,
                category=self.category,
                severity=self.severity,
                message=f"Recipient business mismatch: artifact business ({expected_business_id}) != context business ({context_business_id}).",
                evidence_reference="Cross-business recipient validation failure",
                remediation="Ensure the draft recipient belongs to the target business profile.",
            )

        recipient_email = artifact.metadata.get("recipient_email")
        business_email = context.get("business_email")

        # If recipient email domain differs drastically from business email domain and both are known
        if recipient_email and business_email and "@" in recipient_email and "@" in business_email:
            rec_domain = recipient_email.split("@")[-1].lower()
            biz_domain = business_email.split("@")[-1].lower()

            # Ignore generic public email domains like gmail, yahoo, outlook
            generic_domains = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"}
            if rec_domain not in generic_domains and biz_domain not in generic_domains and rec_domain != biz_domain:
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message=f"Recipient domain '{rec_domain}' does not match business email domain '{biz_domain}'.",
                    evidence_reference=f"Domain mismatch ({rec_domain} vs {biz_domain})",
                    remediation="Verify that recipient email address corresponds to the targeted business entity.",
                )

        return None
