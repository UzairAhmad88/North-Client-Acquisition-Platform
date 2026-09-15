"""
Outcomes Tracking, Post-Decision Retrospective Review, Decision Quality Framework, and Decision Journal.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class OutcomeJournalManager:
    """Manages real outcome measurement, post-decision reviews, decision quality scorecards, and templates."""

    def __init__(self):
        self._outcomes: Dict[str, List[Dict[str, Any]]] = {}
        self._post_reviews: Dict[str, List[Dict[str, Any]]] = {}
        self._templates: Dict[str, Dict[str, Any]] = {}
        self._seed_default_templates()

    def _seed_default_templates(self):
        """Seed standard decision room templates."""
        templates = [
            {
                "id": "tmpl_hiring",
                "name": "Hiring & Headcount Decision",
                "decision_type": "HIRING",
                "description": "Evaluate capacity need, labor economics, and alternative contractor/AI workforce options.",
                "default_criteria": [
                    {"name": "Capacity Gap Filled", "weight": 1.5, "criterion_type": "BENEFIT"},
                    {"name": "Fully-Loaded Cost", "weight": 1.2, "criterion_type": "COST"},
                    {"name": "Ramp-Up Speed", "weight": 1.0, "criterion_type": "BENEFIT"},
                    {"name": "Long-Term Flexibility", "weight": 1.0, "criterion_type": "BENEFIT"},
                ],
                "default_specialists": ["OPERATIONS", "FINANCE", "STRATEGY"],
                "default_approval_steps": [
                    {"step_name": "FINANCIAL_REVIEW", "required_role": "CFO"},
                    {"step_name": "EXECUTIVE_APPROVAL", "required_role": "CEO"},
                ],
            },
            {
                "id": "tmpl_pricing",
                "name": "Pricing & Tier Structure Decision",
                "decision_type": "PRICING",
                "description": "Analyze market positioning, margin expansion, client retention risk, and competitive response.",
                "default_criteria": [
                    {"name": "Revenue Potential", "weight": 1.5, "criterion_type": "BENEFIT"},
                    {"name": "Client Churn Risk", "weight": 1.4, "criterion_type": "COST"},
                    {"name": "Implementation Complexity", "weight": 0.8, "criterion_type": "COST"},
                ],
                "default_specialists": ["FINANCE", "CUSTOMER_SUCCESS", "STRATEGY"],
                "default_approval_steps": [
                    {"step_name": "COMMERCIAL_REVIEW", "required_role": "HEAD_OF_SALES"},
                    {"step_name": "EXECUTIVE_APPROVAL", "required_role": "CEO"},
                ],
            },
            {
                "id": "tmpl_strategic_investment",
                "name": "Strategic Investment & Expansion",
                "decision_type": "STRATEGIC",
                "description": "Evaluate multi-year business expansion, tech migration, or major new service launches.",
                "default_criteria": [
                    {"name": "Strategic Alignment", "weight": 1.5, "criterion_type": "BENEFIT"},
                    {"name": "Expected ROI Multiple", "weight": 1.3, "criterion_type": "BENEFIT"},
                    {"name": "Downside Risk", "weight": 1.2, "criterion_type": "COST"},
                ],
                "default_specialists": ["STRATEGY", "FINANCE", "SECURITY", "OPERATIONS"],
                "default_approval_steps": [
                    {"step_name": "RISK_REVIEW", "required_role": "RISK_OFFICER"},
                    {"step_name": "SECURITY_REVIEW", "required_role": "SECURITY_LEAD"},
                    {"step_name": "BOARD_APPROVAL", "required_role": "CEO"},
                ],
            },
        ]
        for t in templates:
            self._templates[t["id"]] = t

    # Outcomes & Measurements
    def record_outcome(
        self,
        room_id: str,
        metric_name: str,
        expected_value: float,
        actual_value: float,
    ) -> Dict[str, Any]:
        """Record post-execution empirical metric measurement."""
        variance = 0.0
        if expected_value != 0:
            variance = round(((actual_value - expected_value) / expected_value) * 100, 2)

        outcome = {
            "id": f"outc_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "metric_name": metric_name,
            "expected_value": expected_value,
            "actual_value": actual_value,
            "variance_pct": variance,
            "measured_at": datetime.utcnow().isoformat(),
        }
        self._outcomes.setdefault(room_id, []).append(outcome)
        return outcome

    def list_outcomes(self, room_id: str) -> List[Dict[str, Any]]:
        return self._outcomes.get(room_id, [])

    # Post-Decision Retrospective & Decision Quality Framework
    def submit_post_review(
        self,
        room_id: str,
        reviewed_by: str,
        outcome_rating: str = "NEUTRAL",
        prediction_error: Optional[str] = None,
        assumption_error: Optional[str] = None,
        execution_error: Optional[str] = None,
        model_error: Optional[str] = None,
        lessons_learned: Optional[List[str]] = None,
        evidence_quality: float = 85.0,
        option_diversity: float = 80.0,
        risk_coverage: float = 85.0,
    ) -> Dict[str, Any]:
        """
        Record post-decision review and calculate rigorous Decision Quality Score.
        Note: Decision Quality ($Q$) is separated from outcome favorability.
        """
        # Weighted decision quality calculation
        decision_quality_score = round(
            0.35 * evidence_quality + 0.35 * risk_coverage + 0.30 * option_diversity, 2
        )

        review = {
            "id": f"prev_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "decision_quality_score": decision_quality_score,
            "outcome_rating": outcome_rating,
            "prediction_error": prediction_error,
            "assumption_error": assumption_error,
            "execution_error": execution_error,
            "model_error": model_error,
            "lessons_learned": lessons_learned or [],
            "feed_to_organizational_memory": True,
            "reviewed_by": reviewed_by,
            "reviewed_at": datetime.utcnow().isoformat(),
        }
        self._post_reviews.setdefault(room_id, []).append(review)
        return review

    def list_post_reviews(self, room_id: str) -> List[Dict[str, Any]]:
        return self._post_reviews.get(room_id, [])

    # Templates
    def list_templates(self) -> List[Dict[str, Any]]:
        return list(self._templates.values())

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        return self._templates.get(template_id)
