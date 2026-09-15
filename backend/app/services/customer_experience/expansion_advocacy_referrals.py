"""Customer Retention, Expansion Opportunities, Advocacy, Referrals, Segments, and Personas."""
from typing import Any, Dict, List, Optional
from backend.app.services.customer_experience.base import (
    AttrDict,
    generate_cx_id,
    current_utc_time,
)


class ExpansionAdvocacyReferralsService:
    """Manages retention, expansion, advocacy records, referrals, customer segmentation, and personas."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_retentions: List[Dict[str, Any]] = []
        self._in_memory_expansions: List[Dict[str, Any]] = []
        self._in_memory_advocacy: List[Dict[str, Any]] = []
        self._in_memory_referrals: List[Dict[str, Any]] = []
        self._in_memory_segments: List[Dict[str, Any]] = []
        self._in_memory_personas: List[Dict[str, Any]] = []

    def create_retention_opportunity(
        self,
        customer_id: str,
        title: str,
        trigger_reason: str,
        proposed_action: str,
        impact_estimate: str = "high",
        effort_required: str = "medium",
    ) -> AttrDict:
        r_id = generate_cx_id("ret")
        now = current_utc_time().isoformat()
        opportunity = AttrDict({
            "id": r_id,
            "customer_id": customer_id,
            "title": title,
            "trigger_reason": trigger_reason,
            "proposed_action": proposed_action,
            "impact_estimate": impact_estimate.lower(),
            "effort_required": effort_required.lower(),
            "status": "open",
            "requires_governance_approval": True,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_retentions.append(opportunity)
        return opportunity

    def list_retention_opportunities(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [r for r in self._in_memory_retentions if r.get("customer_id") == customer_id]
        return list(self._in_memory_retentions)

    def create_expansion_opportunity(
        self,
        customer_id: str,
        title: str,
        expansion_type: str = "additional_capacity",
        description: Optional[str] = None,
        estimated_arr_value: float = 25000.0,
        evidence_signals: Optional[List[str]] = None,
        confidence: float = 0.85,
    ) -> AttrDict:
        exp_id = generate_cx_id("exp")
        now = current_utc_time().isoformat()
        expansion = AttrDict({
            "id": exp_id,
            "customer_id": customer_id,
            "expansion_type": expansion_type.lower(),
            "title": title,
            "description": description or f"Expansion opportunity: {title}",
            "estimated_arr_value": estimated_arr_value,
            "evidence_signals": evidence_signals or ["Approaching 90% seat threshold", "Active interest in Phase 50 Twin module"],
            "stage": "discovery",
            "confidence": confidence,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_expansions.append(expansion)
        return expansion

    def list_expansion_opportunities(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [e for e in self._in_memory_expansions if e.get("customer_id") == customer_id]
        return list(self._in_memory_expansions)

    def create_advocacy_record(
        self,
        customer_id: str,
        title: str,
        content: str,
        advocacy_type: str = "testimonial",
        permission_granted: bool = False,
    ) -> AttrDict:
        adv_id = generate_cx_id("adv")
        now = current_utc_time().isoformat()
        advocacy = AttrDict({
            "id": adv_id,
            "customer_id": customer_id,
            "advocacy_type": advocacy_type.lower(),
            "title": title,
            "content": content,
            "permission_granted": permission_granted,
            "publication_status": "approved" if permission_granted else "draft",
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_advocacy.append(advocacy)
        return advocacy

    def list_advocacy_records(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [a for a in self._in_memory_advocacy if a.get("customer_id") == customer_id]
        return list(self._in_memory_advocacy)

    def create_referral(
        self,
        referrer_customer_id: str,
        referred_company_name: str,
        referred_contact_email: Optional[str] = None,
        relationship_context: Optional[str] = None,
        conversion_value: float = 0.0,
    ) -> AttrDict:
        ref_id = generate_cx_id("ref")
        now = current_utc_time().isoformat()
        referral = AttrDict({
            "id": ref_id,
            "referrer_customer_id": referrer_customer_id,
            "referred_company_name": referred_company_name,
            "referred_contact_email": referred_contact_email,
            "relationship_context": relationship_context or "Industry peer referral",
            "status": "submitted",
            "conversion_value": conversion_value,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_referrals.append(referral)
        return referral

    def list_referrals(self, referrer_customer_id: Optional[str] = None) -> List[AttrDict]:
        if referrer_customer_id:
            return [r for r in self._in_memory_referrals if r.get("referrer_customer_id") == referrer_customer_id]
        return list(self._in_memory_referrals)

    def list_segments(self) -> List[AttrDict]:
        if not self._in_memory_segments:
            now = current_utc_time().isoformat()
            self._in_memory_segments = [
                AttrDict({
                    "id": generate_cx_id("seg"),
                    "name": "Enterprise High-Growth FinTech",
                    "description": "High-volume transactional systems with strict compliance needs.",
                    "criteria": {"arr_min": 100000, "industry": "FinTech"},
                    "member_count": 48,
                    "avg_health_score": 86.4,
                    "created_at": now,
                    "updated_at": now,
                }),
                AttrDict({
                    "id": generate_cx_id("seg"),
                    "name": "Mid-Market Autonomous Operations",
                    "description": "Companies leveraging automated workforce orchestration.",
                    "criteria": {"arr_min": 35000, "modules": ["workforce", "twin"]},
                    "member_count": 112,
                    "avg_health_score": 79.8,
                    "created_at": now,
                    "updated_at": now,
                }),
            ]
        return list(self._in_memory_segments)

    def list_personas(self) -> List[AttrDict]:
        if not self._in_memory_personas:
            now = current_utc_time().isoformat()
            self._in_memory_personas = [
                AttrDict({
                    "id": generate_cx_id("per"),
                    "persona_name": "VP of Engineering / Tech Leader",
                    "role_category": "Decision Maker",
                    "primary_goals": ["System reliability", "Speed of deployment", "Zero-defect delivery"],
                    "common_pain_points": ["Integration bottlenecks", "Complex permissions overhead"],
                    "preferred_channels": ["technical_review", "slack_connect", "portal"],
                    "evidence_count": 34,
                    "is_ai_hypothesis": False,
                    "created_at": now,
                    "updated_at": now,
                }),
                AttrDict({
                    "id": generate_cx_id("per"),
                    "persona_name": "Operations & Compliance Director",
                    "role_category": "Executive Governance",
                    "primary_goals": ["GRC audit readiness", "Deterministic evidence lineage"],
                    "common_pain_points": ["Manual audit prep", "Lack of real-time visibility"],
                    "preferred_channels": ["executive_briefing", "email", "portal"],
                    "evidence_count": 21,
                    "is_ai_hypothesis": True,
                    "created_at": now,
                    "updated_at": now,
                }),
            ]
        return list(self._in_memory_personas)
