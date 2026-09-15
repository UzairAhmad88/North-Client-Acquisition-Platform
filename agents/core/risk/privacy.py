"""Privacy and sensitive data leakage rule subsystem."""

import re
from typing import Any, Dict, List, Optional
from agents.core.risk.models import RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class SensitiveDataRule(RiskRule):
    rule_id = "R-PRIVACY-SENSITIVE-DATA"
    category = "PII"
    severity = "CRITICAL"
    description = "Detects accidental exposure of API keys, tokens, passwords, database URLs, or internal credentials."

    PATTERNS = [
        (r"\b(api[_-]?key|secret[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}['\"]?", "API Key"),
        (r"\b(bearer\s+[A-Za-z0-9_\-\.]{20,})", "Bearer Token"),
        (r"\b(password|passwd|pwd)\s*[:=]\s*['\"]?\S{6,}['\"]?", "Password"),
        (r"postgres://\S+:\S+@\S+", "Database Connection URI"),
        (r"mongodb(?:\+srv)?://\S+:\S+@\S+", "MongoDB Connection URI"),
        (r"aws[_-]secret[_-]access[_-]key\s*[:=]", "AWS Secret Key"),
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        text = f"{artifact.subject or ''} {artifact.content}"
        for pat, label in self.PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message=f"Critical sensitive data exposure detected: {label}.",
                    evidence_reference=f"Pattern match for sensitive credential ({label})",
                    remediation="Immediately remove all internal credentials, tokens, or system keys from draft body.",
                )
        return None


class InternalSystemInfoRule(RiskRule):
    rule_id = "R-PRIVACY-INTERNAL-INFO"
    category = "PRIVACY"
    severity = "HIGH"
    description = "Detects leakage of internal system stack traces, database IDs, or agent prompt structures in customer-facing text."

    PATTERNS = [
        r"Traceback\s+\(most\s+recent\s+call\s+last\)",
        r"<UNTRUSTED_EXTERNAL_DATA>",
        r"agent_run_id\s*[:=]",
        r"SELECT\s+.*\s+FROM\s+users",
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        text = f"{artifact.subject or ''} {artifact.content}"
        for pat in self.PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message="Internal system debugging information or agent markup leaked in draft.",
                    evidence_reference="Match on internal system artifact pattern",
                    remediation="Clean text of internal debug logs, raw SQL statements, or system prompt markup tags.",
                )
        return None
