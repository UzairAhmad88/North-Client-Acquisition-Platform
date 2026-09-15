"""Service Level Objective (SLO), SLI measurement, and Error Budget tracking engine."""

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.reliability.base import ErrorBudgetStatus, SLOType


class SLOSnapshot(BaseModel):
    name: str
    slo_type: SLOType
    target_percentage: Decimal
    current_sli_percentage: Decimal
    error_budget_total_percentage: Decimal
    error_budget_consumed_percentage: Decimal
    error_budget_remaining_percentage: Decimal
    budget_status: ErrorBudgetStatus
    window_days: int = 30
    is_compliant: bool
    summary: str


class SLOEngine:
    """
    Computes Service Level Indicators (SLIs), evaluates compliance against SLO targets,
    and calculates exact remaining error budgets to govern deployment velocity.
    """

    DEFAULT_SLOS = [
        {
            "name": "API Availability",
            "slo_type": SLOType.AVAILABILITY,
            "target_percentage": Decimal("99.90"),
            "window_days": 30,
        },
        {
            "name": "Critical Workflow Completion",
            "slo_type": SLOType.COMPLETION_RATE,
            "target_percentage": Decimal("99.95"),
            "window_days": 30,
        },
        {
            "name": "Payment & Ledger Reconciliations",
            "slo_type": SLOType.AVAILABILITY,
            "target_percentage": Decimal("99.99"),
            "window_days": 30,
        },
        {
            "name": "API p95 Latency (< 500ms)",
            "slo_type": SLOType.LATENCY,
            "target_percentage": Decimal("99.00"),
            "window_days": 30,
        },
    ]

    @classmethod
    def evaluate_slo(
        cls,
        name: str,
        target_percentage: Decimal,
        total_events: int,
        good_events: int,
        slo_type: SLOType = SLOType.AVAILABILITY,
        window_days: int = 30,
    ) -> SLOSnapshot:
        if total_events <= 0:
            current_sli = Decimal("100.00")
        else:
            current_sli = (Decimal(good_events) / Decimal(total_events)) * Decimal("100.00")

        current_sli = max(Decimal("0.00"), min(Decimal("100.00"), current_sli))
        is_compliant = current_sli >= target_percentage

        # Error budget total is (100 - target)%
        total_budget = Decimal("100.00") - target_percentage
        
        # Actual failure percentage
        actual_failure_pct = Decimal("100.00") - current_sli

        if total_budget > Decimal("0.00"):
            consumed_fraction = actual_failure_pct / total_budget
            consumed_percentage = min(Decimal("100.00"), max(Decimal("0.00"), consumed_fraction * Decimal("100.00")))
            remaining_percentage = Decimal("100.00") - consumed_percentage
        else:
            consumed_percentage = Decimal("100.00") if not is_compliant else Decimal("0.00")
            remaining_percentage = Decimal("0.00") if not is_compliant else Decimal("100.00")

        if remaining_percentage >= Decimal("50.00"):
            status = ErrorBudgetStatus.HEALTHY
        elif remaining_percentage >= Decimal("20.00"):
            status = ErrorBudgetStatus.WARNING
        elif remaining_percentage > Decimal("0.00"):
            status = ErrorBudgetStatus.EXHAUSTED
        else:
            status = ErrorBudgetStatus.BREACHED

        summary = (
            f"SLO '{name}' current SLI is {current_sli:.2f}% (Target: {target_percentage:.2f}%). "
            f"Error budget remaining: {remaining_percentage:.1f}% ({status.value})."
        )

        return SLOSnapshot(
            name=name,
            slo_type=slo_type,
            target_percentage=target_percentage,
            current_sli_percentage=current_sli,
            error_budget_total_percentage=total_budget,
            error_budget_consumed_percentage=consumed_percentage,
            error_budget_remaining_percentage=remaining_percentage,
            budget_status=status,
            window_days=window_days,
            is_compliant=is_compliant,
            summary=summary,
        )
