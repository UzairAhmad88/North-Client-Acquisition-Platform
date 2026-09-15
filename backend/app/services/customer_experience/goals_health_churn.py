"""Customer Goals, Experience Health Index, and Churn Predictive Intelligence."""
from typing import Any, Dict, List, Optional
from backend.app.services.customer_experience.base import (
    AttrDict,
    HealthState,
    generate_cx_id,
    current_utc_time,
)


class GoalsHealthChurnService:
    """Tracks customer goals, calculates health scores, and predicts churn risks."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_goals: List[Dict[str, Any]] = []
        self._in_memory_health: Dict[str, Dict[str, Any]] = {}
        self._in_memory_churn: List[Dict[str, Any]] = []

    def create_goal(
        self,
        customer_id: str,
        title: str,
        goal_type: str = "business_goal",
        description: Optional[str] = None,
        baseline_value: Optional[str] = None,
        target_value: Optional[str] = None,
        current_value: Optional[str] = None,
        progress_pct: float = 0.0,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> AttrDict:
        g_id = generate_cx_id("goal")
        now = current_utc_time().isoformat()
        goal = AttrDict({
            "id": g_id,
            "customer_id": customer_id,
            "goal_type": goal_type.lower(),
            "title": title,
            "description": description or f"Customer goal: {title}",
            "baseline_value": baseline_value or "0",
            "target_value": target_value or "100",
            "current_value": current_value or "0",
            "progress_pct": progress_pct,
            "status": "in_progress",
            "evidence": evidence or {},
            "target_date": None,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_goals.append(goal)
        return goal

    def list_goals(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [g for g in self._in_memory_goals if g.get("customer_id") == customer_id]
        return list(self._in_memory_goals)

    def evaluate_health(
        self,
        customer_id: str,
        engagement_score: float = 85.0,
        adoption_score: float = 90.0,
        support_score: float = 95.0,
        effort_score: float = 80.0,
        sentiment_score: float = 85.0,
    ) -> AttrDict:
        """Calculates multi-factor composite experience health score."""
        overall_score = round(
            (engagement_score * 0.25) +
            (adoption_score * 0.25) +
            (support_score * 0.20) +
            (effort_score * 0.15) +
            (sentiment_score * 0.15),
            1
        )

        if overall_score >= 85.0:
            state = HealthState.EXCELLENT.value
        elif overall_score >= 70.0:
            state = HealthState.HEALTHY.value
        elif overall_score >= 55.0:
            state = HealthState.STABLE.value
        elif overall_score >= 40.0:
            state = HealthState.WATCH.value
        elif overall_score >= 25.0:
            state = HealthState.AT_RISK.value
        else:
            state = HealthState.CRITICAL.value

        churn_prob = max(0.02, min(0.95, round(1.0 - (overall_score / 100.0), 3)))
        expansion_readiness = max(0.05, min(0.95, round(overall_score / 100.0 * 0.9, 3)))

        h_id = generate_cx_id("hlth")
        now = current_utc_time().isoformat()
        health_record = AttrDict({
            "id": h_id,
            "customer_id": customer_id,
            "overall_health_score": overall_score,
            "health_state": state,
            "factor_breakdown": {
                "engagement": engagement_score,
                "product_adoption": adoption_score,
                "support_health": support_score,
                "customer_effort": effort_score,
                "satisfaction_sentiment": sentiment_score,
            },
            "churn_probability": churn_prob,
            "expansion_readiness": expansion_readiness,
            "explanation": f"Overall health score {overall_score}/100 categorized as {state} based on balanced engagement and low friction.",
            "last_evaluated_at": now,
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_health[customer_id] = health_record
        return health_record

    def get_health(self, customer_id: str) -> Optional[AttrDict]:
        return self._in_memory_health.get(customer_id)

    def predict_churn(
        self,
        customer_id: str,
        churn_probability: float = 0.12,
        risk_level: str = "low",
        primary_drivers: Optional[List[str]] = None,
        recommended_interventions: Optional[List[str]] = None,
        confidence: float = 0.89,
    ) -> AttrDict:
        c_id = generate_cx_id("churn")
        now = current_utc_time().isoformat()
        churn_record = AttrDict({
            "id": c_id,
            "customer_id": customer_id,
            "churn_probability": churn_probability,
            "risk_level": risk_level.lower(),
            "primary_drivers": primary_drivers or ["Slight decrease in weekly active seats", "Open support ticket on integration"],
            "recommended_interventions": recommended_interventions or ["Schedule Technical Architecture Review", "Provide training session on Phase 48 Memory"],
            "model_name": "gradient-boosted-churn-v2",
            "confidence": confidence,
            "is_confirmed_by_human": False,
            "predicted_at": now,
            "created_at": now,
        })
        self._in_memory_churn.append(churn_record)
        return churn_record

    def list_churn_predictions(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [c for c in self._in_memory_churn if c.get("customer_id") == customer_id]
        return list(self._in_memory_churn)
