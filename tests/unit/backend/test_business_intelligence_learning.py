"""Unit and Integration Tests for Phase 31: Business Intelligence, Portfolio Analytics & Organizational Learning."""

import pytest
from agents.core.context import AgentContext
from agents.core.errors import AgentPermissionDeniedError
from agents.core.permissions import AgentPermission, validate_agent_permissions
from agents.learning.agent import BusinessIntelligenceAgent
from agents.learning.hypothesis_engine import HypothesisEngine
from agents.learning.insight_generator import InsightGeneratorEngine
from agents.learning.pattern_detector import PatternDetectorEngine
from agents.learning.semantic_layer import SemanticLayerEngine
from app.models.analytics import (
    AnalyticsMetric,
    BusinessInsight,
    BusinessRecommendation,
    Experiment,
    InsightCategory,
    InsightStatus,
    RecommendationStatus,
    ExperimentStatus,
    ConfidenceLevel,
)
from app.repositories.analytics import AnalyticsRepository
from app.services.analytics import AnalyticsService


# =============================================================================
# 1. Pattern Detection & Guardrail Tests
# =============================================================================

def test_pattern_detector_insufficient_data():
    """Verify that sample sizes below threshold return INSUFFICIENT_DATA and never fabricate metrics."""
    detector = PatternDetectorEngine()
    small_sample = [{"score": 90, "status": "WON"}, {"score": 40, "status": "LOST"}]

    res = detector.analyze_lead_score_calibration(small_sample)
    assert res["status"] == "INSUFFICIENT_DATA"
    assert res["sample_size"] == 2


def test_pattern_detector_lead_score_calibration():
    """Verify accurate calculation of lead score conversion bands and false positive/negative detection."""
    detector = PatternDetectorEngine()
    leads = [
        {"score": 95, "status": "WON"},
        {"score": 85, "status": "LOST"},  # False positive (high score but lost)
        {"score": 70, "status": "WON"},
        {"score": 65, "status": "LOST"},
        {"score": 45, "status": "WON"},   # False negative (low score but won)
        {"score": 30, "status": "LOST"},
    ]

    res = detector.analyze_lead_score_calibration(leads)
    assert res["status"] == "VALID"
    assert res["sample_size"] == 6
    assert res["false_positives"] == 1
    assert res["false_negatives"] == 1
    assert "80-100" in res["band_conversions"]
    assert res["band_conversions"]["80-100"]["conversion_rate_pct"] == 50.0


def test_pattern_detector_estimation_variance():
    """Verify calculation of PERT estimation variance and service breakdowns."""
    detector = PatternDetectorEngine()
    projects = [
        {"estimated_hours": 100.0, "actual_hours": 120.0, "service": "AI Systems"},  # +20%
        {"estimated_hours": 50.0, "actual_hours": 45.0, "service": "Websites"},      # -10%
        {"estimated_hours": 80.0, "actual_hours": 100.0, "service": "AI Systems"},   # +25%
        {"estimated_hours": 40.0, "actual_hours": 44.0, "service": "Websites"},      # +10%
        {"estimated_hours": 60.0, "actual_hours": 66.0, "service": "CRM"},           # +10%
    ]

    res = detector.analyze_estimation_variance(projects)
    assert res["status"] == "VALID"
    assert res["sample_size"] == 5
    assert res["underestimated_projects"] == 2
    assert "AI Systems" in res["service_breakdown"]
    assert res["service_breakdown"]["AI Systems"]["avg_variance_pct"] == 22.5


def test_pattern_detector_requirements_scope_creep():
    """Verify correlation detection between unresolved initial requirements and subsequent scope changes."""
    detector = PatternDetectorEngine()
    projects = [
        {"has_unresolved_requirements": True, "change_requests_count": 3},
        {"has_unresolved_requirements": True, "change_requests_count": 2},
        {"has_unresolved_requirements": True, "change_requests_count": 0},
        {"has_unresolved_requirements": False, "change_requests_count": 0},
        {"has_unresolved_requirements": False, "change_requests_count": 1},
        {"has_unresolved_requirements": False, "change_requests_count": 0},
    ]

    res = detector.analyze_requirements_scope_creep(projects)
    assert res["status"] == "VALID"
    assert res["incomplete_req_projects"] == 3
    assert res["incomplete_change_risk_pct"] == 66.67
    assert res["complete_change_risk_pct"] == 0.0


# =============================================================================
# 2. Insight & Recommendation Generation Tests
# =============================================================================

def test_insight_generator_evidence_grounding():
    """Verify that generated insights strictly attach quantitative empirical evidence."""
    detector = PatternDetectorEngine()
    generator = InsightGeneratorEngine()

    projects = [
        {"estimated_hours": 100.0, "actual_hours": 125.0, "service": "AI Systems"},
        {"estimated_hours": 80.0, "actual_hours": 100.0, "service": "AI Systems"},
        {"estimated_hours": 50.0, "actual_hours": 60.0, "service": "CRM"},
        {"estimated_hours": 40.0, "actual_hours": 44.0, "service": "Websites"},
        {"estimated_hours": 70.0, "actual_hours": 84.0, "service": "AI Systems"},
    ]

    pattern = detector.analyze_estimation_variance(projects)
    insight = generator.generate_estimation_variance_insight(pattern)

    assert insight is not None
    assert insight.category == "ESTIMATION"
    assert insight.sample_size == 5
    assert len(insight.evidence_items) > 0
    assert insight.evidence_items[0]["source_type"] == "ESTIMATION_VARIANCE"
    assert insight.evidence_items[0]["sample_count"] == 5

    # Recommendation from insight
    rec = generator.create_recommendation_from_insight(insight)
    assert rec.affected_workflow == "ESTIMATION"
    assert "Expected Benefit:" not in rec.recommendation  # structured field


# =============================================================================
# 3. Hypothesis & Continuous Experiment Engine Tests
# =============================================================================

def test_hypothesis_engine_evaluation_downward_metric():
    """Verify statistical evaluation of downward-improving metric (e.g. reducing scope changes)."""
    engine = HypothesisEngine()
    exp_meta = {
        "baseline_value": 3.0,  # 3 change requests per project
        "target_value": 1.0,    # Target <= 1 change request
        "sample_target": 10,
    }

    # 5 trial outcomes
    results = [
        {"observed_value": 1.0},
        {"observed_value": 0.0},
        {"observed_value": 1.0},
        {"observed_value": 1.0},
        {"observed_value": 0.0},
    ]

    res = engine.evaluate_experiment_results(exp_meta, results)
    assert res["status"] == "EVALUATED"
    assert res["sample_count"] == 5
    assert res["observed_mean"] == 0.6
    assert res["hypothesis_supported"] is True


# =============================================================================
# 4. Semantic Layer & Security Guardrail Tests
# =============================================================================

def test_semantic_query_layer_resolution():
    """Verify natural language query maps to approved metrics and prohibits arbitrary SQL execution."""
    semantic = SemanticLayerEngine()

    query1 = "Why are project estimates inaccurate and overrunning hours?"
    res1 = semantic.resolve_query_intent(query1)
    assert res1["query_key"] == "ESTIMATION_ACCURACY"

    query2 = "Which services converted best this quarter?"
    res2 = semantic.resolve_query_intent(query2)
    assert res2["query_key"] == "SALES_CONVERSION"
    assert res2["extracted_parameters"]["time_window"] == "90d"


def test_prohibited_permissions_block_autonomous_policy_changes():
    """Verify agent runtime strictly blocks autonomous policy, pricing, scoring weight, or model deploy changes."""
    prohibited_set = {
        "CHANGE_PRICING",
        "CHANGE_SCORING_WEIGHTS",
        "DEPLOY_MODEL",
        "EXECUTE_ARBITRARY_SQL",
    }
    for perm in prohibited_set:
        with pytest.raises(AgentPermissionDeniedError):
            validate_agent_permissions({perm})


# =============================================================================
# 5. Business Intelligence Agent Execution Tests
# =============================================================================

@pytest.mark.asyncio
async def test_bi_agent_execute_workflow():
    """Verify BusinessIntelligenceAgent runs analysis and outputs structured recommendations."""
    agent = BusinessIntelligenceAgent()
    context = AgentContext(
        workflow_id="wf_bi_test",
        task_id="t_bi_1",
        agent_run_id="run_bi_1",
        metadata={
            "parameters": {
                "action": "GENERATE_INSIGHTS",
                "projects": [
                    {"estimated_hours": 100.0, "actual_hours": 120.0, "service": "AI Systems", "has_unresolved_requirements": True, "change_requests_count": 3},
                    {"estimated_hours": 50.0, "actual_hours": 45.0, "service": "Websites", "has_unresolved_requirements": False, "change_requests_count": 0},
                    {"estimated_hours": 80.0, "actual_hours": 100.0, "service": "AI Systems", "has_unresolved_requirements": True, "change_requests_count": 2},
                    {"estimated_hours": 40.0, "actual_hours": 44.0, "service": "Websites", "has_unresolved_requirements": False, "change_requests_count": 0},
                    {"estimated_hours": 60.0, "actual_hours": 66.0, "service": "CRM", "has_unresolved_requirements": False, "change_requests_count": 1},
                ],
            }
        },
    )

    res = await agent.execute(context)
    assert res["status"] == "SUCCESS"
    assert res["insights_count"] > 0
    assert len(res["recommendations"]) > 0


@pytest.mark.asyncio
async def test_bi_agent_semantic_query_action():
    """Verify BusinessIntelligenceAgent handles NATURAL_LANGUAGE_QUERY action securely."""
    agent = BusinessIntelligenceAgent()
    context = AgentContext(
        workflow_id="wf_bi_query",
        task_id="t_bi_q",
        agent_run_id="run_bi_q",
        metadata={
            "parameters": {
                "action": "NATURAL_LANGUAGE_QUERY",
                "query": "How much AI cost did lead research consume?",
                "context_data": {"total_cost": 42.60},
            }
        },
    )

    res = await agent.execute(context)
    assert res["status"] == "SUCCESS"
    assert res["result"]["query_key"] == "AI_USAGE_COSTS"
    assert "Direct SQL execution is disabled by security policy" in res["result"]["evidence_notes"]
