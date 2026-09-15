"""
Freshness and Expiration Monitor for Phase 48:
Unified Knowledge, Enterprise Search, Semantic Intelligence & Organizational Memory Platform.

Enforces Section 11 & 52:
Knowledge items age and may expire (FRESH -> AGING -> STALE -> EXPIRED).
Retrieval rankings apply freshness decay penalties to stale items.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple

try:
    from backend.app.knowledge.base import (
        FreshnessStatus,
        KnowledgeDomain,
        KnowledgeItem,
    )
except ImportError:
    from app.knowledge.base import (
        FreshnessStatus,
        KnowledgeDomain,
        KnowledgeItem,
    )


class FreshnessMonitor:
    """
    Monitors knowledge items against TTL and domain freshness policies.
    """

    # Default lifespan thresholds by domain (in days)
    DEFAULT_AGING_DAYS: Dict[KnowledgeDomain, int] = {
        KnowledgeDomain.SECURITY: 30,
        KnowledgeDomain.FINANCE: 45,
        KnowledgeDomain.PRICING if hasattr(KnowledgeDomain, "PRICING") else KnowledgeDomain.BUSINESS: 60,
        KnowledgeDomain.TECHNICAL: 90,
        KnowledgeDomain.COMPLIANCE: 90,
        KnowledgeDomain.POLICY: 180,
        KnowledgeDomain.GOVERNANCE: 180,
        KnowledgeDomain.REQUIREMENTS: 60,
        KnowledgeDomain.CRM: 90,
        KnowledgeDomain.ORGANIZATIONAL_MEMORY: 365,
    }

    DEFAULT_STALE_DAYS: Dict[KnowledgeDomain, int] = {
        KnowledgeDomain.SECURITY: 60,
        KnowledgeDomain.FINANCE: 90,
        KnowledgeDomain.PRICING if hasattr(KnowledgeDomain, "PRICING") else KnowledgeDomain.BUSINESS: 120,
        KnowledgeDomain.TECHNICAL: 180,
        KnowledgeDomain.COMPLIANCE: 180,
        KnowledgeDomain.POLICY: 365,
        KnowledgeDomain.GOVERNANCE: 365,
        KnowledgeDomain.REQUIREMENTS: 120,
        KnowledgeDomain.CRM: 180,
        KnowledgeDomain.ORGANIZATIONAL_MEMORY: 730,
    }

    def evaluate_freshness(
        self,
        item: KnowledgeItem,
        current_time: Optional[datetime] = None,
    ) -> Tuple[FreshnessStatus, float]:
        """
        Evaluates the current freshness status of an item and returns:
        (FreshnessStatus, FreshnessScoreMultiplier between 0.0 and 1.0)
        """
        now = current_time or datetime.now(timezone.utc)

        # 1. Check explicit expiration
        if item.valid_until and now > item.valid_until:
            return FreshnessStatus.EXPIRED, 0.2

        # 2. Check time since last update
        ref_time = item.updated_at or item.created_at
        age_days = (now - ref_time).total_seconds() / 86400.0

        aging_threshold = self.DEFAULT_AGING_DAYS.get(item.domain, 90)
        stale_threshold = self.DEFAULT_STALE_DAYS.get(item.domain, 180)

        if age_days <= aging_threshold:
            return FreshnessStatus.FRESH, 1.0
        elif age_days <= stale_threshold:
            # Linear decay from 1.0 down to 0.6
            progress = (age_days - aging_threshold) / max(1.0, (stale_threshold - aging_threshold))
            score = 1.0 - (0.4 * progress)
            return FreshnessStatus.AGING, round(score, 3)
        else:
            # Stale knowledge
            return FreshnessStatus.STALE, 0.4

    def update_item_freshness(
        self,
        item: KnowledgeItem,
        current_time: Optional[datetime] = None,
    ) -> KnowledgeItem:
        """
        Evaluates and updates the item's freshness_status in place.
        """
        status, _ = self.evaluate_freshness(item, current_time)
        item.freshness_status = status
        return item

    def filter_stale_items(
        self,
        items: List[KnowledgeItem],
        current_time: Optional[datetime] = None,
    ) -> List[KnowledgeItem]:
        """
        Returns all items that are either STALE or EXPIRED.
        """
        stale_list = []
        for it in items:
            status, _ = self.evaluate_freshness(it, current_time)
            if status in (FreshnessStatus.STALE, FreshnessStatus.EXPIRED):
                stale_list.append(it)
        return stale_list
