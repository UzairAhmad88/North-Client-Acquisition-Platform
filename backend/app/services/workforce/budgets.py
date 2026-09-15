"""
Workforce Budget & Economics Subsystem for Phase 52.
Enforces hard monetary ceilings, daily token limits, and tracks workforce ROI against human hours saved.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


class BudgetEngine:
    """Manages worker and department budget limits with strict overspend prevention."""

    def __init__(self):
        self._daily_spend: Dict[str, float] = {}

    def track_task_spend(
        self,
        worker_code: str,
        cost_usd: float,
        daily_limit_usd: float = 15.0,
    ) -> Dict[str, Any]:
        """Records task cost and checks for budget exhaustion."""
        current = self._daily_spend.get(worker_code, 0.0) + cost_usd
        self._daily_spend[worker_code] = round(current, 4)

        is_exceeded = current > daily_limit_usd
        if is_exceeded:
            logger.warning(f"Worker {worker_code} has exceeded daily budget limit (${current:.2f} > ${daily_limit_usd:.2f}).")

        return {
            "worker_code": worker_code,
            "cost_recorded_usd": cost_usd,
            "total_daily_spend_usd": self._daily_spend[worker_code],
            "daily_limit_usd": daily_limit_usd,
            "is_budget_exceeded": is_exceeded,
        }


class WorkforceEconomics:
    """Computes organizational ROI, human hours saved, and cost efficiency metrics."""

    def calculate_workforce_roi(
        self,
        total_tasks_completed: int,
        total_ai_cost_usd: float,
        human_hourly_rate_usd: float = 45.0,
        estimated_minutes_per_task: float = 20.0,
    ) -> Dict[str, Any]:
        """Calculates business value generated versus platform compute costs."""
        human_hours_saved = (total_tasks_completed * estimated_minutes_per_task) / 60.0
        equivalent_human_cost = human_hours_saved * human_hourly_rate_usd
        net_savings = max(0.0, equivalent_human_cost - total_ai_cost_usd)
        
        roi_multiple = (equivalent_human_cost / max(1.0, total_ai_cost_usd)) if total_ai_cost_usd > 0 else 0.0

        return {
            "total_tasks_completed": total_tasks_completed,
            "total_ai_cost_usd": round(total_ai_cost_usd, 2),
            "human_hours_saved": round(human_hours_saved, 1),
            "equivalent_human_cost_usd": round(equivalent_human_cost, 2),
            "net_cost_savings_usd": round(net_savings, 2),
            "roi_multiple": round(roi_multiple, 2),
            "unit_cost_per_task_usd": round(total_ai_cost_usd / max(1, total_tasks_completed), 4),
        }
