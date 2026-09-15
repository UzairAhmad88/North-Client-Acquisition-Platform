"""Evidence validation subsystem evaluating claim-to-evidence traceability and evidence coverage."""

from typing import Any, Dict, List, Optional, Tuple
from agents.core.risk.models import RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class EvidenceCoverageEvaluator:
    """Evaluates evidence coverage score and claim status classification."""

    @staticmethod
    def evaluate_coverage(artifact: RiskArtifact) -> Tuple[float, List[RiskFindingDetail]]:
        claims = artifact.claims or []
        evidence = artifact.evidence or []
        findings: List[RiskFindingDetail] = []

        if not claims:
            return 1.0, []

        supported_count = 0
        total_claims = len(claims)

        for claim in claims:
            statement = claim.get("statement") or claim.get("claim") or str(claim)
            status = claim.get("status", "UNSUPPORTED").upper()

            # Check if any evidence explicitly links to this claim or if claim status is VERIFIED/INFERRED
            linked_evidence = [
                e for e in evidence if e.get("claim_id") == claim.get("id") or e.get("field") in statement.lower()
            ]

            if linked_evidence or status in ("VERIFIED", "INFERRED"):
                supported_count += 1
            else:
                findings.append(
                    RiskFindingDetail(
                        rule_id="R-EVIDENCE-UNSUPPORTED-CLAIM",
                        category="EVIDENCE",
                        severity="MEDIUM",
                        message=f"Claim '{statement[:80]}...' has no supporting evidence in research or audit data.",
                        evidence_reference="Missing linked evidence record",
                        remediation="Link an audit finding or research record to support this claim, or remove the claim.",
                    )
                )

        coverage_score = round(supported_count / total_claims, 2) if total_claims > 0 else 1.0
        return coverage_score, findings


class UnsupportedClaimRule(RiskRule):
    rule_id = "R-EVIDENCE-COVERAGE-LOW"
    category = "EVIDENCE"
    severity = "HIGH"
    description = "Flags artifacts where evidence coverage falls below policy threshold (< 50%)."

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        coverage, _ = EvidenceCoverageEvaluator.evaluate_coverage(artifact)
        min_coverage = context.get("min_evidence_coverage", 0.5)

        if artifact.claims and coverage < min_coverage:
            return RiskFindingDetail(
                rule_id=self.rule_id,
                category=self.category,
                severity=self.severity,
                message=f"Evidence coverage ({int(coverage * 100)}%) is below required threshold ({int(min_coverage * 100)}%).",
                evidence_reference=f"Calculated evidence coverage: {coverage}",
                remediation="Ensure major factual statements are backed by audit findings or research evidence.",
            )
        return None
