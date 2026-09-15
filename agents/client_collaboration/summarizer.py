"""Client feedback summarizer engine."""

from typing import Any, Dict, List
from agents.client_collaboration.models import ExtractedClientActionSchema, FeedbackSummaryResult


class ClientFeedbackSummarizer:
    """Summarizes deliverable feedback and extracts action items."""

    def summarize_feedback(
        self, deliverable_id: str, deliverable_name: str, feedback_items: List[Dict[str, Any]]
    ) -> FeedbackSummaryResult:
        if not feedback_items:
            return FeedbackSummaryResult(
                deliverable_id=deliverable_id,
                deliverable_name=deliverable_name,
                overall_sentiment="POSITIVE",
                key_feedback_points=["No feedback logged for this deliverable version."],
                suggested_action_items=[],
                is_revision_requested=False,
            )

        key_points = []
        actions = []
        has_revision = False

        for item in feedback_items:
            content = str(item.get("content") or "")
            category = str(item.get("category") or "GENERAL")
            key_points.append(f"[{category}] {content}")

            if any(w in content.lower() for w in ["change", "fix", "update", "revise", "wrong", "redo"]):
                has_revision = True
                actions.append(
                    ExtractedClientActionSchema(
                        title=f"Address client feedback for {deliverable_name}",
                        description=content,
                        priority="HIGH",
                        due_in_days=3,
                    )
                )

        sentiment = "REVISION_REQUIRED" if has_revision else "POSITIVE"

        return FeedbackSummaryResult(
            deliverable_id=deliverable_id,
            deliverable_name=deliverable_name,
            overall_sentiment=sentiment,
            key_feedback_points=key_points,
            suggested_action_items=actions,
            is_revision_requested=has_revision,
        )
