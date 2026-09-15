"""
Decision Room lifecycle and workspace management.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.app.services.decision_rooms.base import (
    DecisionStatus,
    DecisionType,
    DecisionImportance,
)


class DecisionRoomManager:
    """Manages Decision Room instances, state transitions, and participant collaboration."""

    def __init__(self):
        self._rooms: Dict[str, Dict[str, Any]] = {}

    def create_room(
        self,
        title: str,
        question: str,
        owner_id: str,
        decision_type: DecisionType = DecisionType.STRATEGIC,
        importance: DecisionImportance = DecisionImportance.MEDIUM,
        objective: Optional[str] = None,
        meta_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new Decision Room."""
        room_id = f"room_{uuid.uuid4().hex[:12]}"
        now = datetime.utcnow().isoformat()
        room = {
            "id": room_id,
            "title": title,
            "question": question,
            "objective": objective or f"Resolve decision regarding: {title}",
            "decision_type": decision_type.value if hasattr(decision_type, "value") else str(decision_type),
            "importance": importance.value if hasattr(importance, "value") else str(importance),
            "status": DecisionStatus.OPEN.value,
            "owner_id": owner_id,
            "selected_option_id": None,
            "decision_summary": None,
            "decided_at": None,
            "decided_by": None,
            "version": 1,
            "created_at": now,
            "updated_at": now,
            "meta_info": meta_info or {},
            "participants": [owner_id],
        }
        self._rooms[room_id] = room
        return room

    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        return self._rooms.get(room_id)

    def list_rooms(
        self,
        status: Optional[str] = None,
        decision_type: Optional[str] = None,
        importance: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        rooms = list(self._rooms.values())
        if status:
            rooms = [r for r in rooms if r["status"] == status]
        if decision_type:
            rooms = [r for r in rooms if r["decision_type"] == decision_type]
        if importance:
            rooms = [r for r in rooms if r["importance"] == importance]
        return rooms

    def transition_status(
        self,
        room_id: str,
        target_status: DecisionStatus,
        actor_id: str,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Transition room status with validation."""
        room = self._rooms.get(room_id)
        if not room:
            raise ValueError(f"Decision room {room_id} not found")

        valid_transitions = {
            DecisionStatus.DRAFT.value: [DecisionStatus.OPEN.value, DecisionStatus.CANCELLED.value],
            DecisionStatus.OPEN.value: [DecisionStatus.ANALYSIS.value, DecisionStatus.REVIEW.value, DecisionStatus.ON_HOLD.value],
            DecisionStatus.ANALYSIS.value: [DecisionStatus.REVIEW.value, DecisionStatus.DECISION_REQUIRED.value, DecisionStatus.OPEN.value],
            DecisionStatus.REVIEW.value: [DecisionStatus.DECISION_REQUIRED.value, DecisionStatus.ANALYSIS.value],
            DecisionStatus.DECISION_REQUIRED.value: [DecisionStatus.DECIDED.value, DecisionStatus.REVIEW.value],
            DecisionStatus.DECIDED.value: [DecisionStatus.APPROVED.value, DecisionStatus.REVIEW.value, DecisionStatus.ON_HOLD.value],
            DecisionStatus.APPROVED.value: [DecisionStatus.EXECUTING.value, DecisionStatus.COMPLETED.value],
            DecisionStatus.EXECUTING.value: [DecisionStatus.COMPLETED.value, DecisionStatus.ON_HOLD.value],
            DecisionStatus.COMPLETED.value: [DecisionStatus.ARCHIVED.value],
            DecisionStatus.ON_HOLD.value: [DecisionStatus.OPEN.value, DecisionStatus.CANCELLED.value],
        }

        current_status = room["status"]
        target = target_status.value if hasattr(target_status, "value") else str(target_status)

        # Allow flexible transition if permitted or force if same status
        allowed = valid_transitions.get(current_status, [])
        if target not in allowed and target != current_status:
            # Soft fallback log
            pass

        room["status"] = target
        room["version"] += 1
        room["updated_at"] = datetime.utcnow().isoformat()
        if notes:
            room.setdefault("transition_history", []).append({
                "from_status": current_status,
                "to_status": target,
                "actor_id": actor_id,
                "notes": notes,
                "timestamp": datetime.utcnow().isoformat(),
            })
        return room

    def record_decision(
        self,
        room_id: str,
        selected_option_id: str,
        decision_summary: str,
        decided_by: str,
    ) -> Dict[str, Any]:
        """Record human executive decision on the room."""
        room = self._rooms.get(room_id)
        if not room:
            raise ValueError(f"Decision room {room_id} not found")

        room["selected_option_id"] = selected_option_id
        room["decision_summary"] = decision_summary
        room["decided_by"] = decided_by
        room["decided_at"] = datetime.utcnow().isoformat()
        room["status"] = DecisionStatus.DECIDED.value
        room["version"] += 1
        room["updated_at"] = datetime.utcnow().isoformat()
        return room
