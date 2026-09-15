"""
Phase 59: Audiences, Explainable Segmentation, Personas, Positioning Engine, and Message Houses
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.services.marketing.base import AttrDict, generate_id


class AudiencePositioningService:
    """Manages marketing audiences, explainable segments, persona mapping, positioning, and message houses."""

    def __init__(self):
        self._audiences: Dict[str, AttrDict] = {}
        self._segments: Dict[str, AttrDict] = {}
        self._personas: Dict[str, AttrDict] = {}
        self._positionings: Dict[str, AttrDict] = {}
        self._message_houses: Dict[str, AttrDict] = {}

    def create_audience(
        self,
        name: str,
        description: str,
        target_icp: str,
        industry: str,
        company_size_tier: str,
        buying_context: str,
        primary_pain_points: List[str],
        channel_preferences: List[str],
        total_market_size: int = 10000,
        reachable_market_size: int = 2500,
    ) -> AttrDict:
        audience_id = generate_id("aud")
        audience = AttrDict({
            "id": audience_id,
            "name": name,
            "description": description,
            "target_icp": target_icp,
            "industry": industry,
            "company_size_tier": company_size_tier,
            "buying_context": buying_context,
            "primary_pain_points": primary_pain_points,
            "channel_preferences": channel_preferences,
            "total_market_size": total_market_size,
            "reachable_market_size": reachable_market_size,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._audiences[audience_id] = audience
        return audience

    def get_audience(self, audience_id: str) -> Optional[AttrDict]:
        return self._audiences.get(audience_id)

    def list_audiences(self) -> List[AttrDict]:
        return list(self._audiences.values())

    def create_segment(
        self,
        audience_id: str,
        name: str,
        segment_type: str = "BEHAVIORAL",
        criteria: Optional[Dict[str, Any]] = None,
        account_count: int = 250,
        avg_revenue_potential_usd: float = 75000.0,
    ) -> AttrDict:
        segment_id = generate_id("seg")
        segment = AttrDict({
            "id": segment_id,
            "audience_id": audience_id,
            "name": name,
            "segment_type": segment_type,
            "criteria": criteria or {"min_employees": 50, "high_intent_signals": True},
            "account_count": account_count,
            "avg_revenue_potential_usd": avg_revenue_potential_usd,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._segments[segment_id] = segment
        return segment

    def list_segments(self, audience_id: Optional[str] = None) -> List[AttrDict]:
        if audience_id:
            return [s for s in self._segments.values() if s.audience_id == audience_id]
        return list(self._segments.values())

    def create_persona(
        self,
        audience_id: str,
        title: str,
        role_type: str = "DECISION_MAKER",
        assumption_status: str = "OBSERVED",
        core_responsibilities: Optional[List[str]] = None,
        top_priorities: Optional[List[str]] = None,
        key_objections: Optional[List[str]] = None,
        preferred_content_formats: Optional[List[str]] = None,
    ) -> AttrDict:
        persona_id = generate_id("per")
        persona = AttrDict({
            "id": persona_id,
            "audience_id": audience_id,
            "title": title,
            "role_type": role_type,
            "assumption_status": assumption_status,
            "core_responsibilities": core_responsibilities or ["Revenue Growth", "Tech Stack Strategy"],
            "top_priorities": top_priorities or ["Automation ROI", "Time-to-Value"],
            "key_objections": key_objections or ["Implementation Complexity", "Budget Alignment"],
            "preferred_content_formats": preferred_content_formats or ["CASE_STUDY", "WHITEPAPER", "EXECUTIVE_BRIEF"],
            "created_at": datetime.utcnow().isoformat(),
        })
        self._personas[persona_id] = persona
        return persona

    def list_personas(self, audience_id: Optional[str] = None) -> List[AttrDict]:
        if audience_id:
            return [p for p in self._personas.values() if p.audience_id == audience_id]
        return list(self._personas.values())

    def create_positioning(
        self,
        audience_id: str,
        target_customer: str,
        problem_statement: str,
        alternative_solution: str,
        our_solution: str,
        key_differentiators: List[str],
        value_statement: str,
        proof_points: List[str],
    ) -> AttrDict:
        pos_id = generate_id("pos")
        pos = AttrDict({
            "id": pos_id,
            "audience_id": audience_id,
            "target_customer": target_customer,
            "problem_statement": problem_statement,
            "alternative_solution": alternative_solution,
            "our_solution": our_solution,
            "key_differentiators": key_differentiators,
            "value_statement": value_statement,
            "proof_points": proof_points,
            "version": 1,
            "is_approved": False,
            "approved_by": None,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._positionings[pos_id] = pos
        return pos

    def approve_positioning(self, positioning_id: str, approver: str) -> AttrDict:
        pos = self._positionings.get(positioning_id)
        if not pos:
            raise ValueError(f"Positioning {positioning_id} not found")
        pos.is_approved = True
        pos.approved_by = approver
        return pos

    def get_positioning(self, positioning_id: str) -> Optional[AttrDict]:
        return self._positionings.get(positioning_id)

    def list_positionings(self, audience_id: Optional[str] = None) -> List[AttrDict]:
        if audience_id:
            return [p for p in self._positionings.values() if p.audience_id == audience_id]
        return list(self._positionings.values())

    def create_message_house(
        self,
        positioning_id: str,
        core_message: str,
        pillar_1: Dict[str, Any],
        pillar_2: Dict[str, Any],
        pillar_3: Dict[str, Any],
        call_to_action: str,
        forbidden_terms: Optional[List[str]] = None,
        preferred_terms: Optional[List[str]] = None,
    ) -> AttrDict:
        mh_id = generate_id("mh")
        mh = AttrDict({
            "id": mh_id,
            "positioning_id": positioning_id,
            "core_message": core_message,
            "pillar_1": pillar_1,
            "pillar_2": pillar_2,
            "pillar_3": pillar_3,
            "call_to_action": call_to_action,
            "forbidden_terms": forbidden_terms or ["guarantee 100% win", "no-risk magic bullet"],
            "preferred_terms": preferred_terms or ["evidence-grounded", "closed-loop growth", "governed execution"],
            "created_at": datetime.utcnow().isoformat(),
        })
        self._message_houses[mh_id] = mh
        return mh

    def get_message_house(self, mh_id: str) -> Optional[AttrDict]:
        return self._message_houses.get(mh_id)

    def list_message_houses(self) -> List[AttrDict]:
        return list(self._message_houses.values())
