"""
Product Roadmap Horizons, Scenarios, and FTE Capacity Planning Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.product_management.base import (
    RoadmapHorizon,
    RoadmapScenario,
)


class RoadmapCapacityManager:
    """Manages multi-horizon product roadmaps, scenario simulations, and team resource capacity."""

    def __init__(self):
        self._roadmaps: Dict[str, Dict[str, Any]] = {}
        self._roadmap_items: Dict[str, List[Dict[str, Any]]] = {}
        self._capacity_plans: Dict[str, List[Dict[str, Any]]] = {}

    # Roadmaps
    def create_roadmap(
        self,
        product_id: str,
        title: str,
        scenario_type: Any = RoadmapScenario.BASE_PLAN,
        confidence_level: float = 0.85,
        **kwargs,
    ) -> Dict[str, Any]:
        """Create a roadmap plan version."""
        rm_id = f"rm_{uuid.uuid4().hex[:12]}"
        scen = kwargs.get("scenario", scenario_type)
        scen_val = scen.value if hasattr(scen, "value") else str(scen)
        rm = {
            "id": rm_id,
            "product_id": product_id,
            "title": title,
            "scenario_type": scen_val,
            "scenario": scen_val,
            "description": kwargs.get("description", f"Roadmap for {title}"),
            "confidence_level": confidence_level,
            "version": 1,
            "items": [],
            "created_at": datetime.utcnow().isoformat(),
        }
        self._roadmaps[rm_id] = rm
        return rm

    def list_roadmaps(self, product_id: str) -> List[Dict[str, Any]]:
        rms = [r for r in self._roadmaps.values() if r.get("product_id") == product_id]
        for r in rms:
            r["items"] = self.list_roadmap_items(r["id"])
        return rms

    def add_roadmap_item(
        self,
        roadmap_id: str,
        title: str,
        horizon: Any = RoadmapHorizon.NOW,
        theme: Optional[str] = None,
        expected_outcome: Optional[str] = None,
        confidence: float = 0.80,
        dependencies: Optional[List[str]] = None,
        estimated_weeks: int = 4,
        **kwargs,
    ) -> Dict[str, Any]:
        """Add an initiative or deliverable to a roadmap horizon column."""
        item_id = f"rmi_{uuid.uuid4().hex[:12]}"
        h_val = horizon.value if hasattr(horizon, "value") else str(horizon)
        item = {
            "id": item_id,
            "roadmap_id": roadmap_id,
            "title": title,
            "horizon": h_val,
            "feature_id": kwargs.get("feature_id"),
            "objective_link": kwargs.get("objective_link"),
            "theme": theme or "Core Capability Expansion",
            "expected_outcome": expected_outcome or f"Deliver measurable uplift in {title}",
            "confidence": confidence,
            "dependencies": dependencies or [],
            "estimated_weeks": estimated_weeks,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._roadmap_items.setdefault(roadmap_id, []).append(item)
        return item

    def list_roadmap_items(self, roadmap_id: str) -> List[Dict[str, Any]]:
        return self._roadmap_items.get(roadmap_id, [])

    # Capacity Planning
    def set_capacity_plan(
        self,
        product_id: str,
        engineering_fte: float = 4.0,
        design_fte: float = 1.0,
        qa_fte: float = 1.0,
        ai_ml_fte: float = 1.0,
        devops_fte: float = 0.5,
        **kwargs,
    ) -> Dict[str, Any]:
        """Configure team FTE allocation and evaluate bottleneck risks."""
        tot_fte = engineering_fte + design_fte + qa_fte + ai_ml_fte + devops_fte

        # Heuristic bottleneck detection
        bottleneck = "NONE"
        if engineering_fte / max(qa_fte, 0.1) > 5.0:
            bottleneck = "QA_BOTTLENECK"
        elif engineering_fte / max(design_fte, 0.1) > 6.0:
            bottleneck = "DESIGN_BOTTLENECK"
        elif ai_ml_fte < 0.5:
            bottleneck = "AI_RESEARCH_BOTTLENECK"

        plan = {
            "id": f"cap_{uuid.uuid4().hex[:12]}",
            "product_id": product_id,
            "team_name": kwargs.get("team_name", "Core Product Squad"),
            "total_fte": round(tot_fte, 1),
            "engineering_fte": engineering_fte,
            "design_fte": design_fte,
            "qa_fte": qa_fte,
            "ai_ml_fte": ai_ml_fte,
            "devops_fte": devops_fte,
            "bottleneck_role": bottleneck,
            "utilization_rate": 0.84,
            "is_overallocated": False,
            "bottleneck_risk": "LOW" if bottleneck == "NONE" else "CRITICAL",
            "capacity_status": "BALANCED" if bottleneck == "NONE" else "CONSTRAINED",
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._capacity_plans.setdefault(product_id, []).append(plan)
        return plan

    def create_capacity_plan(
        self,
        product_id: str,
        team_name: str = "Core Engineering Squad",
        available_fte: float = 5.0,
        allocated_fte: float = 5.0,
        period: str = "Q3-2026",
    ) -> Dict[str, Any]:
        is_over = allocated_fte > available_fte
        plan = {
            "id": f"cap_{uuid.uuid4().hex[:12]}",
            "product_id": product_id,
            "team_name": team_name,
            "available_fte": available_fte,
            "allocated_fte": allocated_fte,
            "period": period,
            "is_overallocated": is_over,
            "bottleneck_risk": "CRITICAL" if is_over else "LOW",
            "utilization_rate": round(allocated_fte / max(available_fte, 0.1), 2),
            "created_at": datetime.utcnow().isoformat(),
        }
        self._capacity_plans.setdefault(product_id, []).append(plan)
        return plan

    def list_capacity_plans(self, product_id: str) -> List[Dict[str, Any]]:
        return self._capacity_plans.get(product_id, [])

    def get_capacity_plan(self, product_id: str) -> Optional[Dict[str, Any]]:
        plans = self._capacity_plans.get(product_id, [])
        return plans[-1] if plans else None
