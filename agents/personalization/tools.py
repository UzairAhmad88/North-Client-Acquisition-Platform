"""Sandbox tools for Personalization Agent built on Agent Core AgentTool."""

from typing import Any, Dict, Optional
from agents.core.base import AgentTool


class ReadQualificationTool(AgentTool):
    name: str = "read_qualification"
    description: str = "Reads the internal qualification assessment for a lead."
    required_permission: str = "READ_QUALIFICATION"

    async def execute(self, params: Dict[str, Any], context: Any) -> Dict[str, Any]:
        return context.metadata.get("qualification_data", {})


class ReadOutreachHistoryTool(AgentTool):
    name: str = "read_outreach_history"
    description: str = "Reads prior outreach history and drafts for a lead to avoid duplicate messaging."
    required_permission: str = "READ_LEAD"

    async def execute(self, params: Dict[str, Any], context: Any) -> Dict[str, Any]:
        return {"outreach_history": context.metadata.get("outreach_history", [])}


class CreateOutreachDraftTool(AgentTool):
    name: str = "create_outreach_draft"
    description: str = "Saves an evidence-backed outreach draft in PENDING_APPROVAL status."
    required_permission: str = "CREATE_OUTREACH_DRAFT"

    async def execute(self, params: Dict[str, Any], context: Any) -> Dict[str, Any]:
        draft_data = params.get("draft", {})
        return {
            "status": "DRAFT_CREATED",
            "approval_status": "PENDING_APPROVAL",
            "version": draft_data.get("version", 1),
            "content_hash": draft_data.get("content_hash"),
        }
