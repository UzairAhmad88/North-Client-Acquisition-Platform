"""
Planetary Resilience Fabric Service
Handles critical system registries, multi-dimensional scorecards, business continuity, RTO/RPO tracking, and dependency-aware recovery.
"""

from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime


class PlanetaryResilienceFabricService:
    def __init__(self):
        self.systems_registry: Dict[str, Dict[str, Any]] = {}
        self.continuity_plans: Dict[str, Dict[str, Any]] = {}

    def register_critical_system(
        self,
        name: str,
        category: str,
        criticality_level: str,
        owner_organization: str,
        dependencies: Optional[List[str]] = None,
        failure_modes: Optional[List[str]] = None,
        recovery_objectives: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        node_id = f"sys-{uuid.uuid4().hex[:8]}"
        record = {
            "node_id": node_id,
            "name": name,
            "category": category,  # Energy, Water, Food, Healthcare, Comms, Transport, Finance, Cloud, Government
            "criticality_level": criticality_level,  # Essential, Important, Non-Critical
            "resilience_state": "Stable",
            "owner_organization": owner_organization,
            "dependencies": dependencies or [],
            "failure_modes": failure_modes or [],
            "recovery_objectives": recovery_objectives or {"RTO_hours": 4, "RPO_hours": 1, "MTD_hours": 12},
            "scorecard": {
                "redundancy": 85.0,
                "capacity": 80.0,
                "adaptability": 75.0,
                "recovery_speed": 90.0,
                "dependency_concentration": 40.0,
                "resource_availability": 88.0,
                "governance_readiness": 92.0,
            },
            "created_at": datetime.utcnow().isoformat(),
        }
        self.systems_registry[node_id] = record
        return record

    def get_resilience_scorecard(self, node_id: str) -> Dict[str, Any]:
        system = self.systems_registry.get(node_id)
        if not system:
            return {"status": "error", "message": f"System {node_id} not found"}
        
        # Calculate maturity model level
        scores = system["scorecard"]
        avg_score = sum(scores.values()) / len(scores)
        if avg_score >= 85:
            maturity = "Adaptive"
        elif avg_score >= 70:
            maturity = "Resilient"
        elif avg_score >= 55:
            maturity = "Managed"
        elif avg_score >= 40:
            maturity = "Developing"
        else:
            maturity = "Initial"

        return {
            "node_id": node_id,
            "name": system["name"],
            "scorecard_dimensions": scores,
            "average_resilience_index": round(avg_score, 2),
            "maturity_level": maturity,
            "state": system["resilience_state"],
            "dependencies_count": len(system["dependencies"]),
        }

    def create_business_continuity_plan(
        self,
        organization_name: str,
        critical_functions: List[str],
        dependencies: List[str],
        fallback_locations: List[str],
        backup_personnel: List[str],
        rto_rpo_targets: Dict[str, Any],
    ) -> Dict[str, Any]:
        plan_id = f"bcp-{uuid.uuid4().hex[:8]}"
        plan = {
            "plan_id": plan_id,
            "organization_name": organization_name,
            "critical_functions": critical_functions,
            "dependencies": dependencies,
            "fallback_locations": fallback_locations,
            "backup_personnel": backup_personnel,
            "rto_rpo_targets": rto_rpo_targets,
            "last_tested": None,
            "test_status": "Untested",
            "created_at": datetime.utcnow().isoformat(),
        }
        self.continuity_plans[plan_id] = plan
        return plan

    def test_continuity_plan(self, plan_id: str, simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        plan = self.continuity_plans.get(plan_id)
        if not plan:
            return {"status": "error", "message": f"Plan {plan_id} not found"}
        
        plan["last_tested"] = datetime.utcnow().isoformat()
        plan["test_status"] = simulation_results.get("status", "Passed")
        plan["test_metrics"] = simulation_results
        return plan

    def calculate_dependency_aware_recovery_sequence(self, impacted_nodes: List[str]) -> Dict[str, Any]:
        # Sort nodes by upstream dependency count & criticality level
        sequence = []
        for node_id in impacted_nodes:
            sys_info = self.systems_registry.get(node_id, {"name": node_id, "criticality_level": "Important", "dependencies": []})
            sequence.append({
                "node_id": node_id,
                "name": sys_info["name"],
                "criticality_level": sys_info["criticality_level"],
                "upstream_dependencies": len(sys_info.get("dependencies", [])),
                "priority_rank": 1 if sys_info["criticality_level"] == "Essential" else 2,
            })
        
        sequence.sort(key=lambda x: (x["priority_rank"], x["upstream_dependencies"]))
        return {
            "total_impacted_systems": len(impacted_nodes),
            "recommended_recovery_sequence": sequence,
            "timestamp": datetime.utcnow().isoformat(),
        }
