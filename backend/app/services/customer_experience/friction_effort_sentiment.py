"""Customer Friction Engine, Effort Scoring (CES), and Sentiment Analysis."""
from typing import Any, Dict, List, Optional
from backend.app.services.customer_experience.base import (
    AttrDict,
    EffortTier,
    FrictionSeverity,
    SentimentType,
    generate_cx_id,
    current_utc_time,
)


class FrictionEffortSentimentService:
    """Detects friction points, scores customer effort, and extracts sentiment/emotions."""

    def __init__(self, db_session=None):
        self.db = db_session
        self._in_memory_frictions: List[Dict[str, Any]] = []
        self._in_memory_efforts: List[Dict[str, Any]] = []
        self._in_memory_sentiments: List[Dict[str, Any]] = []

    def record_friction(
        self,
        customer_id: str,
        stage: str,
        friction_type: str,
        severity: str = FrictionSeverity.MEDIUM.value,
        description: str = "",
        evidence: Optional[Dict[str, Any]] = None,
        customer_impact: Optional[str] = None,
        business_impact: Optional[str] = None,
        confidence: float = 0.88,
        journey_id: Optional[str] = None,
    ) -> AttrDict:
        f_id = generate_cx_id("fric")
        now = current_utc_time().isoformat()
        friction = AttrDict({
            "id": f_id,
            "customer_id": customer_id,
            "journey_id": journey_id,
            "stage": stage.lower(),
            "friction_type": friction_type.lower(),
            "severity": severity.lower(),
            "description": description,
            "evidence": evidence or {},
            "customer_impact": customer_impact or "Delayed onboarding milestone",
            "business_impact": business_impact or "Slower time to value and increased support load",
            "confidence": confidence,
            "resolution_status": "open",
            "created_at": now,
            "updated_at": now,
        })
        self._in_memory_frictions.append(friction)
        return friction

    def list_frictions(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [f for f in self._in_memory_frictions if f.get("customer_id") == customer_id]
        return list(self._in_memory_frictions)

    def calculate_effort(
        self,
        customer_id: str,
        stage: str,
        step_count: int = 1,
        form_count: int = 0,
        repeated_info_instances: int = 0,
        waiting_time_minutes: float = 0.0,
        support_contacts_count: int = 0,
        journey_id: Optional[str] = None,
    ) -> AttrDict:
        """Calculates Customer Effort Score (CES: 1.0 to 5.0) and assigns tier."""
        # Baseline effort formula
        base_score = 1.0 + (step_count * 0.15) + (form_count * 0.25) + (repeated_info_instances * 0.6) + (waiting_time_minutes / 60.0 * 0.4) + (support_contacts_count * 0.5)
        ces_score = min(5.0, max(1.0, round(base_score, 2)))

        if ces_score <= 2.0:
            tier = EffortTier.LOW_EFFORT.value
        elif ces_score <= 3.2:
            tier = EffortTier.MODERATE_EFFORT.value
        elif ces_score <= 4.2:
            tier = EffortTier.HIGH_EFFORT.value
        else:
            tier = EffortTier.CRITICAL_FRICTION.value

        e_id = generate_cx_id("eff")
        now = current_utc_time().isoformat()
        effort_record = AttrDict({
            "id": e_id,
            "customer_id": customer_id,
            "journey_id": journey_id,
            "stage": stage.lower(),
            "ces_score": ces_score,
            "effort_tier": tier,
            "step_count": step_count,
            "form_count": form_count,
            "repeated_info_instances": repeated_info_instances,
            "waiting_time_minutes": waiting_time_minutes,
            "support_contacts_count": support_contacts_count,
            "created_at": now,
        })
        self._in_memory_efforts.append(effort_record)
        return effort_record

    def list_efforts(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [e for e in self._in_memory_efforts if e.get("customer_id") == customer_id]
        return list(self._in_memory_efforts)

    def record_sentiment(
        self,
        customer_id: str,
        source_channel: str,
        sentiment: str = SentimentType.NEUTRAL.value,
        confidence: float = 0.85,
        model_version: str = "cx-sentiment-v2",
        detected_emotions: Optional[List[str]] = None,
        excerpt: Optional[str] = None,
        is_customer_stated: bool = False,
    ) -> AttrDict:
        s_id = generate_cx_id("snt")
        now = current_utc_time().isoformat()
        sentiment_record = AttrDict({
            "id": s_id,
            "customer_id": customer_id,
            "source_channel": source_channel.lower(),
            "sentiment": sentiment.lower(),
            "confidence": confidence,
            "model_version": model_version,
            "detected_emotions": detected_emotions or ["satisfaction", "confidence"],
            "excerpt": excerpt or "Customer expressed satisfaction with setup.",
            "is_customer_stated": is_customer_stated,
            "recorded_at": now,
            "created_at": now,
        })
        self._in_memory_sentiments.append(sentiment_record)
        return sentiment_record

    def list_sentiments(self, customer_id: Optional[str] = None) -> List[AttrDict]:
        if customer_id:
            return [s for s in self._in_memory_sentiments if s.get("customer_id") == customer_id]
        return list(self._in_memory_sentiments)
