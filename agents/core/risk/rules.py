"""Base rules registry and rule definition interfaces for Risk & Quality Engine."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from agents.core.risk.models import RiskArtifact, RiskFindingDetail


class RiskRule(ABC):
    """Abstract base class for all deterministic risk rules."""

    rule_id: str
    category: str
    severity: str
    enabled: bool = True
    description: str

    @abstractmethod
    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        """Evaluate artifact against rule. Return RiskFindingDetail if violated, else None."""
        pass


class RuleRegistry:
    """Registry maintaining active deterministic risk rules."""

    def __init__(self):
        self._rules: Dict[str, RiskRule] = {}

    def register(self, rule: RiskRule) -> None:
        self._rules[rule.rule_id] = rule

    def get_enabled_rules(self) -> List[RiskRule]:
        return [rule for rule in self._rules.values() if rule.enabled]

    def evaluate_all(self, artifact: RiskArtifact, context: Dict[str, Any]) -> List[RiskFindingDetail]:
        findings: List[RiskFindingDetail] = []
        for rule in self.get_enabled_rules():
            finding = rule.evaluate(artifact, context)
            if finding:
                findings.append(finding)
        return findings
