"""Customer Success AI Agent for Phase 41."""

from decimal import Decimal
from typing import Any, Dict, List, Set
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.customer_success.validation import CustomerSuccessSafetyValidator
from agents.customer_success.health import CustomerSuccessHealthEvaluator
from agents.customer_success.risk import CustomerSuccessRiskDetector
from agents.customer_success.opportunity import CustomerSuccessOpportunityFinder
from agents.customer_success.recommendations import CustomerSuccessRecommendationEngine


class CustomerSuccessAgent(BaseAgent):
    """
    Production Customer Success AI Agent.
    Assists in calculating multi-factor client health, detecting risks & churn indicators,
    identifying expansion opportunities, and formulating action recommendations while strictly
    prohibited from sending autonomous client messages, changing pricing, modifying contracts,
    or altering health baseline standards.
    """

    agent_id = "customer_success_agent"
    name = "Customer Success Agent"
    version = "1.0"
    description = (
        "Provides AI-assisted client relationship intelligence, multi-factor health calculations, "
        "churn risk detection, expansion opportunity discovery, and CSM recommendations."
    )
    permissions: Set[str] = {
        "READ_CLIENT",
        "READ_CLIENT_CONTACTS",
        "READ_RENEWALS",
        "READ_GOALS",
        "CREATE_HEALTH_DRAFT",
        "CREATE_RISK_DRAFT",
        "CREATE_SUCCESS_PLAN_DRAFT",
        "CREATE_RECOMMENDATION",
    }

    def __init__(self) -> None:
        super().__init__()
        self.validator = CustomerSuccessSafetyValidator()
        self.health_evaluator = CustomerSuccessHealthEvaluator()
        self.risk_detector = CustomerSuccessRiskDetector()
        self.opportunity_finder = CustomerSuccessOpportunityFinder()
        self.recommendation_engine = CustomerSuccessRecommendationEngine()

    def get_permissions(self) -> List[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        task = context.metadata.get("task", "evaluate_health")

        # Check safety guardrails
        self.validator.validate_action(task)

        if task == "evaluate_health":
            engagement = context.metadata.get("engagement_score")
            project = context.metadata.get("project_health_score")
            support = context.metadata.get("support_satisfaction_score")
            financial = context.metadata.get("financial_health_score")
            relationship = context.metadata.get("relationship_health_score")
            goals = context.metadata.get("goal_progress_score")
            historical = context.metadata.get("historical_scores")

            result_data = self.health_evaluator.evaluate_client_health(
                engagement_score=Decimal(str(engagement)) if engagement is not None else None,
                project_health_score=Decimal(str(project)) if project is not None else None,
                support_satisfaction_score=Decimal(str(support)) if support is not None else None,
                financial_health_score=Decimal(str(financial)) if financial is not None else None,
                relationship_health_score=Decimal(str(relationship)) if relationship is not None else None,
                goal_progress_score=Decimal(str(goals)) if goals is not None else None,
                historical_scores=[Decimal(str(h)) for h in historical] if historical else None,
            )
        elif task == "detect_risks":
            health = Decimal(str(context.metadata.get("health_score", "75.00")))
            unpaid_invoices = int(context.metadata.get("unpaid_invoices_count", 0))
            days_inactive = int(context.metadata.get("days_since_last_contact", 0))
            critical_tickets = int(context.metadata.get("critical_tickets_count", 0))
            negative_sentiment = float(context.metadata.get("negative_sentiment_ratio", 0.0))
            contract_days = int(context.metadata.get("contract_days_remaining", 365))

            result_data = {
                "detected_risks": self.risk_detector.scan_for_risks(
                    health_score=health,
                    unpaid_invoices_count=unpaid_invoices,
                    days_since_last_contact=days_inactive,
                    critical_tickets_count=critical_tickets,
                    negative_sentiment_ratio=negative_sentiment,
                    contract_days_remaining=contract_days,
                )
            }
        elif task == "discover_opportunities":
            health = Decimal(str(context.metadata.get("health_score", "80.00")))
            completed_milestones = int(context.metadata.get("completed_milestones", 0))
            high_csat = int(context.metadata.get("high_csat_responses", 0))
            active_services = int(context.metadata.get("active_services_count", 1))
            goals_pct = Decimal(str(context.metadata.get("goals_completed_percentage", "0.00")))

            result_data = {
                "opportunities": self.opportunity_finder.discover_opportunities(
                    health_score=health,
                    completed_milestones=completed_milestones,
                    high_csat_responses=high_csat,
                    active_services_count=active_services,
                    goals_completed_percentage=goals_pct,
                )
            }
        elif task == "generate_recommendations":
            health = Decimal(str(context.metadata.get("health_score", "75.00")))
            days_since_qbr = int(context.metadata.get("days_since_qbr", 90))
            unmet_goals = int(context.metadata.get("unmet_goals_count", 0))
            renewal_days = int(context.metadata.get("renewal_days_remaining", 180))

            result_data = {
                "recommendations": self.recommendation_engine.generate_recommendations(
                    health_score=health,
                    days_since_qbr=days_since_qbr,
                    unmet_goals_count=unmet_goals,
                    renewal_days_remaining=renewal_days,
                )
            }
        else:
            result_data = {"error": f"Unknown task: {task}"}

        return AgentResult(
            status="completed",
            result=result_data,
            confidence="HIGH",
            metadata={
                "agent_id": self.agent_id,
                "task": task,
            },
        )

