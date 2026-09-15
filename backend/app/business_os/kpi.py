"""Authoritative KPI Registry, Versioning, Freshness Monitoring & Multi-Domain Reconciliation."""

from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
import uuid

from app.business_os.base import KPICategory, KPISnapshot, ScorecardStatus


class KPIDefinition:
    """Authoritative metadata definition of a metric."""

    def __init__(
        self,
        kpi_id: str,
        name: str,
        category: KPICategory,
        description: str,
        unit: str,
        currency: str,
        source_domain: str,
        formula: str,
        target_value: Optional[Decimal] = None,
        warning_threshold: Optional[Decimal] = None,
        critical_threshold: Optional[Decimal] = None,
        freshness_max_seconds: int = 3600,
        version: str = "1.0",
        is_higher_better: bool = True,
    ):
        self.kpi_id = kpi_id
        self.name = name
        self.category = category
        self.description = description
        self.unit = unit
        self.currency = currency
        self.source_domain = source_domain
        self.formula = formula
        self.target_value = target_value
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        self.freshness_max_seconds = freshness_max_seconds
        self.version = version
        self.is_higher_better = is_higher_better


class KPIRegistry:
    """Centralized authoritative registry for all organization-wide KPIs."""

    DEFAULT_DEFINITIONS: Dict[str, KPIDefinition] = {
        # Financial
        "monthly_recurring_revenue": KPIDefinition(
            kpi_id="monthly_recurring_revenue",
            name="Monthly Recurring Revenue (MRR)",
            category=KPICategory.FINANCIAL,
            description="Sum of all active recurring subscription & retainer contracts.",
            unit="currency",
            currency="PKR",
            source_domain="Finance System",
            formula="SUM(active_subscription_amounts)",
            target_value=Decimal("5000000.00"),
            warning_threshold=Decimal("4000000.00"),
            critical_threshold=Decimal("3000000.00"),
            freshness_max_seconds=300,
            version="1.0",
        ),
        "gross_profit_margin": KPIDefinition(
            kpi_id="gross_profit_margin",
            name="Gross Profit Margin",
            category=KPICategory.FINANCIAL,
            description="Percentage of revenue retained after direct labor & provider delivery costs.",
            unit="%",
            currency="",
            source_domain="Finance System",
            formula="((Revenue - Delivery Costs) / Revenue) * 100",
            target_value=Decimal("65.00"),
            warning_threshold=Decimal("50.00"),
            critical_threshold=Decimal("40.00"),
            freshness_max_seconds=600,
            version="1.0",
        ),
        "outstanding_accounts_receivable": KPIDefinition(
            kpi_id="outstanding_accounts_receivable",
            name="Outstanding Accounts Receivable",
            category=KPICategory.FINANCIAL,
            description="Total unpaid approved client invoices past issue date.",
            unit="currency",
            currency="PKR",
            source_domain="Finance System",
            formula="SUM(unpaid_invoices_balance)",
            target_value=Decimal("500000.00"),
            warning_threshold=Decimal("1500000.00"),
            critical_threshold=Decimal("3000000.00"),
            freshness_max_seconds=300,
            version="1.0",
            is_higher_better=False,
        ),
        # Sales
        "pipeline_weighted_value": KPIDefinition(
            kpi_id="pipeline_weighted_value",
            name="Weighted Sales Pipeline Value",
            category=KPICategory.SALES,
            description="Sum of active qualified opportunities multiplied by win probability.",
            unit="currency",
            currency="PKR",
            source_domain="CRM / Sales",
            formula="SUM(opportunity_value * win_probability)",
            target_value=Decimal("12000000.00"),
            warning_threshold=Decimal("8000000.00"),
            critical_threshold=Decimal("5000000.00"),
            freshness_max_seconds=900,
            version="1.0",
        ),
        "lead_conversion_rate": KPIDefinition(
            kpi_id="lead_conversion_rate",
            name="Lead-to-Opportunity Conversion Rate",
            category=KPICategory.SALES,
            description="Percentage of qualified leads progressing to proposal/contract stages.",
            unit="%",
            currency="",
            source_domain="CRM / Sales",
            formula="(converted_leads / total_qualified_leads) * 100",
            target_value=Decimal("30.00"),
            warning_threshold=Decimal("20.00"),
            critical_threshold=Decimal("15.00"),
            freshness_max_seconds=1800,
            version="1.0",
        ),
        # Client / Customer Success
        "active_client_retention_rate": KPIDefinition(
            kpi_id="active_client_retention_rate",
            name="Net Client Retention Rate",
            category=KPICategory.CLIENT,
            description="Percentage of recurring clients renewing or expanding contracts.",
            unit="%",
            currency="",
            source_domain="Customer Success",
            formula="(renewed_and_expanding_clients / total_due_clients) * 100",
            target_value=Decimal("95.00"),
            warning_threshold=Decimal("85.00"),
            critical_threshold=Decimal("75.00"),
            freshness_max_seconds=1800,
            version="1.0",
        ),
        "portfolio_average_client_health": KPIDefinition(
            kpi_id="portfolio_average_client_health",
            name="Average Client Relationship Health Score",
            category=KPICategory.CLIENT,
            description="Mean composite health score across all active client accounts.",
            unit="score",
            currency="",
            source_domain="Customer Success",
            formula="AVG(client_composite_health_scores)",
            target_value=Decimal("80.00"),
            warning_threshold=Decimal("65.00"),
            critical_threshold=Decimal("50.00"),
            freshness_max_seconds=1200,
            version="1.0",
        ),
        # Delivery / Projects
        "on_time_milestone_delivery_rate": KPIDefinition(
            kpi_id="on_time_milestone_delivery_rate",
            name="On-Time Milestone Delivery Rate",
            category=KPICategory.DELIVERY,
            description="Percentage of project deliverables completed on or before baseline deadline.",
            unit="%",
            currency="",
            source_domain="Project Delivery",
            formula="(milestones_delivered_on_time / total_milestones) * 100",
            target_value=Decimal("90.00"),
            warning_threshold=Decimal("80.00"),
            critical_threshold=Decimal("70.00"),
            freshness_max_seconds=600,
            version="1.0",
        ),
        "engineering_capacity_utilization": KPIDefinition(
            kpi_id="engineering_capacity_utilization",
            name="Team Capacity Utilization Rate",
            category=KPICategory.DELIVERY,
            description="Committed project hours divided by total available engineering capacity.",
            unit="%",
            currency="",
            source_domain="Resource & Capacity Platform",
            formula="(committed_task_hours / available_capacity_hours) * 100",
            target_value=Decimal("80.00"),
            warning_threshold=Decimal("95.00"),
            critical_threshold=Decimal("110.00"),
            freshness_max_seconds=900,
            version="1.0",
            is_higher_better=False,
        ),
        # Support
        "support_sla_resolution_compliance": KPIDefinition(
            kpi_id="support_sla_resolution_compliance",
            name="Support SLA Resolution Compliance",
            category=KPICategory.SUPPORT,
            description="Percentage of customer support tickets resolved within warranty/maintenance SLAs.",
            unit="%",
            currency="",
            source_domain="Support System",
            formula="(tickets_resolved_within_sla / total_tickets) * 100",
            target_value=Decimal("98.00"),
            warning_threshold=Decimal("92.00"),
            critical_threshold=Decimal("85.00"),
            freshness_max_seconds=600,
            version="1.0",
        ),
        # AI & Automation
        "ai_autonomous_task_success_rate": KPIDefinition(
            kpi_id="ai_autonomous_task_success_rate",
            name="AI Agent Task Success Rate",
            category=KPICategory.AI,
            description="Percentage of AI agent runs completed without error, guardrail blocks, or retries.",
            unit="%",
            currency="",
            source_domain="AI Governance & Observability",
            formula="(successful_agent_runs / total_agent_runs) * 100",
            target_value=Decimal("99.00"),
            warning_threshold=Decimal("95.00"),
            critical_threshold=Decimal("90.00"),
            freshness_max_seconds=300,
            version="1.0",
        ),
        "monthly_ai_operating_cost": KPIDefinition(
            kpi_id="monthly_ai_operating_cost",
            name="Monthly AI & LLM Inference Cost",
            category=KPICategory.AI,
            description="Total cumulative spend across model router inference APIs.",
            unit="currency",
            currency="PKR",
            source_domain="AI Governance / Finance",
            formula="SUM(ai_token_usage_costs)",
            target_value=Decimal("200000.00"),
            warning_threshold=Decimal("350000.00"),
            critical_threshold=Decimal("500000.00"),
            freshness_max_seconds=300,
            version="1.0",
            is_higher_better=False,
        ),
        # Operations
        "platform_availability_uptime": KPIDefinition(
            kpi_id="platform_availability_uptime",
            name="Core Platform Availability Uptime",
            category=KPICategory.OPERATIONS,
            description="30-day rolling core service uptime percentage.",
            unit="%",
            currency="",
            source_domain="SRE & Reliability Platform",
            formula="(good_http_requests / total_http_requests) * 100",
            target_value=Decimal("99.90"),
            warning_threshold=Decimal("99.50"),
            critical_threshold=Decimal("99.00"),
            freshness_max_seconds=60,
            version="1.0",
        ),
    }

    def __init__(self):
        self._definitions: Dict[str, KPIDefinition] = dict(self.DEFAULT_DEFINITIONS)

    def register_or_update(self, definition: KPIDefinition) -> None:
        self._definitions[definition.kpi_id] = definition

    def get_definition(self, kpi_id: str) -> Optional[KPIDefinition]:
        return self._definitions.get(kpi_id)

    def list_definitions(self, category: Optional[KPICategory] = None) -> List[KPIDefinition]:
        if category:
            return [d for d in self._definitions.values() if d.category == category]
        return list(self._definitions.values())

    def calculate_snapshot(
        self,
        kpi_id: str,
        current_value: Decimal,
        previous_value: Optional[Decimal] = None,
        freshness_seconds: int = 60,
    ) -> KPISnapshot:
        defn = self.get_definition(kpi_id)
        if not defn:
            raise KeyError(f"KPI definition '{kpi_id}' is not registered.")

        target = defn.target_value
        variance = (current_value - target) if target is not None else None
        variance_pct = (
            ((variance / target) * Decimal("100.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if target and target > Decimal("0.00")
            else None
        )

        # Status evaluation
        status = ScorecardStatus.ON_TRACK
        if defn.is_higher_better:
            if target is not None and current_value >= target:
                status = ScorecardStatus.EXCEEDING
            elif defn.critical_threshold is not None and current_value < defn.critical_threshold:
                status = ScorecardStatus.OFF_TRACK
            elif defn.warning_threshold is not None and current_value < defn.warning_threshold:
                status = ScorecardStatus.AT_RISK
            else:
                status = ScorecardStatus.ON_TRACK
        else:
            # Lower is better (e.g. costs, AR, utilization overload)
            if target is not None and current_value <= target:
                status = ScorecardStatus.EXCEEDING
            elif defn.critical_threshold is not None and current_value >= defn.critical_threshold:
                status = ScorecardStatus.OFF_TRACK
            elif defn.warning_threshold is not None and current_value >= defn.warning_threshold:
                status = ScorecardStatus.AT_RISK
            else:
                status = ScorecardStatus.ON_TRACK

        is_stale = freshness_seconds > defn.freshness_max_seconds

        return KPISnapshot(
            kpi_id=defn.kpi_id,
            name=defn.name,
            category=defn.category,
            value=current_value,
            previous_value=previous_value,
            target_value=target,
            variance=variance,
            variance_pct=variance_pct,
            unit=defn.unit,
            currency=defn.currency,
            source_domain=defn.source_domain,
            version=defn.version,
            freshness_seconds=freshness_seconds,
            is_stale=is_stale,
            status=status,
        )

    def reconcile_cross_domain_metrics(
        self,
        finance_revenue: Decimal,
        crm_closed_won_revenue: Decimal,
        active_contracts_count: int,
        active_billing_profiles_count: int,
    ) -> List[Dict[str, Any]]:
        """
        Detects data consistency discrepancies between decoupled operational domains.
        Raises reconciliation warnings rather than silently picking convenient numbers.
        """
        discrepancies: List[Dict[str, Any]] = []

        # Check Revenue Alignment (e.g. Invoiced ledger vs CRM Deal closing)
        rev_delta = abs(finance_revenue - crm_closed_won_revenue)
        if rev_delta > Decimal("100.00"):
            discrepancies.append({
                "discrepancy_type": "REVENUE_MISALIGNMENT",
                "status": "RECONCILIATION_REQUIRED",
                "domain_a": "Finance Invoiced Ledger",
                "value_a": str(finance_revenue),
                "domain_b": "CRM Closed-Won Opportunities",
                "value_b": str(crm_closed_won_revenue),
                "variance": str(rev_delta),
                "severity": "HIGH",
                "recommendation": "Review pending invoice drafts or milestone signoffs for recently closed CRM contracts.",
            })

        # Check Active Accounts vs Billing Profiles
        if active_contracts_count != active_billing_profiles_count:
            discrepancies.append({
                "discrepancy_type": "BILLING_PROFILE_DISPARITY",
                "status": "RECONCILIATION_REQUIRED",
                "domain_a": "Active Contract Baselines",
                "value_a": str(active_contracts_count),
                "domain_b": "Active Billing Profiles",
                "value_b": str(active_billing_profiles_count),
                "variance": str(abs(active_contracts_count - active_billing_profiles_count)),
                "severity": "MEDIUM",
                "recommendation": "Ensure newly signed contracts have configured billing schedules and tax profiles.",
            })

        return discrepancies
