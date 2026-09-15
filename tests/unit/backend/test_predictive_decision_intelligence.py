"""Unit and Integration Tests for Phase 32: Advanced AI/ML Decision Intelligence & Predictive Operations."""

from datetime import datetime
import pytest
from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import (
    AgentPermission,
    PROHIBITED_PERMISSIONS,
    validate_agent_permissions,
)
from agents.decision_intelligence.agent import DecisionIntelligenceAgent
from agents.decision_intelligence.feature_context import FeatureContextEngine
from agents.decision_intelligence.prediction_router import PredictionRouter
from agents.decision_intelligence.explanation import ExplanationEngine
from agents.decision_intelligence.policy import DecisionPolicyEngine
from agents.decision_intelligence.models import PredictionDraft, DecisionSupportDraft
from app.models.predictive import (
    PredictionType,
    RiskBand,
    DecisionState,
    DriftStatus,
    ModelLifecycleStatus,
)


# =============================================================================
# 1. Point-in-Time Data Leakage Defense Tests
# =============================================================================

def test_feature_validator_detects_target_leakage():
    """Verify that forbidden post-hoc outcome keywords are flagged as data leakage."""
    engine = FeatureContextEngine()
    features = {
        "budget": 50000.0,
        "lead_channel": "outbound",
        "final_invoice_amount": 55000.0,  # Post-hoc leakage!
        "realized_margin": 0.25,           # Post-hoc leakage!
    }

    res = engine.validate_feature_leakage(features)
    assert res["leakage_detected"] is True
    assert res["is_valid"] is False
    assert len(res["reasons"]) >= 2
    assert any("final_invoice_amount" in r for r in res["reasons"])
    assert any("realized_margin" in r for r in res["reasons"])


def test_feature_validator_detects_future_timestamp():
    """Verify that feature observation timestamps after inference cutoff timestamp are flagged."""
    engine = FeatureContextEngine()
    cutoff = datetime(2026, 6, 1, 12, 0, 0)
    future_features = {
        "lead_score": 85.0,
        "last_contact_date": "2026-06-15T00:00:00",  # Future relative to cutoff!
    }

    res = engine.validate_feature_leakage(future_features, inference_timestamp=cutoff)
    assert res["leakage_detected"] is True
    assert any("future timestamp" in r.lower() for r in res["reasons"])


def test_feature_validator_assembles_clean_vector():
    """Verify clean feature snapshot strips private keys and packages FeatureVector."""
    engine = FeatureContextEngine()
    raw_data = {
        "_internal_hash": "xyz123",
        "lead_score": 85.0,
        "industry": "Healthcare",
        "tech_stack_count": 4,
    }

    vector = engine.assemble_feature_vector("lead_123", raw_data)
    assert vector.entity_id == "lead_123"
    assert "_internal_hash" not in vector.feature_snapshot
    assert vector.feature_snapshot["lead_score"] == 85.0
    assert vector.feature_snapshot["industry"] == "Healthcare"


# =============================================================================
# 2. Prediction Router Tests
# =============================================================================

def test_prediction_router_lead_conversion_calibrated():
    """Verify lead conversion probability calculation and uncertainty intervals."""
    router = PredictionRouter()
    features = {
        "lead_score": 90.0,
        "service_fit_score": 80.0,
        "has_response": True,
        "interaction_count": 3,
    }

    pred = router.predict_lead_conversion("lead_99", features)
    assert pred.prediction_type == "LEAD_CONVERSION"
    assert pred.entity_id == "lead_99"
    assert pred.probability >= 0.70
    assert pred.risk_band == "HIGH"
    assert pred.confidence_interval["lower"] <= pred.probability <= pred.confidence_interval["upper"]
    assert len(pred.key_drivers) > 0
    assert "Probabilistic baseline estimate" in pred.safety_notes[0]


def test_prediction_router_project_delay():
    """Verify project delay risk estimation with variance factors."""
    router = PredictionRouter()
    features = {
        "blocked_tasks_count": 3,
        "unresolved_requirements_count": 2,
        "active_scope_changes_count": 2,
    }

    pred = router.predict_project_delay("proj_101", features)
    assert pred.prediction_type == "PROJECT_DELAY"
    assert pred.entity_id == "proj_101"
    assert pred.probability >= 0.60
    assert pred.risk_band in ("HIGH", "CRITICAL")
    assert pred.confidence_interval["lower"] <= pred.probability


def test_prediction_router_client_retention():
    """Verify client retention prediction based on support tickets and feedback."""
    router = PredictionRouter()
    features = {
        "support_reopens_count": 3,
        "unresolved_incidents_count": 2,
        "days_since_last_activity": 70,
        "has_active_maintenance": False,
    }

    pred = router.predict_client_retention_risk("client_50", features)
    assert pred.prediction_type == "CLIENT_RETENTION"
    assert pred.probability >= 0.70
    assert pred.risk_band == "HIGH"


# =============================================================================
# 3. Explanation & Driver Sanitization Tests
# =============================================================================

def test_explanation_engine_ranks_drivers():
    """Verify driver summary ranks feature impact by magnitude and formats explanation."""
    engine = ExplanationEngine()
    drivers = [
        {"feature": "budget_fit", "value": 100, "impact": "+0.10"},
        {"feature": "lead_score", "value": 95, "impact": "+0.45"},
        {"feature": "client_response", "value": True, "impact": "+0.15"},
    ]

    summary = engine.format_driver_summary("LEAD_CONVERSION", 0.85, drivers)
    assert "summary_text" in summary
    assert "lead_score" in summary["ranked_drivers"][0]["feature"]
    assert "safety_disclaimer" in summary


def test_explanation_engine_sanitizes_speculative_certainty():
    """Verify explanation generator removes speculative words like 'definitely', 'guaranteed'."""
    engine = ExplanationEngine()
    raw_text = "The client will definitely sign because guaranteed high lead score is 100% sure to convert."
    sanitized = engine.sanitize_explanation_text(raw_text)
    assert "definitely" not in sanitized.lower()
    assert "guaranteed" not in sanitized.lower()
    assert "100% sure" not in sanitized.lower()
    assert "probabilistically estimated to" in sanitized


# =============================================================================
# 4. Deterministic Policy Override Tests (Rules Before AI)
# =============================================================================

def test_policy_override_critical_defect_blocks_release():
    """Verify active critical defect strictly overrides model predictions for release approvals."""
    engine = DecisionPolicyEngine()
    rule = engine.evaluate_deterministic_rules("PROJECT_DELAY", {"open_critical_defects_count": 2})

    assert rule is not None
    assert rule["rule_key"] == "CRITICAL_DEFECT_RELEASE_BLOCK"
    assert rule["action"] == "BLOCK_RELEASE"
    assert "strictly blocked regardless of model predictions" in rule["reason"]


def test_policy_override_dnc_registered_blocks_outreach():
    """Verify DNC registration strictly blocks outreach regardless of lead score."""
    engine = DecisionPolicyEngine()
    rule = engine.evaluate_deterministic_rules("LEAD_CONVERSION", {"dnc_registered": True})

    assert rule is not None
    assert rule["rule_key"] == "DNC_REGISTRY_BLOCK"
    assert rule["action"] == "BLOCK_COMMUNICATION"


def test_policy_no_override_when_rules_pass():
    """Verify no override occurs when entity passes deterministic constraints."""
    engine = DecisionPolicyEngine()
    rule = engine.evaluate_deterministic_rules("LEAD_CONVERSION", {"dnc_registered": False, "is_opted_out": False})
    assert rule is None


def test_policy_formulate_decision_support_override():
    """Verify decision support draft reflects deterministic override when rule fires."""
    policy_engine = DecisionPolicyEngine()
    router = PredictionRouter()
    pred = router.predict_project_delay("proj_1", {"blocked_tasks_count": 1})

    decision_draft = policy_engine.formulate_decision_support(
        prediction=pred,
        entity_context={"open_critical_defects_count": 1, "action_context": "RELEASE_APPROVAL"},
    )

    assert decision_draft.urgency == "CRITICAL"
    assert "Deterministic Rule Triggered" in decision_draft.title
    assert "Mandatory Action: BLOCK_RELEASE" in decision_draft.recommended_action
    assert decision_draft.deterministic_override_applied is True


# =============================================================================
# 5. Agent Permissions & Decision Intelligence Agent Tests
# =============================================================================

def test_decision_intelligence_agent_permissions_enforced():
    """Verify DecisionIntelligenceAgent has read/draft permissions and lacks execution permissions."""
    agent = DecisionIntelligenceAgent()
    permissions = agent.get_required_permissions()

    assert AgentPermission.READ_PREDICTIONS in permissions
    assert AgentPermission.CREATE_DECISION_SUPPORT_DRAFT in permissions
    assert AgentPermission.READ_POLICIES in permissions

    # Strictly forbidden permissions in guard system
    assert "CHANGE_POLICY" in PROHIBITED_PERMISSIONS
    assert "CHANGE_MODEL" in PROHIBITED_PERMISSIONS
    assert "APPROVE_PROJECT" in PROHIBITED_PERMISSIONS
    assert "AUTO_EXECUTE_ACTION" in PROHIBITED_PERMISSIONS
    assert "MODIFY_PREDICTION_THRESHOLD" in PROHIBITED_PERMISSIONS

    # Ensure prohibited permissions raise permission denied error
    with pytest.raises(AgentPermissionDeniedError):
        validate_agent_permissions({"CHANGE_POLICY"})


@pytest.mark.asyncio
async def test_decision_intelligence_agent_execution_flow():
    """Verify end-to-end execution of DecisionIntelligenceAgent with valid context."""
    agent = DecisionIntelligenceAgent()
    context = AgentContext(
        workflow_id="wf_test_001",
        task_id="task_test_001",
        agent_run_id="run_test_phase32_001",
        metadata={
            "action": "GENERATE_PREDICTION",
            "prediction_type": "LEAD_CONVERSION",
            "entity_id": "lead_9988",
            "features": {
                "lead_score": 88.0,
                "service_fit_score": 75.0,
                "has_response": True,
            },
            "entity_context": {
                "dnc_registered": False,
            },
        },
    )

    result = await agent.execute(context)
    assert result["status"] == "SUCCESS"
    assert "prediction" in result
    assert "explanation" in result
    assert "decision_support" in result


@pytest.mark.asyncio
async def test_decision_intelligence_agent_catches_leakage():
    """Verify agent execution fails safely if temporal leakage keywords are detected."""
    agent = DecisionIntelligenceAgent()
    context = AgentContext(
        workflow_id="wf_test_002",
        task_id="task_test_002",
        agent_run_id="run_test_phase32_002",
        metadata={
            "action": "GENERATE_PREDICTION",
            "prediction_type": "LEAD_CONVERSION",
            "entity_id": "lead_9988",
            "features": {
                "lead_score": 88.0,
                "final_invoice_amount": 45000.0,  # Temporal leakage
            },
        },
    )

    result = await agent.execute(context)
    assert result["status"] == "FAILED_LEAKAGE_CHECK"
    assert len(result["reasons"]) > 0
