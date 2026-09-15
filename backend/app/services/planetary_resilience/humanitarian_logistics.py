"""
Humanitarian Coordination & Logistics Service
Handles humanitarian needs modeling, resource matching, distribution route simulation, logistics bottleneck modeling, and anti-fraud verification workflows.
"""

from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime


class HumanitarianLogisticsService:
    def __init__(self):
        self.resource_inventory: Dict[str, Dict[str, Any]] = {}
        self.verified_needs: Dict[str, Dict[str, Any]] = {}

    def register_humanitarian_resource(
        self,
        resource_type: str,  # Food, Water, Shelter, Medical Support, Transport, Comms
        quantity: float,
        unit: str,
        location: str,
        owner_organization: str,
        expiration_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        res_id = f"res-{uuid.uuid4().hex[:8]}"
        resource = {
            "resource_id": res_id,
            "resource_type": resource_type,
            "quantity": quantity,
            "allocated_quantity": 0.0,
            "available_quantity": quantity,
            "unit": unit,
            "location": location,
            "owner_organization": owner_organization,
            "expiration_date": expiration_date,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.resource_inventory[res_id] = resource
        return resource

    def log_humanitarian_need(
        self,
        incident_id: str,
        location: str,
        resource_type: str,
        requested_quantity: float,
        unit: str,
        urgency_level: str,  # Critical, High, Medium, Low
        requesting_entity: str,
    ) -> Dict[str, Any]:
        need_id = f"need-{uuid.uuid4().hex[:8]}"
        need = {
            "need_id": need_id,
            "incident_id": incident_id,
            "location": location,
            "resource_type": resource_type,
            "requested_quantity": requested_quantity,
            "fulfilled_quantity": 0.0,
            "unit": unit,
            "urgency_level": urgency_level,
            "requesting_entity": requesting_entity,
            "verification_status": "Human_Verification_Pending",
            "fraud_risk_score": 0.05,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.verified_needs[need_id] = need
        return need

    def match_resources_to_needs(self, need_id: str) -> Dict[str, Any]:
        need = self.verified_needs.get(need_id)
        if not need:
            return {"status": "error", "message": f"Need {need_id} not found"}
        
        # Simple proximity & category matching engine
        matched_resources = []
        needed_type = need["resource_type"]
        remaining_qty = need["requested_quantity"] - need["fulfilled_quantity"]

        for res_id, res in self.resource_inventory.items():
            if res["resource_type"] == needed_type and res["available_quantity"] > 0:
                allocated = min(remaining_qty, res["available_quantity"])
                matched_resources.append({
                    "resource_id": res_id,
                    "supplier": res["owner_organization"],
                    "origin": res["location"],
                    "allocated_quantity": allocated,
                })
                remaining_qty -= allocated
                if remaining_qty <= 0:
                    break

        return {
            "need_id": need_id,
            "resource_type": needed_type,
            "requested_quantity": need["requested_quantity"],
            "matched_quantity": need["requested_quantity"] - remaining_qty,
            "fulfillment_percentage": round(((need["requested_quantity"] - remaining_qty) / need["requested_quantity"]) * 100, 2),
            "allocations": matched_resources,
            "matched_at": datetime.utcnow().isoformat(),
        }

    def simulate_logistics_distribution(
        self,
        origin: str,
        destination: str,
        resource_type: str,
        quantity: float,
        simulated_shocks: Optional[List[str]] = None,  # Road Closure, Fuel Shortage, Port Failure, Comms Loss
    ) -> Dict[str, Any]:
        shocks = simulated_shocks or []
        base_travel_time_hours = 6.0
        delay_hours = 0.0
        bottlenecks = []

        if "Road Closure" in shocks:
            delay_hours += 4.5
            bottlenecks.append("Detour via Secondary Highway (+4.5 hrs)")
        if "Fuel Shortage" in shocks:
            delay_hours += 3.0
            bottlenecks.append("Refueling Queue at Regional Depot (+3.0 hrs)")
        if "Port Failure" in shocks:
            delay_hours += 12.0
            bottlenecks.append("Port Congestion / Redirection (+12.0 hrs)")

        total_time = base_travel_time_hours + delay_hours
        risk_level = "High" if delay_hours > 6.0 else "Low"

        return {
            "origin": origin,
            "destination": destination,
            "resource_type": resource_type,
            "quantity": quantity,
            "base_travel_time_hours": base_travel_time_hours,
            "total_estimated_delivery_hours": round(total_time, 2),
            "simulated_shocks": shocks,
            "detected_bottlenecks": bottlenecks,
            "delivery_risk": risk_level,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def flag_suspicious_claim(self, claim_id: str, reason: str) -> Dict[str, Any]:
        need = self.verified_needs.get(claim_id)
        if need:
            need["verification_status"] = "Under_Fraud_Review"
            need["fraud_risk_score"] = 0.85
        return {
            "claim_id": claim_id,
            "status": "Flagged_For_Human_Review",
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
        }
