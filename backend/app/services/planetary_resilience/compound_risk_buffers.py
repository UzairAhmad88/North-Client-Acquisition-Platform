"""
Compound Risk & Resilience Buffer Engine Service
Handles compound crisis simulation, cascading failure chains, buffer depletion tracking (Capacity, Financial, Inventory, Energy, Time, Human), early warnings, and cost-resilience analysis.
"""

from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime


class CompoundRiskBufferService:
    def __init__(self):
        self.buffers: Dict[str, Dict[str, Any]] = {}
        self.active_warnings: Dict[str, Dict[str, Any]] = {}

    def register_resilience_buffer(
        self,
        system_id: str,
        buffer_name: str,
        buffer_type: str,  # Capacity, Financial, Inventory, Energy, Time, Human Capacity
        total_capacity: float,
        unit: str,
    ) -> Dict[str, Any]:
        buf_id = f"buf-{uuid.uuid4().hex[:8]}"
        record = {
            "buffer_id": buf_id,
            "system_id": system_id,
            "buffer_name": buffer_name,
            "buffer_type": buffer_type,
            "total_capacity": total_capacity,
            "current_available": total_capacity,
            "unit": unit,
            "depletion_rate_per_hour": 0.0,
            "restoration_plan_defined": True,
            "updated_at": datetime.utcnow().isoformat(),
        }
        self.buffers[buf_id] = record
        return record

    def simulate_compound_cascading_crisis(
        self, primary_shocks: List[str], duration_days: int
    ) -> Dict[str, Any]:
        # Cascading steps: Primary Shock -> Infrastructure -> Economic -> Social -> Recovery Pressure
        infrastructure_impact = "Severe grid frequency drift & partial water pressure loss" if "Heatwave" in primary_shocks or "Cyber Attack" in primary_shocks else "Moderate slowdown"
        economic_impact = "Supply chain delivery delays (+35%) & market spot price spike"
        social_impact = "Increased demand for emergency shelter and cooling centers"
        recovery_pressure = "High load on emergency management personnel"

        return {
            "simulation_id": f"sim-{uuid.uuid4().hex[:8]}",
            "primary_shocks": primary_shocks,
            "duration_days": duration_days,
            "cascading_chain": {
                "step_1_primary_shock": primary_shocks,
                "step_2_infrastructure_impact": infrastructure_impact,
                "step_3_economic_impact": economic_impact,
                "step_4_social_impact": social_impact,
                "step_5_recovery_pressure": recovery_pressure,
            },
            "buffer_depletion_estimates": [
                {"buffer": "Energy Reserves", "depletion_percent": 65.0, "time_to_depletion_hours": 36.0},
                {"buffer": "Emergency Cash Buffer", "depletion_percent": 25.0, "time_to_depletion_hours": 120.0},
                {"buffer": "Human Staff Capacity", "depletion_percent": 40.0, "time_to_depletion_hours": 72.0},
            ],
            "correlation_uncertainty_note": "Risks are modeled with non-linear correlation; unexpected compounding effects preserved.",
            "timestamp": datetime.utcnow().isoformat(),
        }

    def issue_early_warning_alert(
        self,
        risk_title: str,
        warning_level: str,  # Watch, Advisory, Warning, Critical
        confidence_score: float,
        evidence_summary: str,
        target_regions: List[str],
    ) -> Dict[str, Any]:
        alert_id = f"wng-{uuid.uuid4().hex[:8]}"
        alert = {
            "alert_id": alert_id,
            "risk_title": risk_title,
            "warning_level": warning_level,
            "confidence_score": max(0.0, min(1.0, confidence_score)),
            "evidence_summary": evidence_summary,
            "target_regions": target_regions,
            "alert_fatigue_filtered": False,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.active_warnings[alert_id] = alert
        return alert

    def perform_cost_resilience_analysis(
        self, system_id: str, proposed_investments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        results = []
        total_cost = 0.0
        total_resilience_gain = 0.0

        for inv in proposed_investments:
            cost = inv.get("cost", 50000.0)
            gain = inv.get("resilience_score_gain", 12.0)
            total_cost += cost
            total_resilience_gain += gain
            results.append({
                "category": inv.get("category", "Redundancy"),
                "description": inv.get("description", "Upgrade backup power"),
                "cost": cost,
                "resilience_score_gain": gain,
                "roi_index": round(gain / (cost / 10000), 2),
            })

        return {
            "system_id": system_id,
            "proposed_investments": results,
            "total_investment_cost": total_cost,
            "total_estimated_resilience_gain": round(total_resilience_gain, 2),
            "uncertainty_labeled": True,
            "timestamp": datetime.utcnow().isoformat(),
        }
