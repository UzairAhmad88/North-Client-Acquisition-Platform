"""
Human Discussions, Annotations, Multi-Step Approvals, and Controlled Action Dispatch.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.decision_rooms.base import (
    ApprovalStatus,
    ActionExecutionStatus,
)


class DiscussionApprovalManager:
    """Manages discussions, annotations, multi-role approval steps, and action generation."""

    def __init__(self):
        self._discussions: Dict[str, List[Dict[str, Any]]] = {}
        self._approvals: Dict[str, List[Dict[str, Any]]] = {}
        self._actions: Dict[str, List[Dict[str, Any]]] = {}

    def add_comment(
        self,
        room_id: str,
        author_id: str,
        content: str,
        author_role: str = "HUMAN_DECISION_MAKER",
        is_human: bool = True,
        parent_id: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        annotations: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Post a discussion message or annotation."""
        comment = {
            "id": f"disc_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "author_id": author_id,
            "author_role": author_role,
            "content": content,
            "is_human": is_human,
            "parent_id": parent_id,
            "mentions": mentions or [],
            "annotations": annotations or [],
            "created_at": datetime.utcnow().isoformat(),
        }
        self._discussions.setdefault(room_id, []).append(comment)
        return comment

    def list_comments(self, room_id: str) -> List[Dict[str, Any]]:
        return self._discussions.get(room_id, [])

    # Approvals & Separation of Duties
    def configure_approval_steps(
        self,
        room_id: str,
        steps: List[Dict[str, str]],  # [{"step_name": "RISK_REVIEW", "required_role": "RISK_LEAD"}, ...]
    ) -> List[Dict[str, Any]]:
        """Set up required approval steps enforcing separation of duties."""
        created_steps = []
        for s in steps:
            step = {
                "id": f"appr_{uuid.uuid4().hex[:12]}",
                "room_id": room_id,
                "step_name": s["step_name"],
                "required_role": s["required_role"],
                "approver_id": None,
                "status": ApprovalStatus.PENDING.value,
                "decision_notes": None,
                "reviewed_at": None,
            }
            created_steps.append(step)
        self._approvals[room_id] = created_steps
        return created_steps

    def list_approvals(self, room_id: str) -> List[Dict[str, Any]]:
        return self._approvals.get(room_id, [])

    def record_approval_action(
        self,
        room_id: str,
        step_id: str,
        approver_id: str,
        status: ApprovalStatus,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record human approval or rejection on a specific gate."""
        steps = self.list_approvals(room_id)
        step = next((s for s in steps if s["id"] == step_id), None)
        if not step:
            raise ValueError(f"Approval step {step_id} not found")

        step["approver_id"] = approver_id
        step["status"] = status.value if hasattr(status, "value") else str(status)
        step["decision_notes"] = notes
        step["reviewed_at"] = datetime.utcnow().isoformat()
        return step

    # Action Dispatch
    def create_action_item(
        self,
        room_id: str,
        title: str,
        target_system: str,
        description: Optional[str] = None,
        target_payload: Optional[Dict[str, Any]] = None,
        assigned_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a controlled action item derived from an approved decision."""
        action = {
            "id": f"act_{uuid.uuid4().hex[:12]}",
            "room_id": room_id,
            "title": title,
            "description": description,
            "target_system": target_system,
            "target_payload": target_payload or {},
            "assigned_to": assigned_to,
            "execution_status": ActionExecutionStatus.PENDING_APPROVAL.value,
            "dispatched_at": None,
        }
        self._actions.setdefault(room_id, []).append(action)
        return action

    def list_actions(self, room_id: str) -> List[Dict[str, Any]]:
        return self._actions.get(room_id, [])

    def authorize_action_execution(
        self,
        room_id: str,
        action_id: str,
        authorizer_id: str,
    ) -> Dict[str, Any]:
        """Explicitly authorize action execution following approvals."""
        actions = self.list_actions(room_id)
        act = next((a for a in actions if a["id"] == action_id), None)
        if not act:
            raise ValueError(f"Action {action_id} not found")

        act["execution_status"] = ActionExecutionStatus.AUTHORIZED.value
        act["dispatched_at"] = datetime.utcnow().isoformat()
        act["authorized_by"] = authorizer_id
        return act
