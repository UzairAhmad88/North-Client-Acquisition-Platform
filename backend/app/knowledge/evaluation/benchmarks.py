"""
Retrieval and AI Grounding Evaluation Benchmark Suite for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.

Enforces Section 40, 41, 78 & 79:
Computes:
- Precision@K, Recall@K, MRR (Mean Reciprocal Rank)
- Grounding Rate, Citation Accuracy
- Security Metric: Unauthorized Retrieval Rate (Target: EXACTLY 0.0)
"""

from typing import Any, Dict, List, Optional
import math


class RetrievalEvaluator:
    """
    Evaluates enterprise search and context retrieval quality across benchmark queries.
    """

    def evaluate_retrieval_metrics(
        self,
        test_cases: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Each test_case should have:
        - query: str
        - expected_codes: List[str]
        - retrieved_codes: List[str]
        - unauthorized_retrieved_count: int (must be 0)
        - is_grounded: bool
        - citations_accurate: bool
        """
        if not test_cases:
            return {
                "total_cases": 0,
                "precision_at_k": 1.0,
                "recall_at_k": 1.0,
                "mrr": 1.0,
                "grounding_rate": 1.0,
                "citation_accuracy": 1.0,
                "unauthorized_retrieval_rate": 0.0,
            }

        precisions = []
        recalls = []
        reciprocal_ranks = []
        grounded_count = 0
        citation_accurate_count = 0
        total_unauthorized_leaks = 0

        for case in test_cases:
            expected = set(case.get("expected_codes", []))
            retrieved = case.get("retrieved_codes", [])
            unauthorized = case.get("unauthorized_retrieved_count", 0)
            total_unauthorized_leaks += unauthorized

            if case.get("is_grounded", True):
                grounded_count += 1
            if case.get("citations_accurate", True):
                citation_accurate_count += 1

            if not retrieved:
                precisions.append(0.0 if expected else 1.0)
                recalls.append(0.0 if expected else 1.0)
                reciprocal_ranks.append(0.0)
                continue

            # Precision@K
            true_positives = [code for code in retrieved if code in expected]
            p_k = len(true_positives) / len(retrieved)
            precisions.append(p_k)

            # Recall@K
            r_k = len(true_positives) / len(expected) if expected else 1.0
            recalls.append(r_k)

            # MRR
            rr = 0.0
            for rank_idx, code in enumerate(retrieved, start=1):
                if code in expected:
                    rr = 1.0 / rank_idx
                    break
            reciprocal_ranks.append(rr)

        total = len(test_cases)
        avg_precision = sum(precisions) / total
        avg_recall = sum(recalls) / total
        avg_mrr = sum(reciprocal_ranks) / total
        grounding_rate = grounded_count / total
        citation_accuracy = citation_accurate_count / total
        unauthorized_rate = total_unauthorized_leaks / total

        return {
            "total_cases": total,
            "precision_at_k": round(avg_precision, 3),
            "recall_at_k": round(avg_recall, 3),
            "mrr": round(avg_mrr, 3),
            "grounding_rate": round(grounding_rate, 3),
            "citation_accuracy": round(citation_accuracy, 3),
            "unauthorized_retrieval_rate": round(unauthorized_rate, 4),  # Must be 0.0
            "zero_leakage_verified": total_unauthorized_leaks == 0,
        }

    def evaluate_grounding_case(
        self,
        question: str,
        retrieved_evidence: List[str],
        ai_response_claims: List[str],
    ) -> Dict[str, Any]:
        """
        Validates whether AI response claims are supported by retrieved evidence text.
        Identifies:
        - supported_claims
        - unsupported_claims
        - grounding_status: 'SUPPORTED' | 'INSUFFICIENT_INFORMATION' | 'UNSUPPORTED'
        """
        if not retrieved_evidence:
            return {
                "question": question,
                "grounding_status": "INSUFFICIENT_INFORMATION",
                "supported_claims": [],
                "unsupported_claims": ai_response_claims,
                "grounding_ratio": 0.0,
            }

        evidence_blob = " ".join(retrieved_evidence).lower()
        supported = []
        unsupported = []

        for claim in ai_response_claims:
            # Check key claim words in evidence
            claim_words = [w for w in claim.lower().split() if len(w) > 3]
            match_count = sum(1 for w in claim_words if w in evidence_blob)
            if claim_words and (match_count / len(claim_words)) >= 0.5:
                supported.append(claim)
            else:
                unsupported.append(claim)

        ratio = len(supported) / max(1, len(ai_response_claims))
        status = "SUPPORTED" if ratio >= 0.8 else ("PARTIAL" if ratio > 0 else "UNSUPPORTED")

        return {
            "question": question,
            "grounding_status": status,
            "supported_claims": supported,
            "unsupported_claims": unsupported,
            "grounding_ratio": round(ratio, 2),
        }
