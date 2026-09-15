"""
Scenario Simulation and Multi-Factor Risk Assessment Engine.
"""

import uuid
from typing import Dict, Any, List, Optional


class ScenarioRiskManager:
    """Manages scenarios, second-order effects, and multi-factor risk assessments."""

    def __init__(self):
        self._scenarios: Dict[str, List[Dict[str, Any]]] = {}
        self._risks: Dict[str, List[Dict[str, Any]]] = {}

    def create_scenario(
        self,
        room_id: str,
        name: str,
        scenario_type: str = "BASELINE",
        option_id: Optional[str] = None,
        assumptions_applied: Optional[Dict[str, Any]] = None,
        projected_metrics: Optional[Dict[str, Any]] = None,
        second_order_effects: Optional[List[str]] = None,
        confidence_interval: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a scenario simulation model linked to an option."""
        scenario = {
            "id": f"scen_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "option_id": option_id,
            "name": name,
            "scenario_type": scenario_type,
            "assumptions_applied": assumptions_applied or {},
            "projected_metrics": projected_metrics or {},
            "second_order_effects": second_order_effects or [],
            "confidence_interval": confidence_interval or {"p10": 0.8, "p50": 1.0, "p90": 1.25},
        }
        self._scenarios.setdefault(room_id, []).append(scenario)
        return scenario

    def list_scenarios(self, room_id: str) -> List[Dict[str, Any]]:
        return self._scenarios.get(room_id, [])

    def add_risk(
        self,
        room_id: str,
        risk_category: str,
        description: str,
        probability: float = 0.3,
        impact: float = 0.5,
        mitigation: Optional[str] = None,
        blast_radius: str = "TEAM",
        option_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record a risk item with probability and impact scores."""
        clamped_p = max(0.0, min(1.0, probability))
        clamped_i = max(0.0, min(1.0, impact))
        risk_score = round(clamped_p * clamped_i, 3)

        risk = {
            "id": f"rsk_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "option_id": option_id,
            "risk_category": risk_category,
            "description": description,
            "probability": clamped_p,
            "impact": clamped_i,
            "risk_score": risk_score,
            "mitigation": mitigation,
            "blast_radius": blast_radius,
        }
        self._risks.setdefault(room_id, []).append(risk)
        return risk

    def list_risks(self, room_id: str) -> List[Dict[str, Any]]:
        return self._risks.get(room_id, [])
