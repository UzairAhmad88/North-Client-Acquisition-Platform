"""Claim validation subsystem detecting prohibited and unsupported factual claims."""

import re
from typing import Any, Dict, List, Optional
from agents.core.risk.models import RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class GuaranteeClaimRule(RiskRule):
    rule_id = "R-CLAIM-GUARANTEE"
    category = "CLAIM_ACCURACY"
    severity = "CRITICAL"
    description = "Flags prohibited false guarantees (e.g., guaranteed revenue, rankings, conversions)."

    PATTERNS = [
        r"\bguarantee\b",
        r"\bguaranteed\b",
        r"100%\s+success",
        r"300%\s+growth",
        r"double\s+your\s+revenue",
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        text = f"{artifact.subject or ''} {artifact.content}".lower()
        for pat in self.PATTERNS:
            if re.search(pat, text):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message="Prohibited guarantee detected in message text.",
                    evidence_reference="Regex match on prohibited guarantee pattern",
                    remediation="Remove absolute guarantee statements or replace with probabilistic consultative language.",
                )
        return None


class FakeSocialProofRule(RiskRule):
    rule_id = "R-CLAIM-SOCIAL-PROOF"
    category = "DECEPTION"
    severity = "CRITICAL"
    description = "Flags fabricated client numbers, fake testimonials, or false client counts."

    PATTERNS = [
        r"worked\s+with\s+hundreds\s+of\s+businesses",
        r"thousands\s+of\s+satisfied\s+clients",
        r"everyone\s+in\s+your\s+area\s+is\s+using",
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        text = f"{artifact.subject or ''} {artifact.content}".lower()
        for pat in self.PATTERNS:
            if re.search(pat, text):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message="Unverified or fabricated social proof claim detected.",
                    evidence_reference="Regex match on exaggerated social proof statement",
                    remediation="Remove unverified client counts or replace with verified case study references.",
                )
        return None


class FalseUrgencyRule(RiskRule):
    rule_id = "R-CLAIM-FALSE-URGENCY"
    category = "DECEPTION"
    severity = "HIGH"
    description = "Flags artificial urgency tactics not backed by actual business constraints."

    PATTERNS = [
        r"only\s+two\s+slots\s+left",
        r"offer\s+expires\s+tonight",
        r"last\s+chance\s+to\s+claim",
        r"urgent:\s+action\s+required",
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        text = f"{artifact.subject or ''} {artifact.content}".lower()
        for pat in self.PATTERNS:
            if re.search(pat, text):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message="False urgency tactic detected.",
                    evidence_reference="Regex match on false urgency pattern",
                    remediation="Remove artificial expiration threats or slot limitations unless factually verified.",
                )
        return None


class DeceptiveIdentityRule(RiskRule):
    rule_id = "R-CLAIM-DECEPTIVE-IDENTITY"
    category = "DECEPTION"
    severity = "CRITICAL"
    description = "Flags impersonation, misleading authority claims, or deceptive identity phrasing."

    PATTERNS = [
        r"re:\s+your\s+recent\s+order",
        r"official\s+notice\s+from",
        r"security\s+alert\s+for\s+your\s+account",
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        subject = (artifact.subject or "").lower()
        for pat in self.PATTERNS:
            if re.search(pat, subject):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message="Deceptive subject line or identity impersonation pattern detected.",
                    evidence_reference="Regex match on deceptive identity subject line",
                    remediation="Use a clear, honest subject line reflecting your actual company and intent.",
                )
        return None
