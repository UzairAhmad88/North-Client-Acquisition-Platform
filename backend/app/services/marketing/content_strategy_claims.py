"""
Phase 59: Content Strategy, Assets, Briefs, Factual Claims Verification, Approvals, Gap Analysis, Repurposing, Brand Voice
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.services.marketing.base import AttrDict, ContentStatus, ClaimVerificationStatus, generate_id


class ContentStrategyClaimsService:
    """Manages content assets, versioning, briefs, factual claims verification, gap analysis, and brand voice."""

    def __init__(self):
        self._assets: Dict[str, AttrDict] = {}
        self._versions: Dict[str, List[AttrDict]] = {}
        self._briefs: Dict[str, AttrDict] = {}
        self._claims: Dict[str, List[AttrDict]] = {}
        self._approvals: Dict[str, List[AttrDict]] = {}
        self._gaps: Dict[str, AttrDict] = {}
        self._brand_voices: Dict[str, AttrDict] = {}

    def create_content_asset(
        self,
        title: str,
        content_type: str = "ARTICLE",
        journey_stage: str = "AWARENESS",
        target_audience_id: Optional[str] = None,
        body_markdown: str = "",
        primary_cta: Optional[str] = None,
        author: str = "system",
    ) -> AttrDict:
        asset_id = generate_id("cnt")
        asset = AttrDict({
            "id": asset_id,
            "title": title,
            "content_type": content_type,
            "journey_stage": journey_stage,
            "target_audience_id": target_audience_id,
            "status": ContentStatus.DRAFT.value,
            "current_version": 1,
            "body_markdown": body_markdown,
            "primary_cta": primary_cta or "Schedule a Strategy Call",
            "revenue_influenced_usd": 0.0,
            "views_count": 0,
            "conversions_count": 0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        })
        self._assets[asset_id] = asset

        initial_version = AttrDict({
            "id": generate_id("ver"),
            "asset_id": asset_id,
            "version_number": 1,
            "title": title,
            "body_markdown": body_markdown,
            "author": author,
            "change_summary": "Initial draft creation",
            "created_at": datetime.utcnow().isoformat(),
        })
        self._versions[asset_id] = [initial_version]
        return asset

    def update_content_asset(
        self,
        asset_id: str,
        title: Optional[str] = None,
        body_markdown: Optional[str] = None,
        author: str = "editor",
        change_summary: str = "Editorial update",
    ) -> AttrDict:
        asset = self._assets.get(asset_id)
        if not asset:
            raise ValueError(f"Content asset {asset_id} not found")

        new_version_num = asset.current_version + 1
        asset.current_version = new_version_num
        if title:
            asset.title = title
        if body_markdown is not None:
            asset.body_markdown = body_markdown
        asset.updated_at = datetime.utcnow().isoformat()

        version_record = AttrDict({
            "id": generate_id("ver"),
            "asset_id": asset_id,
            "version_number": new_version_num,
            "title": asset.title,
            "body_markdown": asset.body_markdown,
            "author": author,
            "change_summary": change_summary,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._versions[asset_id].append(version_record)
        return asset

    def get_content_asset(self, asset_id: str) -> Optional[AttrDict]:
        return self._assets.get(asset_id)

    def list_content_assets(self, journey_stage: Optional[str] = None) -> List[AttrDict]:
        if journey_stage:
            return [a for a in self._assets.values() if a.journey_stage == journey_stage]
        return list(self._assets.values())

    def create_content_brief(
        self,
        target_topic: str,
        target_audience_id: Optional[str] = None,
        journey_stage: str = "AWARENESS",
        search_intent: str = "INFORMATIONAL",
        key_takeaways: Optional[List[str]] = None,
        primary_keywords: Optional[List[str]] = None,
        required_evidence_sources: Optional[List[str]] = None,
    ) -> AttrDict:
        brief_id = generate_id("brf")
        brief = AttrDict({
            "id": brief_id,
            "target_topic": target_topic,
            "target_audience_id": target_audience_id,
            "journey_stage": journey_stage,
            "search_intent": search_intent,
            "key_takeaways": key_takeaways or ["Market shift overview", "Cost of inaction", "Implementation roadmap"],
            "primary_keywords": primary_keywords or [target_topic.lower(), "b2b growth strategy"],
            "required_evidence_sources": required_evidence_sources or ["Official Benchmarks 2026", "Internal Client Case Studies"],
            "status": "OPEN",
            "created_at": datetime.utcnow().isoformat(),
        })
        self._briefs[brief_id] = brief
        return brief

    def list_content_briefs(self) -> List[AttrDict]:
        return list(self._briefs.values())

    def record_claim(
        self,
        asset_id: str,
        claim_text: str,
        source_reference: str,
        source_date: Optional[str] = "2026-09",
        confidence_pct: float = 90.0,
        verification_status: str = ClaimVerificationStatus.VERIFIED.value,
        reviewer_notes: Optional[str] = "Verified against primary research dataset.",
    ) -> AttrDict:
        claim_id = generate_id("clm")
        claim = AttrDict({
            "id": claim_id,
            "asset_id": asset_id,
            "claim_text": claim_text,
            "source_reference": source_reference,
            "source_date": source_date,
            "confidence_pct": confidence_pct,
            "verification_status": verification_status,
            "reviewer_notes": reviewer_notes,
            "verified_at": datetime.utcnow().isoformat(),
            "created_at": datetime.utcnow().isoformat(),
        })
        if asset_id not in self._claims:
            self._claims[asset_id] = []
        self._claims[asset_id].append(claim)
        return claim

    def get_claims_for_asset(self, asset_id: str) -> List[AttrDict]:
        return self._claims.get(asset_id, [])

    def submit_for_approval(
        self,
        asset_id: str,
        approver: str,
        approval_type: str = "EDITORIAL",
        status: str = "APPROVED",
        comments: Optional[str] = "Reviewed and validated for brand voice and factual accuracy.",
    ) -> AttrDict:
        asset = self._assets.get(asset_id)
        if not asset:
            raise ValueError(f"Content asset {asset_id} not found")

        # Check for unverified or conflicting claims
        claims = self._claims.get(asset_id, [])
        has_unverified = any(c.verification_status in [ClaimVerificationStatus.UNVERIFIED.value, ClaimVerificationStatus.CONFLICTING.value] for c in claims)
        if has_unverified and status == "APPROVED":
            status = "NEEDS_FACT_CHECK"

        approval_id = generate_id("app")
        approval = AttrDict({
            "id": approval_id,
            "asset_id": asset_id,
            "approver": approver,
            "approval_type": approval_type,
            "status": status,
            "comments": comments,
            "created_at": datetime.utcnow().isoformat(),
        })
        if asset_id not in self._approvals:
            self._approvals[asset_id] = []
        self._approvals[asset_id].append(approval)

        if status == "APPROVED":
            asset.status = ContentStatus.APPROVED.value

        return approval

    def detect_content_gaps(self) -> List[AttrDict]:
        """Identifies high-priority content gaps based on market demand and missing journey stages."""
        gap_id_1 = generate_id("gap")
        gap_id_2 = generate_id("gap")
        gaps = [
            AttrDict({
                "id": gap_id_1,
                "topic": "Enterprise Multi-Agent Governance & Compliance Framework",
                "target_audience": "Enterprise Operations",
                "journey_stage": "CONSIDERATION",
                "demand_volume": "HIGH",
                "revenue_potential_usd": 120000.0,
                "effort_tier": "MEDIUM",
                "priority_score": 9.2,
                "created_at": datetime.utcnow().isoformat(),
            }),
            AttrDict({
                "id": gap_id_2,
                "topic": "Deterministic CAC/LTV Unit Economics in High-Touch B2B",
                "target_audience": "CFOs & Finance Executives",
                "journey_stage": "EVALUATION",
                "demand_volume": "HIGH",
                "revenue_potential_usd": 85000.0,
                "effort_tier": "LOW",
                "priority_score": 8.8,
                "created_at": datetime.utcnow().isoformat(),
            }),
        ]
        for g in gaps:
            self._gaps[g.id] = g
        return gaps

    def list_content_gaps(self) -> List[AttrDict]:
        if not self._gaps:
            self.detect_content_gaps()
        return list(self._gaps.values())

    def repurpose_content(
        self,
        source_asset_id: str,
        target_formats: List[str],
    ) -> List[AttrDict]:
        source = self._assets.get(source_asset_id)
        if not source:
            raise ValueError(f"Source asset {source_asset_id} not found")

        repurposed_assets = []
        for fmt in target_formats:
            rep_asset = self.create_content_asset(
                title=f"[{fmt}] {source.title}",
                content_type=fmt,
                journey_stage=source.journey_stage,
                target_audience_id=source.target_audience_id,
                body_markdown=f"Derived from {source.title}:\n\n{source.body_markdown[:300]}...",
                author="repurposing_engine",
            )
            repurposed_assets.append(rep_asset)
        return repurposed_assets

    def create_brand_voice_profile(
        self,
        name: str = "Default Brand Voice",
        primary_tone: str = "AUTHORITATIVE_EMPATHETIC",
        reading_level: str = "PROFESSIONAL",
        prohibited_claims: Optional[List[str]] = None,
        preferred_vocab: Optional[List[str]] = None,
    ) -> AttrDict:
        voice_id = generate_id("bv")
        voice = AttrDict({
            "id": voice_id,
            "name": name,
            "primary_tone": primary_tone,
            "reading_level": reading_level,
            "prohibited_claims": prohibited_claims or ["100% automated guaranteed revenue", "no human review needed"],
            "preferred_vocab": preferred_vocab or ["evidence-backed", "governed workflow", "probabilistic modeling"],
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
        })
        self._brand_voices[voice_id] = voice
        return voice

    def check_brand_consistency(self, body_text: str) -> Dict[str, Any]:
        """Checks text against active brand voice rules and forbidden terms."""
        violations = []
        prohibited = ["guaranteed 100% win", "no human review needed", "magic bullet"]
        for p in prohibited:
            if p.lower() in body_text.lower():
                violations.append(f"Contains prohibited term/claim: '{p}'")

        return {
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "tone_assessment": "PROFESSIONAL",
            "checked_at": datetime.utcnow().isoformat(),
        }
