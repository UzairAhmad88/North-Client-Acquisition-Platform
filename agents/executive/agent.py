"""Business OS Executive AI Agent built on BaseAgent runtime."""

from typing import Any, Dict, List, Set
from agents.core.base import BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from app.business_os.service import BusinessOSPlatformService


class BusinessOSExecutiveAgent(BaseAgent):
    """
    Executive AI Copilot & Strategic Intelligence Agent.
    Provides decision support, scenario simulation, and briefing synthesis.
    Strictly upholds the Business OS principle: AI recommends; Humans decide.
    """

    agent_id = "business_os_executive_agent"
    name = "Business OS Executive Agent"
    version = "1.0"
    description = (
        "Provides grounded executive intelligence, 10-dimension business health evaluation, "
        "decision option formulation, and What-If scenario simulations without autonomous execution."
    )

    def __init__(self):
        super().__init__()
        self.platform_service = BusinessOSPlatformService()

    def get_required_permissions(self) -> Set[AgentPermission]:
        return {
            AgentPermission.READ_EXECUTIVE_360,
            AgentPermission.READ_STRATEGY,
            AgentPermission.READ_ORGANIZATIONAL_RISKS,
            AgentPermission.READ_DECISION_QUEUE,
            AgentPermission.CREATE_DECISION_DRAFT,
            AgentPermission.CREATE_BRIEFING_DRAFT,
            AgentPermission.RUN_SCENARIO_SIMULATION,
        }

    async def execute(self, context: AgentContext) -> Dict[str, Any]:
        """Execute executive query, scenario simulation, or briefing compilation."""
        input_data = (
            context.metadata.get("parameters")
            if context.metadata and "parameters" in context.metadata
            else context.metadata or {}
        )
        action = str(input_data.get("action") or "QUERY_COPILOT")

        if action == "QUERY_COPILOT":
            query_text = str(input_data.get("query", "How is the business doing?"))
            resp = self.platform_service.query_copilot(query=query_text)
            return {
                "status": "SUCCESS",
                "query_id": resp.query_id,
                "intent": resp.intent,
                "answer_markdown": resp.answer_markdown,
                "confidence": resp.confidence,
                "evidence_sources": resp.evidence_sources,
                "suggested_followups": resp.suggested_followups,
                "action_prohibited": resp.action_prohibited,
            }

        elif action == "RUN_SCENARIO":
            scen_name = str(input_data.get("scenario_name", "What-If Price & Conversion Test"))
            res = self.platform_service.run_scenario(
                scenario_name=scen_name,
                price_change_pct=input_data.get("price_change_pct", 0.0),
                conversion_change_pct=input_data.get("conversion_change_pct", 0.0),
                client_churn_revenue=input_data.get("client_churn_revenue", 0.0),
                new_hires_count=input_data.get("new_hires_count", 0),
            )
            return {
                "status": "SUCCESS",
                "scenario_id": res.scenario_id,
                "simulated_revenue": str(res.simulated_revenue),
                "simulated_profit": str(res.simulated_profit),
                "margin_pct": str(res.simulated_margin_pct),
                "utilization_pct": str(res.capacity_utilization_pct),
                "risk_level": res.risk_level,
                "is_production_isolated": res.is_production_isolated,
            }

        elif action == "GENERATE_BRIEFING":
            brf = self.platform_service.get_briefing()
            return {
                "status": "SUCCESS",
                "briefing_id": brf.briefing_id,
                "title": brf.title,
                "summary": brf.summary_paragraph,
                "metrics": brf.key_metrics_snapshot,
            }

        elif action == "EVALUATE_HEALTH":
            health = self.platform_service.get_business_health()
            return {
                "status": "SUCCESS",
                "overall_health_score": str(health.overall_health_score),
                "overall_status": health.overall_status.value,
                "dimensions_count": len(health.dimensions),
            }

        return {
            "status": "ERROR",
            "error": f"Unknown action '{action}' requested.",
        }
