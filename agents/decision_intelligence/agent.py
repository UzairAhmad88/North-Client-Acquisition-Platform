"""Decision Intelligence AI Agent built on BaseAgent runtime."""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.decision_intelligence.explanation import ExplanationEngine
from agents.decision_intelligence.feature_context import FeatureContextEngine
from agents.decision_intelligence.policy import DecisionPolicyEngine
from agents.decision_intelligence.prediction_router import PredictionRouter


class DecisionIntelligenceAgent(BaseAgent):
    """Production Decision Intelligence & Predictive Operations AI Agent.

    Enforces the 'Rules Before AI' paradigm and point-in-time leakage defense to generate
    calibrated predictions and human decision support drafts without autonomous policy execution.
    """

    agent_id = "decision_intelligence_agent"
    name = "Decision Intelligence Agent"
    version = "1.0"
    description = (
        "Calculates probabilistic operational predictions across leads, projects, estimation, support, "
        "and client retention, enforcing deterministic rules and generating human decision support recommendations."
    )

    def __init__(self):
        super().__init__()
        self.feature_context = FeatureContextEngine()
        self.prediction_router = PredictionRouter()
        self.explanation_engine = ExplanationEngine()
        self.policy_engine = DecisionPolicyEngine()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_PREDICTIONS,
            AgentPermission.READ_MODEL_METADATA,
            AgentPermission.READ_POLICIES,
            AgentPermission.READ_PROJECTS,
            AgentPermission.READ_LEADS,
            AgentPermission.READ_SUPPORT,
            AgentPermission.READ_CLIENT_SUCCESS,
            AgentPermission.READ_ANALYTICS,
            AgentPermission.READ_METRICS,
            AgentPermission.CREATE_DECISION_SUPPORT_DRAFT,
            AgentPermission.CREATE_EXPLANATION,
            AgentPermission.CREATE_PREDICTION_DRAFT,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute predictive inference, leakage verification, or decision support formulation."""
        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        task_action = str(input_data.get("action") or "GENERATE_PREDICTION")

        if task_action == "VALIDATE_LEAKAGE":
            features = input_data.get("features") or {}
            leakage_check = self.feature_context.validate_feature_leakage(features)
            return {
                "action": "VALIDATE_LEAKAGE",
                "status": "SUCCESS",
                "validation": leakage_check,
            }

        elif task_action == "EXPLAIN_PREDICTION":
            pred_type = str(input_data.get("prediction_type") or "PROJECT_DELAY")
            prob = float(input_data.get("probability") or 0.5)
            drivers = input_data.get("drivers") or []
            exp = self.explanation_engine.format_driver_summary(pred_type, prob, drivers)
            return {
                "action": "EXPLAIN_PREDICTION",
                "status": "SUCCESS",
                "explanation": exp,
            }

        else:
            # Default GENERATE_PREDICTION workflow
            pred_type = str(input_data.get("prediction_type") or "PROJECT_DELAY").upper()
            entity_id = str(input_data.get("entity_id") or "entity_default")
            raw_features = input_data.get("features") or {}

            # Step 1: Leakage check
            leakage = self.feature_context.validate_feature_leakage(raw_features)
            if leakage.get("leakage_detected"):
                return {
                    "action": "GENERATE_PREDICTION",
                    "status": "FAILED_LEAKAGE_CHECK",
                    "reasons": leakage.get("reasons"),
                }

            # Step 2: Route prediction
            if pred_type == "LEAD_CONVERSION":
                pred = self.prediction_router.predict_lead_conversion(entity_id, raw_features)
            elif pred_type == "PROJECT_EFFORT_VARIANCE":
                pred = self.prediction_router.predict_estimation_risk(entity_id, raw_features)
            elif pred_type == "CLIENT_RETENTION":
                pred = self.prediction_router.predict_client_retention_risk(entity_id, raw_features)
            else:
                pred = self.prediction_router.predict_project_delay(entity_id, raw_features)

            # Step 3: Formulate Explanation & Decision Support (Rules Before AI)
            explanation = self.explanation_engine.format_driver_summary(
                prediction_type=pred.prediction_type,
                probability=pred.probability,
                drivers=pred.key_drivers,
            )
            decision_draft = self.policy_engine.formulate_decision_support(pred, raw_features)

            return {
                "action": "GENERATE_PREDICTION",
                "status": "SUCCESS",
                "prediction": pred.model_dump(),
                "explanation": explanation,
                "decision_support": decision_draft.model_dump(),
            }
