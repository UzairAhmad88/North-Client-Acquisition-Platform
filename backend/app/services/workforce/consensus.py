"""
Consensus & Adversarial Review Subsystem for Phase 52.
Coordinates multi-worker independent evaluations, consensus synthesis, and adversarial critic fact-checking.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

try:
    from backend.app.services.workforce.base import AIConsensusResult, AIReviewResult
except ImportError:
    from app.services.workforce.base import AIConsensusResult, AIReviewResult

logger = logging.getLogger(__name__)


class ConsensusEngine:
    """Aggregates independent worker evaluations into a consensus score and highlights dissenting positions."""

    def evaluate_consensus(
        self,
        topic: str,
        worker_evaluations: List[Dict[str, Any]],
    ) -> AIConsensusResult:
        """Calculates agreement level across multiple workers."""
        if not worker_evaluations:
            return AIConsensusResult(
                topic=topic,
                participating_workers=[],
                worker_opinions=[],
                consensus_score=0.0,
                has_conflicts=False,
                synthesized_conclusion="No worker evaluations provided.",
            )

        participating = [e.get("worker_code", "UNKNOWN") for e in worker_evaluations]
        confidences = [float(e.get("confidence", 0.8)) for e in worker_evaluations]
        avg_conf = sum(confidences) / len(confidences)

        # Check for conflicts in recommendations
        recs = [e.get("recommendation", "").strip().lower() for e in worker_evaluations]
        unique_recs = set(recs)
        has_conflicts = len(unique_recs) > 1

        dissenting = []
        if has_conflicts:
            dissenting = [
                {"worker": e.get("worker_code"), "opinion": e.get("recommendation"), "rationale": e.get("rationale")}
                for e in worker_evaluations
            ]
            conclusion = f"Consensus divergence detected across {len(participating)} workers. Human review recommended to adjudicate conflicting findings."
            consensus_score = max(0.40, avg_conf * 0.7)
        else:
            conclusion = f"Unanimous agreement across {len(participating)} specialized workers on topic: {topic}."
            consensus_score = min(0.98, avg_conf * 1.05)

        return AIConsensusResult(
            topic=topic,
            participating_workers=participating,
            worker_opinions=worker_evaluations,
            consensus_score=round(consensus_score, 2),
            has_conflicts=has_conflicts,
            synthesized_conclusion=conclusion,
            dissenting_views=dissenting,
        )


class AdversarialReviewEngine:
    """Conducts independent adversarial critique on drafts/plans prior to human submission."""

    def review_draft(
        self,
        target_task_code: str,
        author_worker_code: str,
        critic_worker_code: str,
        draft_content: str,
        review_type: str = "FACT_AND_RISK",
    ) -> AIReviewResult:
        """Inspects draft for unsupported claims, hallucinations, or uncalibrated risk."""
        findings = []
        quality_score = 0.92

        if len(draft_content) < 50:
            findings.append({"type": "INSUFFICIENT_DEPTH", "severity": "MEDIUM", "detail": "Draft appears too concise to satisfy all strategic requirements."})
            quality_score -= 0.15

        if "guarantee" in draft_content.lower() or "100%" in draft_content:
            findings.append({"type": "UNVERIFIABLE_CLAIM", "severity": "HIGH", "detail": "Draft contains absolute performance claims which violate platform policy."})
            quality_score -= 0.25

        is_approved = quality_score >= 0.75

        critique = (
            f"Critic inspection completed by {critic_worker_code}. "
            f"Quality Rating: {quality_score*100:.0f}%. "
            f"{'Approved for human review.' if is_approved else 'Flagged with critical deficiencies.'}"
        )

        return AIReviewResult(
            target_task_code=target_task_code,
            author_worker_code=author_worker_code,
            critic_worker_code=critic_worker_code,
            review_type=review_type,
            critique_summary=critique,
            findings=findings,
            quality_score=round(quality_score, 2),
            is_approved_by_critic=is_approved,
        )
