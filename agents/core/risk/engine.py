"""Central orchestrator for the Risk & Quality Engine."""

import logging
from typing import Any, Dict, Optional
from agents.core.risk.claims import DeceptiveIdentityRule, FalseUrgencyRule, FakeSocialProofRule, GuaranteeClaimRule
from agents.core.risk.channels import ChannelRecipientFormatRule
from agents.core.risk.content import ContentQualityRule, ContentQualityValidator
from agents.core.risk.evaluator import SemanticRiskEvaluator
from agents.core.risk.evidence import EvidenceCoverageEvaluator, UnsupportedClaimRule
from agents.core.risk.injection import PromptInjectionRule
from agents.core.risk.models import RiskArtifact, RiskAssessmentResult
from agents.core.risk.policies import DEFAULT_RISK_POLICY, RiskPolicy
from agents.core.risk.privacy import InternalSystemInfoRule, SensitiveDataRule
from agents.core.risk.recipients import RecipientBusinessMismatchRule
from agents.core.risk.reconciler import RiskReconciler
from agents.core.risk.rules import RuleRegistry

logger = logging.getLogger(__name__)


class RiskEngine:
    """Central evaluation engine assessing safety, evidence support, and quality of artifacts."""

    def __init__(self, policy: Optional[RiskPolicy] = None):
        self.policy = policy or DEFAULT_RISK_POLICY
        self.registry = RuleRegistry()
        self._register_default_rules()

    def _register_default_rules(self) -> None:
        """Register default deterministic safety and quality rules."""
        self.registry.register(GuaranteeClaimRule())
        self.registry.register(FakeSocialProofRule())
        self.registry.register(FalseUrgencyRule())
        self.registry.register(DeceptiveIdentityRule())
        self.registry.register(UnsupportedClaimRule())
        self.registry.register(SensitiveDataRule())
        self.registry.register(InternalSystemInfoRule())
        self.registry.register(RecipientBusinessMismatchRule())
        self.registry.register(ChannelRecipientFormatRule())
        self.registry.register(PromptInjectionRule())
        self.registry.register(ContentQualityRule())

    async def assess(self, artifact: RiskArtifact, context: Optional[Dict[str, Any]] = None) -> RiskAssessmentResult:
        """
        Execute full evaluation pipeline:
        1. Calculate content hash
        2. Evaluate evidence coverage & claims
        3. Evaluate content quality
        4. Run deterministic rules engine
        5. Run optional AI semantic evaluation
        6. Reconcile findings to PASS / REVIEW / BLOCK
        """
        ctx = self.policy.to_context_dict()
        if context:
            ctx.update(context)

        content_hash = artifact.get_content_hash()

        # 1. Evidence Coverage Evaluation
        coverage_score, evidence_findings = EvidenceCoverageEvaluator.evaluate_coverage(artifact)

        # 2. Content Quality Evaluation
        quality_score, quality_checks, quality_findings = ContentQualityValidator.evaluate_quality(artifact)

        # 3. Deterministic Rules Evaluation
        deterministic_findings = self.registry.evaluate_all(artifact, ctx)
        all_deterministic_findings = evidence_findings + quality_findings + deterministic_findings

        # 4. Optional AI Semantic Review
        ai_risk_level, ai_findings = await SemanticRiskEvaluator.evaluate_semantic_risk(artifact, ctx)

        # 5. Reconcile Findings
        decision, risk_level = RiskReconciler.reconcile(
            all_deterministic_findings, ai_risk_level, ai_findings, self.policy
        )

        all_findings = all_deterministic_findings + ai_findings

        return RiskAssessmentResult(
            artifact_id=artifact.artifact_id,
            artifact_type=artifact.artifact_type,
            decision=decision,
            risk_level=risk_level,
            quality_score=quality_score,
            confidence="HIGH",
            evidence_coverage=coverage_score,
            engine_version=self.policy.engine_version,
            policy_version=self.policy.policy_version,
            content_hash=content_hash,
            artifact_version=artifact.version,
            findings=all_findings,
            quality_checks=quality_checks,
            is_stale=False,
            status="COMPLETED",
        )
