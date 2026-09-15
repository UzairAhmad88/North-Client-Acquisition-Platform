"""FastAPI Router for Phase 57: Unified Customer Experience, Journey Intelligence & Optimization Platform."""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from backend.app.schemas.customer_experience import (
    AdvocacyCreateRequest,
    AlertCreateRequest,
    ChurnPredictRequest,
    CopilotQueryRequest,
    EffortCalculateRequest,
    EventRecordRequest,
    ExpansionCreateRequest,
    ExpectationGapRecordRequest,
    ExperimentCreateRequest,
    FrictionRecordRequest,
    GoalCreateRequest,
    HealthEvaluateRequest,
    JourneyCreateRequest,
    OpportunityCreateRequest,
    ReferralCreateRequest,
    RetentionCreateRequest,
    SentimentRecordRequest,
    StageAdvanceRequest,
    TouchpointRecordRequest,
    VoiceRecordRequest,
)
from backend.app.services.customer_experience.service import CustomerExperiencePlatformService

router = APIRouter(prefix="/customer-experience", tags=["Customer Experience & Journey Intelligence"])

# Global singleton service for in-process state consistency
_service = CustomerExperiencePlatformService()


@router.get("/overview")
async def get_overview():
    """Retrieve top-level CX overview metrics and aggregated telemetry."""
    return _service.get_overview_metrics()


@router.get("/customer-360/{customer_id}")
async def get_customer_360(customer_id: str):
    """Retrieve unified Customer 360 profile."""
    return _service.journeys.get_customer_360(customer_id=customer_id)


# --- Journeys & Path Analytics ---
@router.post("/journeys", status_code=status.HTTP_201_CREATED)
async def create_journey(req: JourneyCreateRequest):
    """Create a new customer journey."""
    return _service.journeys.create_journey(
        customer_id=req.customer_id,
        customer_name=req.customer_name,
        journey_type=req.journey_type,
        initial_stage=req.initial_stage,
        metadata_json=req.metadata_json,
    )


@router.get("/journeys")
async def list_journeys(customer_id: Optional[str] = Query(None)):
    """List customer journeys."""
    return _service.journeys.list_journeys(customer_id=customer_id)


@router.get("/journeys/{journey_id}")
async def get_journey(journey_id: str):
    """Get single journey details."""
    j = _service.journeys.get_journey(journey_id)
    if not j:
        raise HTTPException(status_code=404, detail=f"Journey {journey_id} not found")
    return j


@router.post("/journeys/{journey_id}/advance")
async def advance_journey_stage(journey_id: str, req: StageAdvanceRequest):
    """Advance a journey to next lifecycle stage."""
    j = _service.journeys.advance_stage(journey_id, req.next_stage, req.notes)
    if not j:
        raise HTTPException(status_code=404, detail=f"Journey {journey_id} not found")
    return j


@router.post("/journeys/{journey_id}/events", status_code=status.HTTP_201_CREATED)
async def record_journey_event(journey_id: str, req: EventRecordRequest):
    """Ingest a canonical journey event."""
    return _service.reconstruction.record_event(
        journey_id=journey_id,
        customer_id=req.customer_id,
        event_type=req.event_type,
        stage=req.stage,
        channel=req.channel,
        actor_type=req.actor_type,
        actor_id=req.actor_id,
        provenance_source=req.provenance_source,
        properties=req.properties,
    )


@router.get("/journeys/{journey_id}/events")
async def list_journey_events(journey_id: str):
    """List events for a specific journey."""
    return _service.reconstruction.list_events(journey_id)


@router.post("/journeys/{journey_id}/touchpoints", status_code=status.HTTP_201_CREATED)
async def record_touchpoint(journey_id: str, req: TouchpointRecordRequest):
    """Record a customer touchpoint interaction."""
    return _service.reconstruction.record_touchpoint(
        journey_id=journey_id,
        customer_id=req.customer_id,
        channel=req.channel,
        touchpoint_type=req.touchpoint_type,
        purpose=req.purpose,
        outcome=req.outcome,
        sentiment=req.sentiment,
        friction_detected=req.friction_detected,
        duration_seconds=req.duration_seconds,
        interaction_metadata=req.interaction_metadata,
    )


@router.get("/journeys/{journey_id}/touchpoints")
async def list_touchpoints(journey_id: str):
    """List touchpoints for a specific journey."""
    return _service.reconstruction.list_touchpoints(journey_id)


@router.get("/journeys/{journey_id}/variants")
async def get_journey_variants(journey_id: str):
    """Discover path variants for this journey."""
    return _service.reconstruction.discover_variants()


@router.get("/journeys/{journey_id}/metrics")
async def get_journey_metrics(journey_id: str):
    """Get metrics and reconstruction telemetry for journey."""
    return _service.reconstruction.reconstruct_journey_path(journey_id)


# --- Friction, Effort & Sentiment ---
@router.post("/friction", status_code=status.HTTP_201_CREATED)
async def record_friction(req: FrictionRecordRequest):
    """Record customer friction point."""
    return _service.friction_effort_sentiment.record_friction(
        customer_id=req.customer_id,
        stage=req.stage,
        friction_type=req.friction_type,
        severity=req.severity,
        description=req.description,
        evidence=req.evidence,
        customer_impact=req.customer_impact,
        business_impact=req.business_impact,
        confidence=req.confidence,
        journey_id=req.journey_id,
    )


@router.get("/friction")
async def list_frictions(customer_id: Optional[str] = Query(None)):
    """List recorded friction points."""
    return _service.friction_effort_sentiment.list_frictions(customer_id)


@router.post("/effort", status_code=status.HTTP_201_CREATED)
async def calculate_effort(req: EffortCalculateRequest):
    """Calculate and record Customer Effort Score (CES)."""
    return _service.friction_effort_sentiment.calculate_effort(
        customer_id=req.customer_id,
        stage=req.stage,
        step_count=req.step_count,
        form_count=req.form_count,
        repeated_info_instances=req.repeated_info_instances,
        waiting_time_minutes=req.waiting_time_minutes,
        support_contacts_count=req.support_contacts_count,
        journey_id=req.journey_id,
    )


@router.get("/effort")
async def list_efforts(customer_id: Optional[str] = Query(None)):
    """List customer effort score records."""
    return _service.friction_effort_sentiment.list_efforts(customer_id)


@router.post("/sentiment", status_code=status.HTTP_201_CREATED)
async def record_sentiment(req: SentimentRecordRequest):
    """Record sentiment analysis observation."""
    return _service.friction_effort_sentiment.record_sentiment(
        customer_id=req.customer_id,
        source_channel=req.source_channel,
        sentiment=req.sentiment,
        confidence=req.confidence,
        model_version=req.model_version,
        detected_emotions=req.detected_emotions,
        excerpt=req.excerpt,
        is_customer_stated=req.is_customer_stated,
    )


@router.get("/sentiment")
async def list_sentiments(customer_id: Optional[str] = Query(None)):
    """List customer sentiment observations."""
    return _service.friction_effort_sentiment.list_sentiments(customer_id)


# --- Goals, Health & Churn ---
@router.post("/goals", status_code=status.HTTP_201_CREATED)
async def create_goal(req: GoalCreateRequest):
    """Record customer goal and milestone tracking."""
    return _service.goals_health_churn.create_goal(
        customer_id=req.customer_id,
        title=req.title,
        goal_type=req.goal_type,
        description=req.description,
        baseline_value=req.baseline_value,
        target_value=req.target_value,
        current_value=req.current_value,
        progress_pct=req.progress_pct,
        evidence=req.evidence,
    )


@router.get("/goals")
async def list_goals(customer_id: Optional[str] = Query(None)):
    """List customer goals."""
    return _service.goals_health_churn.list_goals(customer_id)


@router.post("/health/evaluate")
async def evaluate_health(req: HealthEvaluateRequest):
    """Evaluate multi-factor composite experience health."""
    return _service.goals_health_churn.evaluate_health(
        customer_id=req.customer_id,
        engagement_score=req.engagement_score,
        adoption_score=req.adoption_score,
        support_score=req.support_score,
        effort_score=req.effort_score,
        sentiment_score=req.sentiment_score,
    )


@router.get("/health")
async def get_health(customer_id: str = Query("cust-demo-001")):
    """Get experience health profile for customer."""
    h = _service.goals_health_churn.get_health(customer_id)
    if not h:
        return _service.goals_health_churn.evaluate_health(customer_id=customer_id)
    return h


@router.post("/churn/predict", status_code=status.HTTP_201_CREATED)
async def predict_churn(req: ChurnPredictRequest):
    """Generate predictive churn analysis record."""
    return _service.goals_health_churn.predict_churn(
        customer_id=req.customer_id,
        churn_probability=req.churn_probability,
        risk_level=req.risk_level,
        primary_drivers=req.primary_drivers,
        recommended_interventions=req.recommended_interventions,
        confidence=req.confidence,
    )


@router.get("/churn")
async def list_churn_predictions(customer_id: Optional[str] = Query(None)):
    """List churn risk predictions."""
    return _service.goals_health_churn.list_churn_predictions(customer_id)


# --- Retention, Expansion, Advocacy & Referrals ---
@router.post("/retention", status_code=status.HTTP_201_CREATED)
async def create_retention_opportunity(req: RetentionCreateRequest):
    """Log customer retention intervention opportunity."""
    return _service.expansion_advocacy_referrals.create_retention_opportunity(
        customer_id=req.customer_id,
        title=req.title,
        trigger_reason=req.trigger_reason,
        proposed_action=req.proposed_action,
        impact_estimate=req.impact_estimate,
        effort_required=req.effort_required,
    )


@router.get("/retention")
async def list_retention_opportunities(customer_id: Optional[str] = Query(None)):
    """List retention opportunities."""
    return _service.expansion_advocacy_referrals.list_retention_opportunities(customer_id)


@router.post("/expansion", status_code=status.HTTP_201_CREATED)
async def create_expansion_opportunity(req: ExpansionCreateRequest):
    """Log expansion opportunity."""
    return _service.expansion_advocacy_referrals.create_expansion_opportunity(
        customer_id=req.customer_id,
        title=req.title,
        expansion_type=req.expansion_type,
        description=req.description,
        estimated_arr_value=req.estimated_arr_value,
        evidence_signals=req.evidence_signals,
        confidence=req.confidence,
    )


@router.get("/expansion")
async def list_expansion_opportunities(customer_id: Optional[str] = Query(None)):
    """List expansion opportunities."""
    return _service.expansion_advocacy_referrals.list_expansion_opportunities(customer_id)


@router.post("/advocacy", status_code=status.HTTP_201_CREATED)
async def create_advocacy_record(req: AdvocacyCreateRequest):
    """Record customer testimonial / case study advocacy."""
    return _service.expansion_advocacy_referrals.create_advocacy_record(
        customer_id=req.customer_id,
        title=req.title,
        content=req.content,
        advocacy_type=req.advocacy_type,
        permission_granted=req.permission_granted,
    )


@router.get("/advocacy")
async def list_advocacy_records(customer_id: Optional[str] = Query(None)):
    """List customer advocacy records."""
    return _service.expansion_advocacy_referrals.list_advocacy_records(customer_id)


@router.post("/referrals", status_code=status.HTTP_201_CREATED)
async def create_referral(req: ReferralCreateRequest):
    """Log incoming customer referral."""
    return _service.expansion_advocacy_referrals.create_referral(
        referrer_customer_id=req.referrer_customer_id,
        referred_company_name=req.referred_company_name,
        referred_contact_email=req.referred_contact_email,
        relationship_context=req.relationship_context,
        conversion_value=req.conversion_value,
    )


@router.get("/referrals")
async def list_referrals(referrer_customer_id: Optional[str] = Query(None)):
    """List referrals."""
    return _service.expansion_advocacy_referrals.list_referrals(referrer_customer_id)


@router.get("/segments")
async def list_segments():
    """List customer segmentation cohorts."""
    return _service.expansion_advocacy_referrals.list_segments()


@router.get("/personas")
async def list_personas():
    """List evidence-backed customer personas."""
    return _service.expansion_advocacy_referrals.list_personas()


@router.get("/cohorts")
async def list_cohorts():
    """List customer journey cohorts."""
    return _service.expansion_advocacy_referrals.list_segments()


# --- Voice of Customer & Expectations ---
@router.post("/voice-of-customer", status_code=status.HTTP_201_CREATED)
async def record_voice(req: VoiceRecordRequest):
    """Record Voice of Customer feedback statement."""
    return _service.voc_expectations.record_voice(
        customer_id=req.customer_id,
        source_channel=req.source_channel,
        quote_text=req.quote_text,
        feedback_category=req.feedback_category,
        extracted_topics=req.extracted_topics,
        sentiment=req.sentiment,
    )


@router.get("/voice-of-customer")
async def list_voice_records(customer_id: Optional[str] = Query(None)):
    """List VoC feedback records and themes."""
    return {
        "records": _service.voc_expectations.list_voice_records(customer_id),
        "themes": _service.voc_expectations.list_voice_themes(),
    }


@router.post("/expectations", status_code=status.HTTP_201_CREATED)
async def record_expectation_gap(req: ExpectationGapRecordRequest):
    """Record expectation gap (PROMISED vs EXPECTED vs DELIVERED)."""
    return _service.voc_expectations.record_expectation_gap(
        customer_id=req.customer_id,
        area=req.area,
        promised_capability=req.promised_capability,
        customer_expected=req.customer_expected,
        delivered_reality=req.delivered_reality,
        gap_severity=req.gap_severity,
        evidence_source=req.evidence_source,
        remediation_action=req.remediation_action,
    )


@router.get("/expectations")
async def list_expectation_gaps(customer_id: Optional[str] = Query(None)):
    """List identified expectation gaps."""
    return _service.voc_expectations.list_expectation_gaps(customer_id)


@router.get("/communication")
async def get_communication_analytics(customer_id: str = Query("cust-demo-001")):
    """Get customer communication clarity and SLA analytics."""
    return _service.voc_expectations.get_communication_analytics(customer_id)


# --- Experiments, Simulation, Optimization & Alerts ---
@router.post("/experiments", status_code=status.HTTP_201_CREATED)
async def create_experiment(req: ExperimentCreateRequest):
    """Create customer experience experiment."""
    return _service.experiments_alerts.create_experiment(
        name=req.name,
        hypothesis=req.hypothesis,
        control_variant=req.control_variant,
        treatment_variant=req.treatment_variant,
        target_stage=req.target_stage,
        primary_metric=req.primary_metric,
        experiment_type=req.experiment_type,
    )


@router.get("/experiments")
async def list_experiments():
    """List customer experience experiments."""
    return _service.experiments_alerts.list_experiments()


@router.get("/simulations")
async def simulate_changes(
    target_stage: str = Query("onboarding"),
    step_reduction: int = Query(2),
):
    """Simulate journey optimization impact."""
    return _service.experiments_alerts.simulate_journey_changes(
        target_stage=target_stage,
        reduction_in_steps=step_reduction,
    )


@router.get("/optimization")
async def get_optimization_summary():
    """Get journey optimization objectives and projected gains."""
    return {
        "bottlenecks": _service.experiments_alerts.detect_bottlenecks(),
        "simulations": _service.experiments_alerts.simulate_journey_changes("onboarding"),
        "top_opportunities": _service.experiments_alerts.list_opportunities(),
    }


@router.get("/bottlenecks")
async def list_bottlenecks():
    """Detect drop-off and friction bottlenecks."""
    return _service.experiments_alerts.detect_bottlenecks()


@router.get("/root-cause")
async def analyze_root_cause(problem: str = Query("Compliance questionnaire turnaround")):
    """Perform evidence-backed root cause analysis."""
    return _service.experiments_alerts.analyze_root_cause(problem_description=problem)


@router.post("/opportunities", status_code=status.HTTP_201_CREATED)
async def create_opportunity(req: OpportunityCreateRequest):
    """Create an experience improvement opportunity."""
    return _service.experiments_alerts.create_opportunity(
        problem=req.problem,
        stage=req.stage,
        proposed_improvement=req.proposed_improvement,
        business_impact=req.business_impact,
        customer_impact=req.customer_impact,
        effort=req.effort,
        confidence=req.confidence,
    )


@router.get("/opportunities")
async def list_opportunities():
    """List experience opportunities."""
    return _service.experiments_alerts.list_opportunities()


@router.post("/alerts", status_code=status.HTTP_201_CREATED)
async def create_alert(req: AlertCreateRequest):
    """Create customer experience alert."""
    return _service.experiments_alerts.create_alert(
        customer_id=req.customer_id,
        alert_type=req.alert_type,
        severity=req.severity,
        title=req.title,
        message=req.message,
        evidence_signals=req.evidence_signals,
        recommended_action=req.recommended_action,
    )


@router.get("/alerts")
async def list_alerts(customer_id: Optional[str] = Query(None)):
    """List experience alerts."""
    return _service.experiments_alerts.list_alerts(customer_id)


@router.get("/decisions")
async def list_experience_decisions():
    """List human-in-the-loop decision room interventions."""
    return [
        {
            "id": "dec-cx-001",
            "decision_type": "Onboarding Security Flow Optimization",
            "status": "APPROVED",
            "human_approver": "Director of Customer Success",
            "evidence_backed": True,
            "governance_checked": True,
        }
    ]


@router.get("/outcomes")
async def list_experience_outcomes():
    """List verified customer experience outcomes."""
    return [
        {
            "id": "out-cx-001",
            "customer_id": "cust-demo-001",
            "journey_stage": "onboarding",
            "metric": "time_to_first_value_days",
            "baseline": 18.0,
            "realized": 6.5,
            "verified": True,
        }
    ]


# --- Customer Journey Copilot ---
@router.post("/copilot")
async def ask_copilot(req: CopilotQueryRequest):
    """Ask Customer Journey Copilot natural language questions."""
    return _service.answer_copilot_query(query=req.query, customer_id=req.customer_id)
