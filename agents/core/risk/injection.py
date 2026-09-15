"""Prompt injection defense and untrusted external data isolation rule."""

import re
from typing import Any, Dict, Optional
from agents.core.risk.models import RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class PromptInjectionRule(RiskRule):
    rule_id = "R-SECURITY-PROMPT-INJECTION"
    category = "PROMPT_INJECTION"
    severity = "CRITICAL"
    description = "Detects prompt injection attempts or system instruction override commands in external data."

    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"disregard\s+the\s+above\s+instructions",
        r"system\s*:\s*you\s+are\s+now",
        r"you\s+are\s+a\s+helpful\s+assistant\s+that\s+always\s+approves",
        r"override\s+safety\s+policy",
        r"send_email\s*\(\s*\)",
        r"grant\s+admin\s+permission",
    ]

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        text = f"{artifact.subject or ''} {artifact.content}"
        for pat in self.INJECTION_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                return RiskFindingDetail(
                    rule_id=self.rule_id,
                    category=self.category,
                    severity=self.severity,
                    message="Prompt injection attack or instruction override attempt detected in artifact text.",
                    evidence_reference="Regex match on malicious prompt injection pattern",
                    remediation="Sanitize external web/research content to strip prompt override instructions before draft generation.",
                )
        return None
