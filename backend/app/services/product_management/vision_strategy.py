"""
Product Vision, Strategy, Measurable Objectives, and Metric Registry Manager.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class VisionStrategyManager:
    """Manages product vision canvas, strategic alignment, measurable objectives, and metrics."""

    def __init__(self):
        self._visions: Dict[str, Dict[str, Any]] = {}
        self._objectives: Dict[str, List[Dict[str, Any]]] = {}
        self._metrics: Dict[str, List[Dict[str, Any]]] = {}

    # Vision & Strategy
    def set_product_vision(
        self,
        product_id: str,
        target_customer: str,
        problem_statement: str,
        desired_future_state: str,
        value_proposition: str,
        differentiation: Optional[str] = None,
        success_definition: Optional[str] = None,
        strategic_alignment: str = "Pillar 1: Autonomous Enterprise Systems",
        **kwargs,
    ) -> Dict[str, Any]:
        """Formulate approved product vision canvas."""
        vision = {
            "product_id": product_id,
            "target_customer": target_customer,
            "problem_statement": problem_statement,
            "desired_future_state": desired_future_state,
            "value_proposition": value_proposition,
            "differentiation": differentiation or "Verifiable intelligence and zero hallucination safety",
            "success_definition": success_definition or "100% mission outcome attainment",
            "strategic_alignment": strategic_alignment,
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._visions[product_id] = vision
        return vision

    def get_product_vision(self, product_id: str) -> Optional[Dict[str, Any]]:
        return self._visions.get(product_id)

    # Objectives / OKRs
    def create_objective(
        self,
        product_id: str,
        title: Optional[str] = None,
        metric_name: Optional[str] = None,
        baseline_value: float = 0.0,
        target_value: float = 0.0,
        current_value: float = 0.0,
        unit: str = "%",
        time_window: str = "Q3 2026",
        owner_id: str = "product_lead",
        confidence: float = 0.85,
        **kwargs,
    ) -> Dict[str, Any]:
        """Record measurable product objective or key result."""
        obj_id = f"obj_{uuid.uuid4().hex[:12]}"
        name_val = title or kwargs.get("name", "Strategic Objective")
        metric_val = metric_name or kwargs.get("metric", "conversion_rate")
        baseline_val = baseline_value or kwargs.get("baseline", 0.0)
        target_val = target_value or kwargs.get("target", 1.0)
        owner_val = owner_id or kwargs.get("owner", "Product Lead")
        conf_val = confidence if confidence != 0.85 else kwargs.get("confidence", 0.85)

        progress = 0.0
        if target_val != baseline_val:
            progress = max(0.0, min(1.0, (current_value - baseline_val) / (target_val - baseline_val)))

        status = "ON_TRACK" if progress >= 0.5 or current_value >= baseline_val else "AT_RISK"
        if progress >= 1.0 or current_value >= target_val:
            status = "ACHIEVED"

        obj = {
            "id": obj_id,
            "product_id": product_id,
            "title": name_val,
            "name": name_val,
            "metric_name": metric_val,
            "metric": metric_val,
            "baseline_value": baseline_val,
            "baseline": baseline_val,
            "target_value": target_val,
            "target": target_val,
            "current_value": current_value,
            "unit": unit,
            "progress_percentage": round(progress * 100, 1),
            "time_window": time_window,
            "owner_id": owner_val,
            "owner": owner_val,
            "confidence": conf_val,
            "status": status,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._objectives.setdefault(product_id, []).append(obj)
        return obj

    def list_objectives(self, product_id: str) -> List[Dict[str, Any]]:
        return self._objectives.get(product_id, [])

    # Metrics Registry
    def register_metric(
        self,
        product_id: str,
        name: str,
        category: str = "ENGAGEMENT",
        definition: Optional[str] = None,
        formula: Optional[str] = None,
        source: Optional[str] = None,
        current_value: float = 0.0,
        target_value: Optional[float] = None,
        unit: str = "count",
        time_window: str = "30d",
        **kwargs,
    ) -> Dict[str, Any]:
        """Register authoritative product metric definition and telemetry source."""
        met_id = f"met_{uuid.uuid4().hex[:12]}"
        is_ns = kwargs.get("is_north_star", False)
        metric = {
            "id": met_id,
            "product_id": product_id,
            "name": name,
            "category": category,
            "definition": definition or f"Metric definition for {name}",
            "formula": formula or "SUM(events) / COUNT(users)",
            "source": source or kwargs.get("source", "Product Telemetry / Postgres Events"),
            "owner": kwargs.get("owner", "Data Team"),
            "current_value": current_value or kwargs.get("current_value", 0.0),
            "target_value": target_value or kwargs.get("target_value"),
            "is_north_star": is_ns,
            "unit": unit,
            "time_window": time_window,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._metrics.setdefault(product_id, []).append(metric)
        return metric

    def list_metrics(self, product_id: str) -> List[Dict[str, Any]]:
        return self._metrics.get(product_id, [])
