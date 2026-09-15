"""Business Intelligence & Organizational Learning AI Agent built on BaseAgent runtime."""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.learning.hypothesis_engine import HypothesisEngine
from agents.learning.insight_generator import InsightGeneratorEngine
from agents.learning.pattern_detector import PatternDetectorEngine
from agents.learning.semantic_layer import SemanticLayerEngine


class BusinessIntelligenceAgent(BaseAgent):
    """Business Intelligence & Organizational Learning Agent.

    Transforms historical lifecycle operations into structured evidence, insights,
    recommendations, and experiment evaluations without autonomous policy modification.
    """

    agent_id = "business_intelligence_agent"
    name = "Business Intelligence & Learning Agent"
    version = "1.0"
    description = (
        "Analyzes historical lifecycle data to discover patterns, generate evidence-backed insights, "
        "formulate continuous improvement recommendations, and evaluate experiments."
    )

    def __init__(self):
        super().__init__()
        self.pattern_detector = PatternDetectorEngine()
        self.insight_generator = InsightGeneratorEngine()
        self.hypothesis_engine = HypothesisEngine()
        self.semantic_layer = SemanticLayerEngine()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_ANALYTICS,
            AgentPermission.READ_METRICS,
            AgentPermission.READ_PROJECTS,
            AgentPermission.READ_LEADS,
            AgentPermission.READ_PROPOSALS,
            AgentPermission.READ_ESTIMATES,
            AgentPermission.READ_SUPPORT,
            AgentPermission.READ_CLIENT_SUCCESS,
            AgentPermission.READ_AI_USAGE,
            AgentPermission.CREATE_INSIGHT_DRAFT,
            AgentPermission.CREATE_RECOMMENDATION_DRAFT,
            AgentPermission.CREATE_EXPERIMENT_DRAFT,
            AgentPermission.CREATE_ANALYTICS_SUMMARY,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute BI analytics analysis, insight synthesis, experiment evaluation, or natural language query."""
        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "GENERATE_INSIGHTS")

        if task_action == "NATURAL_LANGUAGE_QUERY":
            query_str = str(input_data.get("query") or "")
            intent_meta = self.semantic_layer.resolve_query_intent(query_str)
            raw_data = input_data.get("context_data") or {}
            result = self.semantic_layer.format_semantic_response(intent_meta, raw_data)
            return {
                "action": "NATURAL_LANGUAGE_QUERY",
                "status": "SUCCESS",
                "result": result.dict(),
            }

        elif task_action == "EVALUATE_EXPERIMENT":
            exp_meta = input_data.get("experiment") or {}
            results = input_data.get("results") or []
            eval_result = self.hypothesis_engine.evaluate_experiment_results(exp_meta, results)
            return {
                "action": "EVALUATE_EXPERIMENT",
                "status": "SUCCESS",
                "evaluation": eval_result,
            }

        elif task_action == "ANALYZE_ESTIMATION_VARIANCE":
            projects = input_data.get("projects") or []
            pattern = self.pattern_detector.analyze_estimation_variance(projects)
            insight = self.insight_generator.generate_estimation_variance_insight(pattern)
            rec = self.insight_generator.create_recommendation_from_insight(insight) if insight else None
            return {
                "action": "ANALYZE_ESTIMATION_VARIANCE",
                "pattern": pattern,
                "insight": insight.dict() if insight else None,
                "recommendation": rec.dict() if rec else None,
            }

        elif task_action == "ANALYZE_LEAD_CALIBRATION":
            leads = input_data.get("leads") or []
            pattern = self.pattern_detector.analyze_lead_score_calibration(leads)
            insight = self.insight_generator.generate_lead_scoring_insight(pattern)
            rec = self.insight_generator.create_recommendation_from_insight(insight) if insight else None
            return {
                "action": "ANALYZE_LEAD_CALIBRATION",
                "pattern": pattern,
                "insight": insight.dict() if insight else None,
                "recommendation": rec.dict() if rec else None,
            }

        else:
            # Default GENERATE_INSIGHTS workflow across available input data
            generated_insights: List[Dict[str, Any]] = []
            generated_recommendations: List[Dict[str, Any]] = []

            leads = input_data.get("leads") or []
            if leads:
                lp = self.pattern_detector.analyze_lead_score_calibration(leads)
                li = self.insight_generator.generate_lead_scoring_insight(lp)
                if li:
                    generated_insights.append(li.dict())
                    generated_recommendations.append(
                        self.insight_generator.create_recommendation_from_insight(li).dict()
                    )

            projects = input_data.get("projects") or []
            if projects:
                ep = self.pattern_detector.analyze_estimation_variance(projects)
                ei = self.insight_generator.generate_estimation_variance_insight(ep)
                if ei:
                    generated_insights.append(ei.dict())
                    generated_recommendations.append(
                        self.insight_generator.create_recommendation_from_insight(ei).dict()
                    )

                rc = self.pattern_detector.analyze_requirements_scope_creep(projects)
                ri = self.insight_generator.generate_requirements_creep_insight(rc)
                if ri:
                    generated_insights.append(ri.dict())
                    generated_recommendations.append(
                        self.insight_generator.create_recommendation_from_insight(ri).dict()
                    )

            qa_items = input_data.get("qa_records") or []
            if qa_items:
                qp = self.pattern_detector.analyze_escaped_defects(qa_items)
                # QA insights can be added if valid
                if qp.get("status") == "VALID":
                    pass

            return {
                "action": "GENERATE_INSIGHTS",
                "status": "SUCCESS",
                "insights_count": len(generated_insights),
                "insights": generated_insights,
                "recommendations": generated_recommendations,
                "summary": f"Generated {len(generated_insights)} empirical insights and {len(generated_recommendations)} reviewable recommendations.",
            }
