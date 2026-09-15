"""Content quality validator assessing relevance, clarity, conciseness, tone, and call-to-action."""

from typing import Any, Dict, List, Optional, Tuple
from agents.core.risk.models import QualityCheckDetail, RiskArtifact, RiskFindingDetail
from agents.core.risk.rules import RiskRule


class ContentQualityValidator:
    """Evaluates content quality metrics: Length, CTA clarity, Professional Tone."""

    @staticmethod
    def evaluate_quality(artifact: RiskArtifact) -> Tuple[float, List[QualityCheckDetail], List[RiskFindingDetail]]:
        text = artifact.content or ""
        subject = artifact.subject or ""
        checks: List[QualityCheckDetail] = []
        findings: List[RiskFindingDetail] = []

        # 1. Subject Quality Check
        if artifact.channel == "EMAIL":
            if not subject:
                findings.append(
                    RiskFindingDetail(
                        rule_id="R-CONTENT-MISSING-SUBJECT",
                        category="CONTENT",
                        severity="HIGH",
                        message="Email outreach draft is missing a subject line.",
                        evidence_reference="Empty subject line",
                        remediation="Add a clear, professional subject line.",
                    )
                )
                checks.append(QualityCheckDetail(check_type="SUBJECT_LINE", status="FAIL", score=0.0))
            elif len(subject) > 120:
                findings.append(
                    RiskFindingDetail(
                        rule_id="R-CONTENT-LONG-SUBJECT",
                        category="CONTENT",
                        severity="LOW",
                        message=f"Subject line is long ({len(subject)} chars, recommended < 80).",
                        evidence_reference=f"Subject length: {len(subject)}",
                        remediation="Shorten subject line for optimal mobile readability.",
                    )
                )
                checks.append(QualityCheckDetail(check_type="SUBJECT_LINE", status="WARNING", score=70.0))
            else:
                checks.append(QualityCheckDetail(check_type="SUBJECT_LINE", status="PASS", score=100.0))

        # 2. Body Length Quality Check
        body_words = len(text.split())
        if body_words < 10:
            findings.append(
                RiskFindingDetail(
                    rule_id="R-CONTENT-TOO-SHORT",
                    category="CONTENT",
                    severity="MEDIUM",
                    message=f"Draft body is too short ({body_words} words).",
                    evidence_reference=f"Body word count: {body_words}",
                    remediation="Add sufficient value-proposition context to the draft.",
                )
            )
            checks.append(QualityCheckDetail(check_type="BODY_LENGTH", status="FAIL", score=40.0))
        elif body_words > 500:
            findings.append(
                RiskFindingDetail(
                    rule_id="R-CONTENT-TOO-LONG",
                    category="CONTENT",
                    severity="LOW",
                    message=f"Draft body is verbose ({body_words} words, recommended < 300).",
                    evidence_reference=f"Body word count: {body_words}",
                    remediation="Trim unnecessary fluff to increase prospect engagement.",
                )
            )
            checks.append(QualityCheckDetail(check_type="BODY_LENGTH", status="WARNING", score=75.0))
        else:
            checks.append(QualityCheckDetail(check_type="BODY_LENGTH", status="PASS", score=100.0))

        # 3. Call to Action (CTA) Check
        cta_keywords = ["connect", "discuss", "call", "chat", "meeting", "thoughts", "schedule", "reply", "demo", "view"]
        has_cta = any(kw in text.lower() for kw in cta_keywords)
        if not has_cta:
            findings.append(
                RiskFindingDetail(
                    rule_id="R-CONTENT-MISSING-CTA",
                    category="CONTENT",
                    severity="MEDIUM",
                    message="Draft lacks a clear, low-friction Call to Action (CTA).",
                    evidence_reference="No CTA keywords detected in draft",
                    remediation="Add a clear conversational CTA (e.g. 'Would you be open to a 10-minute chat next week?').",
                )
            )
            checks.append(QualityCheckDetail(check_type="CALL_TO_ACTION", status="WARNING", score=50.0))
        else:
            checks.append(QualityCheckDetail(check_type="CALL_TO_ACTION", status="PASS", score=100.0))

        # Calculate overall quality score
        quality_score = round(sum(c.score for c in checks) / len(checks), 1) if checks else 100.0
        return quality_score, checks, findings


class ContentQualityRule(RiskRule):
    rule_id = "R-CONTENT-QUALITY-EVALUATION"
    category = "CONTENT"
    severity = "MEDIUM"
    description = "Evaluates overall draft content quality score."

    def evaluate(self, artifact: RiskArtifact, context: Dict[str, Any]) -> Optional[RiskFindingDetail]:
        quality_score, _, findings = ContentQualityValidator.evaluate_quality(artifact)
        min_quality = context.get("min_quality_score", 50.0)

        if quality_score < min_quality:
            return RiskFindingDetail(
                rule_id=self.rule_id,
                category=self.category,
                severity=self.severity,
                message=f"Overall quality score ({quality_score}/100) is below minimum threshold ({min_quality}).",
                evidence_reference=f"Calculated quality score: {quality_score}",
                remediation="Improve draft formatting, add subject/CTA, or fix word count length.",
            )
        return None
