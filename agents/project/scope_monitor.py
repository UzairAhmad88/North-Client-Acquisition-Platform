"""Project scope creep and baseline monitor."""

from typing import Any, Dict, List
from agents.project.models import ScopeSignalResult


class ProjectScopeMonitor:
    """Monitors execution tasks against committed baseline deliverables to detect scope expansion signals."""

    def evaluate_scope_signals(
        self,
        baseline_items: List[Dict[str, Any]],
        current_tasks: List[Dict[str, Any]],
        recent_messages: List[Dict[str, Any]],
    ) -> List[ScopeSignalResult]:
        signals: List[ScopeSignalResult] = []

        baseline_names = {str(item.get("name") or "").lower() for item in baseline_items}

        # 1. Detect tasks not traceable to baseline
        for task in current_tasks:
            t_name = str(task.get("name") or "")
            t_desc = str(task.get("description") or "")
            deliverable_id = task.get("deliverable_id")

            if not deliverable_id and baseline_names:
                matches = any(b_name in t_name.lower() or b_name in t_desc.lower() for b_name in baseline_names)
                if not matches:
                    signals.append(
                        ScopeSignalResult(
                            signal_type="FEATURE_ADDED",
                            description=f"Task '{t_name}' does not map to any item in the committed baseline.",
                            source="TASK_ANALYSIS",
                            severity="MEDIUM",
                            recommended_action="Review task with Project Manager to issue Change Order if scope expanded.",
                        )
                    )

        # 2. Check client messages for new requests
        scope_keywords = ["add feature", "also build", "new page", "mobile app", "extra integration", "can we include"]
        for msg in recent_messages:
            content = str(msg.get("content") or "").lower()
            for kw in scope_keywords:
                if kw in content:
                    signals.append(
                        ScopeSignalResult(
                            signal_type="NEW_SCOPE_REQUEST",
                            description=f"Client requested additional scope in message: '{msg.get('content')}'",
                            source="CLIENT_COMMUNICATION",
                            severity="HIGH",
                            recommended_action="Create formal Scope Change Signal and flag for commercial review before coding.",
                        )
                    )
                    break

        return signals
