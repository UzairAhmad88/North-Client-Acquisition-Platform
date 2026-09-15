"""
Product Backlog and Deterministic Multi-Framework Prioritization Engine.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.product_management.base import (
    BacklogItemType,
    PrioritizationFramework,
)


class BacklogPrioritizationManager:
    """Manages product backlog items, epics, stories, and transparent multi-framework prioritization."""

    def __init__(self):
        self._epics: Dict[str, List[Dict[str, Any]]] = {}
        self._features: Dict[str, List[Dict[str, Any]]] = {}
        self._backlog_items: Dict[str, List[Dict[str, Any]]] = {}
        self._scores: Dict[str, Dict[str, Any]] = {}

    # Epics & Features
    def create_epic(
        self,
        product_id: str,
        title: str,
        objective: str,
        business_value_score: float = 8.0,
        **kwargs,
    ) -> Dict[str, Any]:
        epic_id = f"epic_{uuid.uuid4().hex[:12]}"
        epic = {
            "id": epic_id,
            "product_id": product_id,
            "title": title,
            "objective": objective,
            "problem_statement": kwargs.get("problem_statement"),
            "business_value_score": business_value_score,
            "status": "PLANNED",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._epics.setdefault(product_id, []).append(epic)
        return epic

    def list_epics(self, product_id: str) -> List[Dict[str, Any]]:
        return self._epics.get(product_id, [])

    def create_feature(
        self,
        product_id: str,
        title: str,
        description: Optional[str] = None,
        epic_id: Optional[str] = None,
        user_story: Optional[str] = None,
        effort_points: int = 5,
        priority: str = "HIGH",
        **kwargs,
    ) -> Dict[str, Any]:
        feat_id = f"feat_{uuid.uuid4().hex[:12]}"
        feat = {
            "id": feat_id,
            "product_id": product_id,
            "epic_id": epic_id or kwargs.get("epic_id"),
            "requirement_id": kwargs.get("requirement_id"),
            "title": title,
            "description": description or f"Feature specification for {title}",
            "user_story": user_story or f"As a user, I want {title} so that I achieve higher efficiency.",
            "acceptance_criteria": kwargs.get("acceptance_criteria", ["Functional and non-functional tests pass"]),
            "effort_points": effort_points,
            "priority": priority,
            "status": "READY",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._features.setdefault(product_id, []).append(feat)
        return feat

    def list_features(self, product_id: str) -> List[Dict[str, Any]]:
        return self._features.get(product_id, [])

    # Backlog Items
    def create_backlog_item(
        self,
        product_id: str,
        title: str,
        item_type: Any = BacklogItemType.STORY,
        description: Optional[str] = None,
        priority: str = "MEDIUM",
        business_value: float = 7.0,
        customer_value: float = 7.0,
        effort_estimate: float = 3.0,
        risk_score: float = 2.0,
        assigned_sprint_id: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Record unified backlog item (Story, Bug, Task, Spike, Technical Debt)."""
        b_id = f"item_{uuid.uuid4().hex[:12]}"
        itype = item_type.value if hasattr(item_type, "value") else str(item_type)
        pts = kwargs.get("story_points", int(effort_estimate))
        item = {
            "id": b_id,
            "product_id": product_id,
            "epic_id": kwargs.get("epic_id"),
            "feature_id": kwargs.get("feature_id"),
            "requirement_id": kwargs.get("requirement_id"),
            "title": title,
            "item_type": itype,
            "type": itype,
            "description": description or title,
            "priority": priority,
            "business_value": business_value,
            "customer_value": customer_value,
            "effort_estimate": max(0.5, effort_estimate),
            "story_points": pts,
            "risk_score": risk_score,
            "assigned_sprint_id": assigned_sprint_id,
            "status": "BACKLOG",
            "prioritization_score": 150.0,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._backlog_items.setdefault(product_id, []).append(item)
        return item

    def list_backlog_items(
        self,
        product_id: str,
        item_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        items = self._backlog_items.get(product_id, [])
        if item_type:
            items = [i for i in items if i["item_type"] == item_type or i["type"] == item_type]
        if status:
            items = [i for i in items if i["status"] == status]
        return items

    # Prioritization Engines
    def score_rice(
        self,
        reach: float,  # number of users/events per time window
        impact: float,  # 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal
        confidence: float,  # 1.0=high, 0.8=medium, 0.5=low
        effort: float,  # person-months or sprint points
    ) -> Dict[str, Any]:
        """RICE Score = (Reach * Impact * Confidence) / Effort."""
        eff = max(0.5, effort)
        score = (reach * impact * confidence) / eff
        return {
            "framework": "RICE",
            "score": round(score, 2),
            "formula_breakdown": {
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": eff,
                "formula": f"({reach} * {impact} * {confidence}) / {eff}",
            },
            "calculation_breakdown": {
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": eff,
                "formula": f"({reach} * {impact} * {confidence}) / {eff}",
            },
        }

    def score_wsjf(
        self,
        user_business_value: float,
        time_criticality: float,
        risk_reduction_opportunity: float,
        job_size_effort: float,
    ) -> Dict[str, Any]:
        """WSJF = Cost of Delay / Job Size = (UserVal + TimeCrit + RiskRed) / JobSize."""
        cost_of_delay = user_business_value + time_criticality + risk_reduction_opportunity
        js = max(0.5, job_size_effort)
        score = cost_of_delay / js
        return {
            "framework": "WSJF",
            "score": round(score, 2),
            "formula_breakdown": {
                "user_business_value": user_business_value,
                "time_criticality": time_criticality,
                "risk_reduction_opportunity": risk_reduction_opportunity,
                "cost_of_delay": cost_of_delay,
                "job_size": js,
                "formula": f"({user_business_value} + {time_criticality} + {risk_reduction_opportunity}) / {js}",
            },
            "calculation_breakdown": {
                "user_business_value": user_business_value,
                "time_criticality": time_criticality,
                "risk_reduction_opportunity": risk_reduction_opportunity,
                "cost_of_delay": cost_of_delay,
                "job_size": js,
                "formula": f"({user_business_value} + {time_criticality} + {risk_reduction_opportunity}) / {js}",
            },
        }

    def score_value_vs_effort(
        self,
        customer_value: float,
        business_value: float,
        effort: float,
    ) -> Dict[str, Any]:
        """Value vs Effort Score = (Customer Value + Business Value) / (2 * Effort)."""
        tot_value = customer_value + business_value
        eff = max(0.5, effort)
        score = tot_value / (2.0 * eff)
        return {
            "framework": "VALUE_VS_EFFORT",
            "score": round(score, 2),
            "formula_breakdown": {
                "customer_value": customer_value,
                "business_value": business_value,
                "total_value": tot_value,
                "effort": eff,
                "formula": f"({customer_value} + {business_value}) / (2 * {eff})",
            },
            "calculation_breakdown": {
                "customer_value": customer_value,
                "business_value": business_value,
                "total_value": tot_value,
                "effort": eff,
                "formula": f"({customer_value} + {business_value}) / (2 * {eff})",
            },
        }

    def score_item(
        self,
        item_id: str,
        product_id: str,
        framework: str,
        inputs: Dict[str, float],
    ) -> Dict[str, Any]:
        fw = framework.upper()
        if fw == "RICE":
            reach = inputs.get("reach", 100)
            impact = inputs.get("impact", 2.0)
            conf = inputs.get("confidence", 0.8)
            eff = inputs.get("effort", 2.0)
            res = self.score_rice(reach, impact, conf, eff)
        elif fw == "WSJF":
            ubv = inputs.get("user_business_value", 8)
            tc = inputs.get("time_criticality", 7)
            rr = inputs.get("risk_reduction", inputs.get("risk_reduction_opportunity", 5))
            js = inputs.get("job_size", inputs.get("job_size_effort", 3))
            res = self.score_wsjf(ubv, tc, rr, js)
        else:
            cv = inputs.get("customer_value", 7)
            bv = inputs.get("business_value", 7)
            eff = inputs.get("effort", 3)
            res = self.score_value_vs_effort(cv, bv, eff)

        res["item_id"] = item_id
        res["product_id"] = product_id

        # Update item prioritization score in backlog
        for item in self._backlog_items.get(product_id, []):
            if item["id"] == item_id:
                item["prioritization_score"] = res["score"]
                item["prioritization_framework"] = fw

        return res
