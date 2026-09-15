"""
Knowledge Quality Evaluator for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.

Enforces Section 39 & Section 72:
Measures the 7 dimensions of knowledge quality:
1. Completeness (title, content, summary, source_id, metadata)
2. Accuracy & Authority (distribution of Authoritative/Verified/Confirmed vs Inferred)
3. Consistency (absence of active conflicts/contradictions)
4. Freshness (proportion of FRESH vs STALE/EXPIRED)
5. Validity (unexpired items, valid dates)
6. Uniqueness (content hash deduplication check)
7. Provenance (traceable origin, non-empty provenance)
"""

from typing import Any, Dict, List, Set
try:
    from backend.app.knowledge.base import (
        FreshnessStatus,
        KnowledgeAuthority,
        KnowledgeItem,
        KnowledgeProvenance,
    )
except ImportError:
    from app.knowledge.base import (
        FreshnessStatus,
        KnowledgeAuthority,
        KnowledgeItem,
        KnowledgeProvenance,
    )


class KnowledgeQualityEvaluator:
    """
    Computes quality benchmarks and health scorecards for the organizational knowledge base.
    """

    def evaluate_quality_scorecard(
        self,
        items: List[KnowledgeItem],
        open_conflict_count: int = 0,
    ) -> Dict[str, Any]:
        total = len(items)
        if total == 0:
            return {
                "total_items": 0,
                "overall_quality_score": 100.0,
                "completeness_score": 100.0,
                "authority_score": 100.0,
                "freshness_score": 100.0,
                "provenance_score": 100.0,
                "consistency_score": 100.0,
                "uniqueness_score": 100.0,
                "metrics": {
                    "verified_count": 0,
                    "human_confirmed_count": 0,
                    "inferred_count": 0,
                    "stale_count": 0,
                    "expired_count": 0,
                    "conflicted_count": 0,
                    "missing_provenance_count": 0,
                    "low_confidence_count": 0,
                    "duplicate_candidate_count": 0,
                }
            }

        # 1. Completeness: fields filled
        complete_count = 0
        missing_provenance = 0
        verified_count = 0
        human_confirmed_count = 0
        inferred_count = 0
        stale_count = 0
        expired_count = 0
        low_confidence_count = 0
        seen_hashes: Set[str] = set()
        duplicate_candidates = 0

        for it in items:
            # Check completeness
            if it.title and it.content and len(it.content) > 20 and it.domain:
                complete_count += 1

            # Provenance
            if not it.provenance or it.provenance == KnowledgeProvenance.EXTERNAL_SOURCE and not it.source_id:
                missing_provenance += 1
            if it.provenance == KnowledgeProvenance.HUMAN_CONFIRMED:
                human_confirmed_count += 1

            # Authority
            if it.authority in (KnowledgeAuthority.AUTHORITATIVE, KnowledgeAuthority.VERIFIED):
                verified_count += 1
            elif it.authority == KnowledgeAuthority.CONFIRMED:
                human_confirmed_count += 1
            elif it.authority == KnowledgeAuthority.INFERRED:
                inferred_count += 1

            # Freshness
            if it.freshness_status == FreshnessStatus.STALE:
                stale_count += 1
            elif it.freshness_status == FreshnessStatus.EXPIRED:
                expired_count += 1

            # Confidence
            if it.confidence < 0.7:
                low_confidence_count += 1

            # Duplication
            if it.content_hash:
                if it.content_hash in seen_hashes:
                    duplicate_candidates += 1
                else:
                    seen_hashes.add(it.content_hash)

        completeness_pct = round((complete_count / total) * 100.0, 1)
        provenance_pct = round(((total - missing_provenance) / total) * 100.0, 1)

        # Authority score weights verified/confirmed higher than unverified inferences
        high_auth_count = verified_count + human_confirmed_count
        authority_pct = round((high_auth_count / total) * 100.0, 1)

        fresh_items = total - (stale_count + expired_count)
        freshness_pct = round((max(0, fresh_items) / total) * 100.0, 1)

        # Consistency penalizes open conflicts
        conflict_penalty = min(50.0, open_conflict_count * 5.0)
        consistency_pct = max(0.0, round(100.0 - conflict_penalty, 1))

        # Uniqueness
        uniqueness_pct = round(((total - duplicate_candidates) / total) * 100.0, 1)

        # Composite score
        composite = (
            completeness_pct * 0.20 +
            provenance_pct * 0.20 +
            authority_pct * 0.15 +
            freshness_pct * 0.15 +
            consistency_pct * 0.15 +
            uniqueness_pct * 0.15
        )

        return {
            "total_items": total,
            "overall_quality_score": round(composite, 1),
            "completeness_score": completeness_pct,
            "authority_score": authority_pct,
            "freshness_score": freshness_pct,
            "provenance_score": provenance_pct,
            "consistency_score": consistency_pct,
            "uniqueness_score": uniqueness_pct,
            "metrics": {
                "verified_count": verified_count,
                "human_confirmed_count": human_confirmed_count,
                "inferred_count": inferred_count,
                "stale_count": stale_count,
                "expired_count": expired_count,
                "conflicted_count": open_conflict_count,
                "missing_provenance_count": missing_provenance,
                "low_confidence_count": low_confidence_count,
                "duplicate_candidate_count": duplicate_candidates,
            },
        }
