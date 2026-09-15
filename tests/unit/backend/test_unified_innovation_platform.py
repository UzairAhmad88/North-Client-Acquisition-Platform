import pytest
import asyncio
import math
from typing import Dict, Any

from backend.app.services.innovation.base import (
    InnovationStage,
    HorizonLevel,
    ProblemStatus,
    IdeaStatus,
    IdeaSource,
    HypothesisStatus,
    ExperimentType,
    ExperimentStatus,
    StatisticalOutcome,
    GateStage,
    GateDecision,
    PivotAction
)
from backend.app.services.innovation.service import InnovationPlatformService
from agents.core.permissions import AgentPermission, PROHIBITED_PERMISSIONS
from agents.core.context import AgentContext
from agents.innovation import (
    IdeaDiscoveryAgent,
    ProblemDiscoveryAgent,
    HypothesisAgent,
    ExperimentDesignAgent,
    ExperimentAnalysisAgent,
    ProductStrategyAgent,
    GateReviewAgent
)


@pytest.fixture
def innovation_service():
    """Returns a fresh instance of InnovationPlatformService."""
    return InnovationPlatformService()


class TestInnovationWorkspaceAndProblems:
    @pytest.mark.asyncio
    async def test_workspace_lifecycle(self, innovation_service):
        ws = await innovation_service.create_workspace(
            title="Next-Gen AI Logistics",
            objective="Autonomous route optimization and dispatch for regional fleets",
            horizon=HorizonLevel.HORIZON_2_ADJACENT,
            theme="AI Fleet Automation",
            owner="Principal Product Strategist"
        )
        assert ws.workspace_id is not None
        assert ws.stage == InnovationStage.DISCOVERY
        assert ws.horizon == HorizonLevel.HORIZON_2_ADJACENT

        retrieved = await innovation_service.get_workspace(ws.workspace_id)
        assert retrieved.title == "Next-Gen AI Logistics"

    @pytest.mark.asyncio
    async def test_problem_and_opportunity_discovery(self, innovation_service):
        # Create problem
        prob = await innovation_service.create_problem(
            workspace_id="ws-demo-001",
            statement="Dispatchers spend 4.5 hours daily manually rerouting delivery vans due to traffic bottlenecks.",
            affected_users="Mid-market 3PL logistics dispatchers",
            frequency="DAILY",
            severity=9.0,
            willingness_to_pay=850.0,
            urgency=8.5,
            existing_solutions="Manual spreadsheets and static GPS mapping"
        )
        assert prob.problem_id is not None
        assert prob.severity == 9.0
        assert prob.status == ProblemStatus.OBSERVED

        # Validate problem
        validated = await innovation_service.validate_problem(
            problem_id=prob.problem_id,
            evidence=["Interviewed 18 logistics managers confirming $12k/mo lost driver time"],
            confidence=0.88
        )
        assert validated.status == ProblemStatus.VALIDATED
        assert validated.confidence == 0.88

        # Convert to Opportunity
        opp = await innovation_service.create_opportunity(
            workspace_id="ws-demo-001",
            problem_id=validated.problem_id,
            market_size_usd=145000000.0,
            strategic_alignment=9.0,
            technical_feasibility=8.5,
            time_to_market_months=4
        )
        assert opp.opportunity_id is not None
        assert opp.market_potential == "HIGH"
        assert opp.profit_potential == "HIGH"


class TestIdeaScoringAndOriginAttribution:
    @pytest.mark.asyncio
    async def test_idea_creation_and_11_factor_scoring(self, innovation_service):
        idea = await innovation_service.create_idea(
            workspace_id="ws-demo-001",
            title="Real-Time Dynamic Dispatch AI Copilot",
            description="Autonomous dispatch copilot re-optimizing routes on telemetry anomalies.",
            problem_id="prob-001",
            source=IdeaSource.RESEARCH,
            target_users="Fleet logistics managers",
            proposed_value="Reduces route idle time by 32% with zero manual intervention",
            strategic_alignment=9.0
        )
        assert idea.idea_id is not None
        assert idea.source == IdeaSource.RESEARCH
        assert idea.status == IdeaStatus.IDEA

        # Score idea using 11 factors
        scoring_factors = {
            "customer_value": 9.5,
            "market_potential": 9.0,
            "strategic_fit": 8.5,
            "revenue_potential": 9.0,
            "profitability": 8.0,
            "differentiation": 8.5,
            "technical_feasibility": 8.0,
            "execution_complexity": 7.0,
            "risk": 7.5,
            "time_to_value": 8.0,
            "evidence_strength": 8.5
        }
        scored = await innovation_service.score_idea(idea.idea_id, scoring_factors)
        assert scored.score is not None
        assert scored.score >= 8.0
        assert scored.status == IdeaStatus.PROMISING
        # Verify formula breakdown is completely transparent
        assert scored.scoring_breakdown["customer_value_weighted"] > 0
        assert scored.scoring_breakdown["evidence_strength_weighted"] > 0


class TestHypothesesAndStatisticalExperiments:
    @pytest.mark.asyncio
    async def test_hypothesis_and_assumption_mapping(self, innovation_service):
        hypo = await innovation_service.create_hypothesis(
            workspace_id="ws-demo-001",
            idea_id="idea-001",
            statement="Dispatchers will adopt automated route overrides if prediction confidence exceeds 92%.",
            prediction="Over 65% of test fleet dispatchers accept AI route suggestions.",
            primary_metric="suggestion_acceptance_rate",
            baseline_value=0.25,
            target_value=0.65
        )
        assert hypo.hypothesis_id is not None
        assert hypo.status == HypothesisStatus.FORMULATED

        # Map assumption into 2x2 Impact vs Uncertainty matrix
        asmp = await innovation_service.create_assumption(
            workspace_id="ws-demo-001",
            hypothesis_id=hypo.hypothesis_id,
            category="CUSTOMER",
            description="Dispatchers trust algorithmic routing more than their intuition under traffic jams",
            impact_score=9.0,
            uncertainty_score=8.5
        )
        assert asmp.quadrant == "HIGH_IMPACT_HIGH_UNCERTAINTY"
        assert asmp.must_validate_first is True

    @pytest.mark.asyncio
    async def test_statistical_experiment_evaluation(self, innovation_service):
        exp = await innovation_service.create_experiment(
            workspace_id="ws-demo-001",
            hypothesis_id="hypo-001",
            title="Dispatch Acceptance Live Pilot Experiment",
            experiment_type=ExperimentType.PILOT,
            design="A/B Fleet randomized dispatching with telemetry tracking",
            primary_metric="acceptance_rate",
            control_description="Static GPS navigation",
            treatment_description="Dynamic AI rerouting suggestions",
            sample_size=100
        )
        assert exp.status == ExperimentStatus.DESIGNED

        # Record statistically significant result (p < 0.05)
        result = await innovation_service.record_experiment_result(
            experiment_id=exp.experiment_id,
            control_mean=0.28,
            treatment_mean=0.72,
            control_sample_size=60,
            treatment_sample_size=60,
            primary_metric="acceptance_rate"
        )
        assert result.outcome == StatisticalOutcome.SUPPORTED
        assert result.p_value < 0.01
        assert result.statistically_significant is True
        assert result.delta_pct > 100.0

        # Create learning from experiment
        learning = await innovation_service.generate_learning_from_experiment(
            experiment_id=exp.experiment_id,
            insight="AI route suggestions drastically exceed human acceptance baseline when traffic delay delta is displayed.",
            decision_recommendation="PROCEED to Product Concept and MVP scoping"
        )
        assert learning.learning_id is not None
        assert learning.confidence_level >= 0.85


class TestProductConceptsAndPRD:
    @pytest.mark.asyncio
    async def test_product_concept_and_prd_generation(self, innovation_service):
        concept = await innovation_service.create_product_concept(
            workspace_id="ws-demo-001",
            idea_id="idea-001",
            title="FleetPulse AI Dynamic Dispatcher",
            target_customer="Mid-market 3PL logistics fleet operators (50-500 vehicles)",
            problem_statement="High fuel costs and driver idle time from static routing",
            value_proposition="Reduces fleet idle time by 32% and saves $1,400/vehicle/mo",
            core_features=["Real-time telemetry ingestion", "Predictive congestion avoidance", "One-click driver dispatch"]
        )
        assert concept.concept_id is not None

        # Build business case and unit economics
        bcase = await innovation_service.create_business_case(
            concept_id=concept.concept_id,
            tam_usd=850000000.0,
            sam_usd=120000000.0,
            som_usd=18000000.0,
            expected_cac=4200.0,
            expected_ltv=38000.0,
            gross_margin_pct=82.0,
            break_even_months=11
        )
        assert bcase.ltv_cac_ratio > 9.0
        assert bcase.recommendation == "APPROVE"

        # Generate PRD draft
        prd = await innovation_service.generate_prd(
            concept_id=concept.concept_id,
            non_functional_requirements=["<150ms p99 route re-calculation latency", "SOC2 Type II compliance"]
        )
        assert prd.prd_id is not None
        assert len(prd.user_stories) > 0
        assert len(prd.acceptance_criteria) > 0


class TestStageGateGovernanceAndPivotEngine:
    @pytest.mark.asyncio
    async def test_stage_gate_0_to_5_evaluation(self, innovation_service):
        # Gate 1 evaluation with sufficient evidence
        gate_1 = await innovation_service.evaluate_gate(
            workspace_id="ws-demo-001",
            gate_stage=GateStage.GATE_1_PROBLEM_VALIDATION,
            checklist={
                "customer_interviews_completed": True,
                "problem_severity_validated": True,
                "willingness_to_pay_confirmed": True
            },
            reviewed_by="Head of Product & Governance Board"
        )
        assert gate_1.decision == GateDecision.PROCEED
        assert gate_1.evidence_completeness_score >= 0.85

        # Gate 4 evaluation with missing financial validation
        gate_4 = await innovation_service.evaluate_gate(
            workspace_id="ws-demo-001",
            gate_stage=GateStage.GATE_4_BUSINESS_VALIDATION,
            checklist={
                "tam_sam_som_verified": True,
                "unit_economics_positive": False,
                "regulatory_risk_cleared": False
            },
            reviewed_by="CFO Review Panel"
        )
        assert gate_4.decision == GateDecision.REVISE_EVIDENCE
        assert gate_4.evidence_completeness_score < 0.60

    @pytest.mark.asyncio
    async def test_pivot_engine_recommendations(self, innovation_service):
        pivot_eval = await innovation_service.evaluate_pivot(
            workspace_id="ws-demo-001",
            problem_id="prob-001",
            experiment_outcomes=[StatisticalOutcome.NOT_SUPPORTED, StatisticalOutcome.NOT_SUPPORTED],
            current_cac=9000.0,
            current_ltv=3000.0
        )
        assert pivot_eval["recommended_action"] in [
            PivotAction.CUSTOMER_SEGMENT_PIVOT,
            PivotAction.BUSINESS_MODEL_PIVOT,
            PivotAction.VALUE_PROPOSITION_PIVOT
        ]
        assert len(pivot_eval["suggested_adjustments"]) > 0


class TestInnovationCopilotAndZeroHallucination:
    @pytest.mark.asyncio
    async def test_copilot_grounded_queries(self, innovation_service):
        resp = await innovation_service.query_copilot(
            query="Find problems worth solving and what assumptions should we test first?",
            workspace_id="ws-demo-001"
        )
        assert resp.answer is not None
        assert len(resp.grounding_evidence) > 0
        assert len(resp.assumptions_identified) > 0
        assert len(resp.limitations) > 0
        # Check that copilot does not fabricate claims
        assert "Zero-Hallucination Grounding" in resp.answer or "Empirical" in resp.answer


class TestAgentsAndSecurityGovernance:
    def test_permission_boundaries(self):
        # Verify Phase 55 Prohibitions
        assert "AUTONOMOUS_LAUNCH_PRODUCT" in PROHIBITED_PERMISSIONS
        assert "AUTONOMOUS_PRICE_MUTATION" in PROHIBITED_PERMISSIONS
        assert "FABRICATE_EXPERIMENT_RESULTS" in PROHIBITED_PERMISSIONS
        assert AgentPermission.READ_INNOVATION.value == "READ_INNOVATION"
        assert AgentPermission.CREATE_IDEA.value == "CREATE_IDEA"

    @pytest.mark.asyncio
    async def test_innovation_agent_execution(self):
        agent = IdeaDiscoveryAgent()
        context = AgentContext(
            workflow_id="wf-idea-01",
            task_id="task-idea-01",
            agent_run_id="run-idea-01",
            metadata={
                "workspace_id": "ws-demo-001",
                "problem_statement": "Cold outreach response rates have dropped 45%",
                "target_segment": "B2B SaaS Sales Leaders"
            }
        )
        result = await agent.execute(context)
        assert result["status"] == "SUCCESS"
        assert len(result["candidate_ideas"]) > 0
        assert result["candidate_ideas"][0]["source"] == "AI_WORKER"

    @pytest.mark.asyncio
    async def test_experiment_analysis_agent(self):
        agent = ExperimentAnalysisAgent()
        context = AgentContext(
            workflow_id="wf-exp-01",
            task_id="task-exp-01",
            agent_run_id="run-exp-01",
            metadata={
                "experiment_id": "exp-001",
                "control_mean": 0.12,
                "treatment_mean": 0.28,
                "control_n": 80,
                "treatment_n": 80
            }
        )
        result = await agent.execute(context)
        assert result["status"] == "SUCCESS"
        assert result["outcome"] == "SUPPORTED"
        assert result["statistically_significant"] is True
        assert result["p_value"] < 0.05
