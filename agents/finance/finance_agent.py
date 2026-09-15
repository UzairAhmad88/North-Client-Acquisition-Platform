"""Financial Intelligence AI Agent for Phase 40.
"""

from decimal import Decimal
from typing import Any, Dict, List, Set
from agents.core.base import AgentResult, BaseAgent
from agents.core.context import AgentContext
from agents.core.permissions import AgentPermission
from agents.finance.validation import FinancialSafetyValidator
from agents.finance.forecasting import FinancialForecastingEngine
from agents.finance.reconciliation import FinancialReconciliationAssistant
from agents.finance.profitability import FinancialProfitabilityAssistant


class FinanceAgent(BaseAgent):
    """
    Production Finance AI Agent.
    Assists in commercial analysis, cash flow forecasting, margin variance tracking,
    and reconciliation recommendations while strictly prohibited from executing payments,
    issuing refunds, approving invoices, applying unapproved discounts, or modifying ledgers.
    """

    agent_id = "finance_agent"
    name = "Finance Agent"
    version = "1.0"
    description = "Provides AI-assisted commercial intelligence, reconciliation matching suggestions, margin variance analysis, and cash flow forecasting."
    permissions: Set[str] = {
        "READ_FINANCIAL_RECORDS",
        "READ_INVOICES",
        "READ_PAYMENTS",
        "READ_COSTS",
        "CREATE_FINANCIAL_FORECAST_DRAFT",
        "CREATE_RECONCILIATION_SUGGESTION",
        "CREATE_INVOICE_DRAFT",
    }

    def __init__(self) -> None:
        super().__init__()
        self.validator = FinancialSafetyValidator()
        self.forecaster = FinancialForecastingEngine()
        self.reconciliation_assistant = FinancialReconciliationAssistant()
        self.profitability_assistant = FinancialProfitabilityAssistant()

    def get_permissions(self) -> List[AgentPermission]:
        return [AgentPermission(p) for p in self.permissions if p in AgentPermission.__members__]

    async def run(self, context: AgentContext) -> AgentResult:
        task = context.metadata.get("task", "profitability_analysis")
        
        # Check safety guardrails
        self.validator.validate_no_prohibited_action(task)

        if task == "reconciliation_suggestions":
            unmatched_events = context.metadata.get("unmatched_events", [])
            open_invoices = context.metadata.get("open_invoices", [])
            result_data = self.reconciliation_assistant.analyze_unmatched_transactions(
                unmatched_provider_events=unmatched_events,
                open_invoices=open_invoices,
            )
        elif task == "forecast_cash_flow":
            active_schedules = context.metadata.get("active_schedules", [])
            outstanding_invoices = context.metadata.get("outstanding_invoices", [])
            monthly_burn = Decimal(str(context.metadata.get("projected_monthly_burn", "0.00")))
            months_ahead = int(context.metadata.get("months_ahead", 3))
            result_data = self.forecaster.generate_cash_flow_forecast(
                active_schedules=active_schedules,
                outstanding_invoices=outstanding_invoices,
                projected_monthly_burn=monthly_burn,
                months_ahead=months_ahead,
            )
        elif task == "validate_baseline":
            inv_total = Decimal(str(context.metadata.get("invoice_total", "0.00")))
            milestone_amt = Decimal(str(context.metadata.get("milestone_amount", "0.00"))) if "milestone_amount" in context.metadata else None
            change_amt = Decimal(str(context.metadata.get("change_amount", "0.00"))) if "change_amount" in context.metadata else None
            result_data = self.validator.validate_invoice_baseline(
                invoice_total=inv_total,
                contract_milestone_amount=milestone_amt,
                approved_change_amounts=change_amt,
            )
        else:
            # Default: Profitability analysis
            project_id = context.metadata.get("project_id", "prj-unknown")
            contracted = Decimal(str(context.metadata.get("contracted_revenue", "0.00")))
            invoiced = Decimal(str(context.metadata.get("invoiced_revenue", "0.00")))
            collected = Decimal(str(context.metadata.get("collected_revenue", "0.00")))
            estimated_cost = Decimal(str(context.metadata.get("estimated_cost", "0.00")))
            labor_hours = Decimal(str(context.metadata.get("labor_hours_logged", "0.00")))
            labor_rate = Decimal(str(context.metadata.get("labor_hourly_cost_rate", "0.00")))
            ai_cost = Decimal(str(context.metadata.get("ai_token_cost", "0.00")))
            infra_cost = Decimal(str(context.metadata.get("infrastructure_cost", "0.00")))
            subcontractor_cost = Decimal(str(context.metadata.get("subcontractor_cost", "0.00")))
            other_expenses = Decimal(str(context.metadata.get("other_expenses", "0.00")))

            result_data = self.profitability_assistant.evaluate_project_health(
                project_id=project_id,
                contracted_revenue=contracted,
                invoiced_revenue=invoiced,
                collected_revenue=collected,
                estimated_cost=estimated_cost,
                labor_hours_logged=labor_hours,
                labor_hourly_cost_rate=labor_rate,
                ai_token_cost=ai_cost,
                infrastructure_cost=infra_cost,
                subcontractor_cost=subcontractor_cost,
                other_expenses=other_expenses,
            )

        return AgentResult(
            status="completed",
            result=result_data,
            confidence="HIGH",
            metadata={"task": task},
        )
