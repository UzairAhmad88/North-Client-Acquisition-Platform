"""Summary engine for Change Requests."""

from typing import Any, Dict
from agents.change_management.models import ChangeProposalSummary


class ChangeSummaryEngine:
    """Generates internal and client-safe change proposal summaries."""

    def summarize_change(
        self,
        change_request_id: str,
        change_number: str,
        title: str,
        description: str,
        expected_hours: float,
        change_value: float,
        currency: str = "PKR",
    ) -> ChangeProposalSummary:
        est_days = max(1, int(expected_hours / 6.0))

        exec_summary = f"Change Proposal {change_number} — {title}. Re-estimated effort: {expected_hours} hours (+{est_days} schedule days)."
        scope_delta = f"Scope Addition: {title}. {description}"
        comm_summary = f"Commercial Adjustment: +{currency} {change_value:,.2f}"

        client_summary = (
            f"Change Proposal ({change_number}): {title}\n"
            f"Summary: {description}\n"
            f"Schedule Impact: Estimated +{est_days} working days.\n"
            f"Commercial Value Adjustment: +{currency} {change_value:,.2f}"
        )

        return ChangeProposalSummary(
            change_request_id=change_request_id,
            change_number=change_number,
            title=title,
            executive_summary=exec_summary,
            scope_delta_description=scope_delta,
            estimated_schedule_impact_days=est_days,
            commercial_impact_summary=comm_summary,
            client_safe_summary=client_summary,
        )
