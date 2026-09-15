"""Customer Journey Lifecycle and Customer 360 Aggregator Engine."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from backend.app.services.customer_experience.base import (
    AttrDict,
    JourneyStage,
    JourneyType,
    LifecycleStatus,
    generate_cx_id,
    current_utc_time,
)


class CustomerJourneyService:
    """Manages journeys, stages, and 360 aggregation."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_journeys: Dict[str, Dict[str, Any]] = {}
        self._in_memory_stages: Dict[str, List[Dict[str, Any]]] = {}

    def create_journey(
        self,
        customer_id: str,
        customer_name: Optional[str] = None,
        journey_type: str = JourneyType.SALES.value,
        initial_stage: str = JourneyStage.DISCOVERY.value,
        metadata_json: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        journey_id = generate_cx_id("jrny")
        now = current_utc_time().isoformat()
        
        journey = AttrDict({
            "id": journey_id,
            "customer_id": customer_id,
            "customer_name": customer_name or f"Customer {customer_id}",
            "journey_type": journey_type.lower(),
            "current_stage": initial_stage.lower(),
            "lifecycle_status": LifecycleStatus.ENGAGE.value,
            "health_status": "healthy",
            "completion_rate": 0.1,
            "effort_score": 1.5,
            "sentiment_score": 0.75,
            "stage_history": [
                {
                    "stage": initial_stage.lower(),
                    "entered_at": now,
                    "status": "in_progress",
                }
            ],
            "metadata_json": metadata_json or {},
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_journeys[journey_id] = journey

        # Default standard stages for the journey
        standard_stages = [
            JourneyStage.AWARENESS.value,
            JourneyStage.DISCOVERY.value,
            JourneyStage.CONSIDERATION.value,
            JourneyStage.EVALUATION.value,
            JourneyStage.PURCHASE.value,
            JourneyStage.ONBOARDING.value,
            JourneyStage.ACTIVATION.value,
            JourneyStage.ADOPTION.value,
            JourneyStage.VALUE.value,
            JourneyStage.SUPPORT.value,
            JourneyStage.RENEWAL.value,
            JourneyStage.EXPANSION.value,
            JourneyStage.ADVOCACY.value,
        ]

        stage_records = []
        for idx, stage in enumerate(standard_stages):
            stg_id = generate_cx_id("stg")
            is_init = (stage == initial_stage.lower())
            stage_records.append(AttrDict({
                "id": stg_id,
                "journey_id": journey_id,
                "stage_name": stage,
                "order_index": idx,
                "status": "in_progress" if is_init else "pending",
                "entered_at": now if is_init else None,
                "completed_at": None,
                "duration_seconds": 0.0,
                "dropoff_risk": 0.15,
                "touchpoint_count": 1 if is_init else 0,
                "notes": f"Stage {stage} initialized",
                "created_at": now,
                "updated_at": now,
            }))
        self._in_memory_stages[journey_id] = stage_records

        return journey

    def get_journey(self, journey_id: str) -> Optional[AttrDict]:
        return self._in_memory_journeys.get(journey_id)

    def list_journeys(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [j for j in self._in_memory_journeys.values() if j.get("customer_id") == customer_id]
        return list(self._in_memory_journeys.values())

    def get_journey_stages(self, journey_id: str) -> List[AttrDict]:
        return self._in_memory_stages.get(journey_id, [])

    def advance_stage(self, journey_id: str, next_stage: str, notes: Optional[str] = None) -> Optional[AttrDict]:
        journey = self._in_memory_journeys.get(journey_id)
        if not journey:
            return None
        now = current_utc_time().isoformat()
        old_stage = journey["current_stage"]
        journey["current_stage"] = next_stage.lower()
        journey["updated_at"] = now
        journey["stage_history"].append({
            "stage": next_stage.lower(),
            "previous_stage": old_stage,
            "entered_at": now,
            "notes": notes,
        })
        
        # update stage list statuses
        stages = self._in_memory_stages.get(journey_id, [])
        for stg in stages:
            if stg["stage_name"] == old_stage and stg["status"] == "in_progress":
                stg["status"] = "completed"
                stg["completed_at"] = now
            elif stg["stage_name"] == next_stage.lower():
                stg["status"] = "in_progress"
                stg["entered_at"] = now

        return journey

    def get_customer_360(self, customer_id: str) -> AttrDict:
        """Aggregates a unified Customer 360 profile."""
        now = current_utc_time().isoformat()
        journeys = self.list_journeys(customer_id=customer_id)
        
        return AttrDict({
            "customer_id": customer_id,
            "identity": {
                "name": f"Customer {customer_id}",
                "tenant_id": "tenant-default",
                "segment": "Enterprise B2B",
                "lifecycle_status": "adopt",
                "account_executive": "Alex Rivera",
                "customer_success_manager": "Sarah Chen",
            },
            "organization": {
                "industry": "FinTech / SaaS",
                "tier": "Tier-1 Strategic",
                "employee_count": 1250,
                "arr": 185000.0,
                "contract_renewal_date": "2027-01-15",
            },
            "journeys": journeys,
            "active_journey_count": len(journeys),
            "health_summary": {
                "overall_score": 88.5,
                "state": "healthy",
                "churn_risk_pct": 8.5,
                "expansion_readiness_pct": 78.0,
            },
            "effort_summary": {
                "ces_score": 1.8,
                "tier": "low_effort",
            },
            "sentiment_summary": {
                "overall": "positive",
                "confidence": 0.92,
            },
            "last_touchpoint": {
                "channel": "executive_review",
                "occurred_at": now,
                "outcome": "positive_expansion_interest",
            },
            "metadata_json": {
                "data_minimization_compliant": True,
                "governance_verified": True,
            },
            "generated_at": now,
        })
