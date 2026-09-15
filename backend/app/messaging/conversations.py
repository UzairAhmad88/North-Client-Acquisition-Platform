"""Messaging Engine, Thread Management, and Client Visibility Guardrails."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.communication.base import ConversationType, MessageVisibility


class MessagingManager:
    """Manages conversation threads, message versioning, and client visibility barriers."""

    @staticmethod
    def create_message(
        conversation_id: str,
        sender_id: str,
        content: str,
        visibility: MessageVisibility = MessageVisibility.INTERNAL,
        sender_type: str = "USER",
        reply_to_id: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Create a new message with explicit visibility."""
        msg_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        return {
            "id": msg_id,
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "sender_type": sender_type,
            "content": content,
            "visibility": visibility.value if hasattr(visibility, "value") else str(visibility),
            "reply_to_id": reply_to_id,
            "version": 1,
            "attachments": attachments or [],
            "created_at": now_iso,
            "edited_at": None,
            "deleted_at": None,
            "history": [
                {
                    "version": 1,
                    "content": content,
                    "edited_at": now_iso,
                }
            ],
        }

    @staticmethod
    def edit_message(
        message: Dict[str, Any], new_content: str, editor_id: str
    ) -> Dict[str, Any]:
        """Edit message and preserve previous version snapshot."""
        if message.get("deleted_at"):
            raise ValueError("Cannot edit a deleted message")

        now_iso = datetime.now(timezone.utc).isoformat()
        current_version = message.get("version", 1)
        next_version = current_version + 1

        message["content"] = new_content
        message["version"] = next_version
        message["edited_at"] = now_iso

        history = message.get("history", [])
        history.append({
            "version": next_version,
            "content": new_content,
            "edited_at": now_iso,
            "editor_id": editor_id,
        })
        message["history"] = history
        return message

    @staticmethod
    def filter_messages_for_client(
        messages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Strictly hide internal notes and restricted records from client portal users."""
        return [
            m
            for m in messages
            if m.get("visibility") == MessageVisibility.CLIENT_VISIBLE.value
            and not m.get("deleted_at")
        ]
