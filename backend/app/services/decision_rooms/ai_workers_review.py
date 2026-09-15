"""
Specialist AI Analysis, Adversarial Review, Disagreement Classification, and Consensus Engine.
"""

import uuid
from typing import Dict, Any, List, Optional
from backend.app.services.decision_rooms.base import (
    SpecialistRole,
    DisagreementCategory,
)


class SpecialistReviewManager:
    """Manages specialist AI team contributions, adversarial reviews, disagreements, and consensus."""

    def __init__(self):
        self._analyses: Dict[str, List[Dict[str, Any]]] = {}
        self._reviews: Dict[str, List[Dict[str, Any]]] = {}
        self._disagreements: Dict[str, List[Dict[str, Any]]] = {}

    def submit_specialist_analysis(
        self,
        room_id: str,
        specialist_role: SpecialistRole,
        summary: str,
        recommendations: Optional[List[str]] = None,
        key_findings: Optional[List[str]] = None,
        confidence: float = 0.8,
        facts: Optional[List[str]] = None,
        inferences: Optional[List[str]] = None,
        worker_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record domain-specific specialist analysis."""
        analysis = {
            "id": f"anls_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "specialist_role": specialist_role.value if hasattr(specialist_role, "value") else str(specialist_role),
            "worker_id": worker_id or f"worker_{specialist_role.lower()}",
            "summary": summary,
            "recommendations": recommendations or [],
            "key_findings": key_findings or [],
            "confidence": max(0.0, min(1.0, confidence)),
            "facts": facts or [],
            "inferences": inferences or [],
        }
        self._analyses.setdefault(room_id, []).append(analysis)
        return analysis

    def list_analyses(self, room_id: str) -> List[Dict[str, Any]]:
        return self._analyses.get(room_id, [])

    def submit_adversarial_review(
        self,
        room_id: str,
        critique_summary: str,
        reviewer_role: str = "CRITICAL_ANALYST",
        target_option_id: Optional[str] = None,
        weak_assumptions: Optional[List[str]] = None,
        unintended_consequences: Optional[List[str]] = None,
        hidden_costs: Optional[List[str]] = None,
        data_gaps: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Record adversarial critique challenging proposal assumptions and risks."""
        review = {
            "id": f"rev_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "reviewer_role": reviewer_role,
            "target_option_id": target_option_id,
            "critique_summary": critique_summary,
            "weak_assumptions": weak_assumptions or [],
            "unintended_consequences": unintended_consequences or [],
            "hidden_costs": hidden_costs or [],
            "data_gaps": data_gaps or [],
        }
        self._reviews.setdefault(room_id, []).append(review)
        return review

    def list_reviews(self, room_id: str) -> List[Dict[str, Any]]:
        return self._reviews.get(room_id, [])

    def register_disagreement(
        self,
        room_id: str,
        topic: str,
        disagreement_category: DisagreementCategory,
        party_a: str,
        view_a: str,
        party_b: str,
        view_b: str,
    ) -> Dict[str, Any]:
        """Surface and classify an explicit disagreement between humans or AI specialists."""
        disagreement = {
            "id": f"disag_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "topic": topic,
            "disagreement_category": disagreement_category.value if hasattr(disagreement_category, "value") else str(disagreement_category),
            "party_a": party_a,
            "view_a": view_a,
            "party_b": party_b,
            "view_b": view_b,
            "status": "SURFACED",
            "resolution_notes": None,
        }
        self._disagreements.setdefault(room_id, []).append(disagreement)
        return disagreement

    def list_disagreements(self, room_id: str) -> List[Dict[str, Any]]:
        return self._disagreements.get(room_id, [])

    def compute_consensus_metrics(self, room_id: str) -> Dict[str, Any]:
        """Compute consensus vs disagreement breakdown without claiming truth."""
        analyses = self.list_analyses(room_id)
        disagreements = self.list_disagreements(room_id)

        total_perspectives = max(1, len(analyses))
        unresolved_disagreements = len([d for d in disagreements if d["status"] != "RESOLVED"])

        # Disagreement ratio
        disagreement_pct = round(min(1.0, unresolved_disagreements / total_perspectives) * 100, 1)
        consensus_pct = round(100.0 - disagreement_pct, 1)

        primary_disagreement = disagreements[0]["topic"] if disagreements else "None"

        return {
            "room_id": room_id,
            "consensus_pct": consensus_pct,
            "disagreement_pct": disagreement_pct,
            "total_specialist_analyses": len(analyses),
            "total_disagreements": len(disagreements),
            "unresolved_disagreements": unresolved_disagreements,
            "primary_disagreement": primary_disagreement,
        }
