"""Multi-Dimensional AI Evaluation Engine & Automated Scoring Layer."""

from typing import Any, Dict, List, Optional
import json


class AIEvaluationEngine:
    """Evaluates agent outputs across structural validity, factual grounding, policy compliance, and task completion."""

    def evaluate_structural_quality(self, output_data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """Check for JSON schema validity and presence of required keys."""
        missing = [f for f in required_fields if f not in output_data or output_data[f] is None]
        score = 100.0 if not missing else max(0.0, 100.0 - (len(missing) / max(1, len(required_fields))) * 100.0)

        return {
            "dimension": "STRUCTURAL",
            "score": score,
            "passed": len(missing) == 0,
            "missing_fields": missing,
        }

    def evaluate_policy_compliance(self, text_content: str, prohibited_phrases: Optional[List[str]] = None) -> Dict[str, Any]:
        """Check for prohibited claims, false guarantees, and compliance violations."""
        forbidden = prohibited_phrases or [
            "guaranteed 100%",
            "risk-free return",
            "we guarantee success",
            "zero chance of failure",
        ]
        violations = [p for p in forbidden if p.lower() in text_content.lower()]
        score = 100.0 if not violations else 0.0

        return {
            "dimension": "POLICY",
            "score": score,
            "passed": len(violations) == 0,
            "violations": violations,
        }

    def evaluate_evidence_grounding(self, output_data: Dict[str, Any], evidence_context: Dict[str, Any]) -> Dict[str, Any]:
        """Verify that quantitative claims in output correspond to real evidence in context."""
        claims = output_data.get("claims") or output_data.get("key_drivers") or []
        grounded_count = 0

        for claim in claims:
            # Check if feature key exists in evidence context
            feature_key = claim.get("feature") or claim.get("key") or ""
            if feature_key in evidence_context:
                grounded_count += 1

        total_claims = max(1, len(claims))
        score = round((grounded_count / total_claims) * 100.0, 1) if claims else 100.0

        return {
            "dimension": "FACTUAL_GROUNDING",
            "score": score,
            "passed": score >= 75.0,
            "grounded_ratio": f"{grounded_count}/{len(claims)}",
        }

    def run_comprehensive_evaluation(
        self,
        output_data: Dict[str, Any],
        required_fields: List[str],
        evidence_context: Dict[str, Any],
        text_content: str = "",
    ) -> Dict[str, Any]:
        """Compute aggregate benchmark score across all evaluation dimensions."""
        struct_res = self.evaluate_structural_quality(output_data, required_fields)
        policy_res = self.evaluate_policy_compliance(text_content or json.dumps(output_data))
        fact_res = self.evaluate_evidence_grounding(output_data, evidence_context)

        # Weighted aggregate: 40% structural, 30% policy, 30% factual
        overall_score = round(
            (struct_res["score"] * 0.40) + (policy_res["score"] * 0.30) + (fact_res["score"] * 0.30),
            1,
        )

        all_passed = struct_res["passed"] and policy_res["passed"] and fact_res["passed"]

        return {
            "overall_score": overall_score,
            "passed": all_passed,
            "dimensions": {
                "structural": struct_res,
                "policy": policy_res,
                "factual": fact_res,
            },
        }
