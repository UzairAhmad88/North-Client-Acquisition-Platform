"""Phase 60: Product Prioritization (RICE/WSJF), Roadmap Horizons (Now/Next/Later), Dependencies, Scenarios."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import logging

try:
    from backend.app.services.product_os.base import (
        AttrDict,
        PrioritizationFramework,
        RoadmapHorizon,
        generate_product_id,
    )
except ImportError:
    from app.services.product_os.base import (
        AttrDict,
        PrioritizationFramework,
        RoadmapHorizon,
        generate_product_id,
    )

logger = logging.getLogger(__name__)


class PrioritizationRoadmapsService:
    """Manages multi-framework prioritization (RICE, WSJF), governance logs, roadmaps, and dependency trees."""

    def __init__(self, db_session: Optional[Any] = None):
        self.db_session = db_session
        self._scores: Dict[str, Dict[str, Any]] = {}
        self._roadmaps: Dict[str, Dict[str, Any]] = {}
        self._items: Dict[str, Dict[str, Any]] = {}
        self._overrides: List[Dict[str, Any]] = []

    def score_prioritization(
        self,
        tenant_id: str = "default_tenant",
        item_id: str = "item_001",
        framework: str = PrioritizationFramework.RICE.value,
        reach: float = 1000.0,
        impact: float = 3.0,
        confidence: float = 80.0,
        effort: float = 4.0,
        user_business_value: float = 8.0,
        time_criticality: float = 7.0,
        risk_reduction: float = 6.0,
        **kwargs,
    ) -> AttrDict:
        """Calculate score using RICE, WSJF, or Value vs Effort."""
        score_id = generate_product_id("score")
        now = datetime.now(timezone.utc).isoformat()

        if framework == PrioritizationFramework.RICE.value:
            # RICE = (Reach * Impact * Confidence%) / Effort
            score_val = (reach * impact * (confidence / 100.0)) / max(0.5, effort)
        elif framework == PrioritizationFramework.WSJF.value:
            # WSJF = (User/Business Value + Time Criticality + Risk Reduction) / Job Size (Effort)
            cost_of_delay = user_business_value + time_criticality + risk_reduction
            score_val = cost_of_delay / max(0.5, effort)
        else:
            # Value vs Effort
            score_val = (user_business_value * 2.0) / max(0.5, effort)

        score_val = round(score_val, 2)

        record = {
            "score_id": score_id,
            "id": score_id,
            "tenant_id": tenant_id,
            "item_id": item_id,
            "framework": framework,
            "score": score_val,
            "parameters": {
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": effort,
                "user_business_value": user_business_value,
                "time_criticality": time_criticality,
                "risk_reduction": risk_reduction,
            },
            "created_at": now,
        }
        self._scores[item_id] = record
        return AttrDict(record)

    def log_priority_override(
        self,
        tenant_id: str,
        item_id: str,
        old_priority: str,
        new_priority: str,
        reason: str,
        evidence: str,
        owner_email: str,
        approval_signature: str,
    ) -> AttrDict:
        """Enforce strict governance logging on manual roadmap priority adjustments."""
        override_id = generate_product_id("ovr")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "override_id": override_id,
            "id": override_id,
            "tenant_id": tenant_id,
            "item_id": item_id,
            "old_priority": old_priority,
            "new_priority": new_priority,
            "reason": reason,
            "evidence": evidence,
            "owner_email": owner_email,
            "approval_signature": approval_signature,
            "is_approved": bool(approval_signature),
            "timestamp": now,
        }
        self._overrides.append(record)
        return AttrDict(record)

    def create_roadmap(
        self,
        tenant_id: str = "default_tenant",
        product_id: str = "prod_001",
        title: str = "Quarterly Strategic Roadmap",
        horizon_type: str = "QUARTERLY",
        **kwargs,
    ) -> AttrDict:
        """Create structured product roadmap container."""
        rdm_id = generate_product_id("rdm")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "roadmap_id": rdm_id,
            "id": rdm_id,
            "tenant_id": tenant_id,
            "product_id": product_id,
            "title": title,
            "horizon_type": horizon_type,
            "created_at": now,
            "updated_at": now,
        }
        self._roadmaps[rdm_id] = record
        return AttrDict(record)

    def add_roadmap_item(
        self,
        tenant_id: str = "default_tenant",
        roadmap_id: str = "rdm_001",
        title: str = "New Initiative",
        horizon: str = RoadmapHorizon.NOW.value,
        opportunity_id: Optional[str] = None,
        target_quarter: Optional[str] = "2026-Q3",
        engineering_effort_weeks: float = 4.0,
        dependencies: Optional[List[str]] = None,
        confidence: float = 85.0,
        **kwargs,
    ) -> AttrDict:
        """Add initiative item to roadmap with horizon and dependency linkages."""
        item_id = generate_product_id("item")
        now = datetime.now(timezone.utc).isoformat()

        record = {
            "item_id": item_id,
            "id": item_id,
            "tenant_id": tenant_id,
            "roadmap_id": roadmap_id,
            "title": title,
            "horizon": horizon,
            "opportunity_id": opportunity_id,
            "target_quarter": target_quarter,
            "engineering_effort_weeks": engineering_effort_weeks,
            "dependencies": dependencies or [],
            "confidence": confidence,
            "status": "PLANNED",
            "created_at": now,
            "updated_at": now,
        }
        self._items[item_id] = record
        return AttrDict(record)

    def get_roadmap_board(self, tenant_id: str = "default_tenant") -> AttrDict:
        """Retrieve full Now/Next/Later and Quarterly board."""
        items = [i for i in self._items.values() if i.get("tenant_id") == tenant_id]

        now_items = [i for i in items if i.get("horizon") == RoadmapHorizon.NOW.value]
        next_items = [i for i in items if i.get("horizon") == RoadmapHorizon.NEXT.value]
        later_items = [i for i in items if i.get("horizon") == RoadmapHorizon.LATER.value]

        quarterly_map: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            q = item.get("target_quarter", "Unscheduled")
            quarterly_map.setdefault(q, []).append(item)

        board_record = {
            "tenant_id": tenant_id,
            "total_initiatives": len(items),
            "horizons": {
                "NOW": now_items,
                "NEXT": next_items,
                "LATER": later_items,
            },
            "quarterly_initiatives": quarterly_map,
        }
        return AttrDict(board_record)
