"""
Domain-Specific Intelligence Engines: Market, Competitive, Technology, AI Models, Security, and Regulatory.
"""

import uuid
from typing import Dict, Any, List, Optional


class DomainIntelligenceManager:
    """Manages specialized intelligence profiles across market, competitive, tech, AI, and regulatory vectors."""

    def __init__(self):
        self._competitors: Dict[str, Dict[str, Any]] = {}
        self._market_signals: List[Dict[str, Any]] = []
        self._trends: Dict[str, List[Dict[str, Any]]] = {}

    # Competitive Intelligence
    def upsert_competitor_profile(
        self,
        company_name: str,
        market_position: str = "CHALLENGER",
        products_offered: Optional[List[str]] = None,
        pricing_signals: Optional[Dict[str, Any]] = None,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        recent_changes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Record competitor profile built exclusively from legitimate public signals."""
        cid = company_name.lower().replace(" ", "_")
        profile = {
            "id": f"comp_{cid}",
            "company_name": company_name,
            "market_position": market_position,
            "products_offered": products_offered or [],
            "pricing_signals": pricing_signals or {"model": "Tiered SaaS", "range": "$49 - $299/mo"},
            "strengths": strengths or [],
            "weaknesses": weaknesses or [],
            "recent_changes": recent_changes or [],
        }
        self._competitors[cid] = profile
        return profile

    def list_competitors(self) -> List[Dict[str, Any]]:
        return list(self._competitors.values())

    def get_competitor(self, name: str) -> Optional[Dict[str, Any]]:
        cid = name.lower().replace(" ", "_")
        return self._competitors.get(cid)

    # Market Signals & Trends
    def record_market_signal(
        self,
        market_segment: str,
        signal_type: str,
        description: str,
        confidence: float = 0.85,
        source_reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Capture quantitative or qualitative market signal."""
        signal = {
            "id": f"sig_{uuid.uuid4().hex[:12]}",
            "market_segment": market_segment,
            "signal_type": signal_type,
            "description": description,
            "confidence": confidence,
            "source_reference": source_reference or "Industry Report Q3",
        }
        self._market_signals.append(signal)
        return signal

    def list_market_signals(self, market_segment: Optional[str] = None) -> List[Dict[str, Any]]:
        if market_segment:
            return [s for s in self._market_signals if s["market_segment"] == market_segment]
        return self._market_signals

    # Trends
    def record_trend(
        self,
        workspace_id: str,
        trend_name: str,
        trend_type: str = "EMERGING",
        momentum_score: float = 0.75,
        key_drivers: Optional[List[str]] = None,
        impact_assessment: Optional[str] = None,
    ) -> Dict[str, Any]:
        trend = {
            "id": f"trd_{uuid.uuid4().hex[:12]}",
            "workspace_id": workspace_id,
            "trend_name": trend_name,
            "trend_type": trend_type,
            "momentum_score": momentum_score,
            "key_drivers": key_drivers or [],
            "impact_assessment": impact_assessment or "Positive expansion opportunity.",
        }
        self._trends.setdefault(workspace_id, []).append(trend)
        return trend

    def list_trends(self, workspace_id: str) -> List[Dict[str, Any]]:
        return self._trends.get(workspace_id, [])
