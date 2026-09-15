"""Natural-Language Command Parser turning text instructions into structured Command Objects."""

import re
import uuid
from typing import Any, Dict, Optional

from app.command.base import (
    CommandCategory,
    CommandExecutionStatus,
    CommandObject,
    CommandRiskLevel,
)
from app.command.registry import CommandRegistry, global_command_registry


class CommandParser:
    """Parses natural-language commands and matches them against registered commands."""

    def __init__(self, registry: Optional[CommandRegistry] = None):
        self.registry = registry or global_command_registry

    def parse(self, text: str) -> Optional[CommandObject]:
        """Convert natural language into a structured CommandObject."""
        clean = (text or "").strip().lower()
        if not clean:
            return None

        # 1. Navigation matches
        if clean in ("go to leads", "open leads", "show leads", "leads"):
            cmd = self.registry.get("NAV_LEADS")
            if cmd:
                return self._build_object(cmd, {"url": "/leads"})

        if clean in ("go to projects", "open projects", "show projects", "projects"):
            cmd = self.registry.get("NAV_PROJECTS")
            if cmd:
                return self._build_object(cmd, {"url": "/projects"})

        if clean in ("open inbox", "go to inbox", "inbox", "show notifications"):
            cmd = self.registry.get("NAV_INBOX")
            if cmd:
                return self._build_object(cmd, {"url": "/inbox"})

        if clean in ("open approvals", "go to approvals", "pending approvals", "approvals"):
            cmd = self.registry.get("NAV_APPROVALS")
            if cmd:
                return self._build_object(cmd, {"url": "/approvals"})

        # 2. Query matches
        if "qualified leads" in clean or "leads with high potential" in clean:
            cmd = self.registry.get("QUERY_LEADS")
            if cmd:
                return self._build_object(cmd, {"status": "QUALIFIED"})

        if "projects at risk" in clean or "at risk projects" in clean or "delayed projects" in clean:
            cmd = self.registry.get("QUERY_PROJECTS_AT_RISK")
            if cmd:
                return self._build_object(cmd, {"status": "AT_RISK"})

        # 3. Create Task matches (e.g. "create task prepare homepage for project proj-101")
        task_match = re.search(r"create task\s+(.+?)(?:\s+for project\s+(.+))?$", clean, re.IGNORECASE)
        if task_match:
            cmd = self.registry.get("CREATE_TASK")
            if cmd:
                title = task_match.group(1).strip()
                proj = (task_match.group(2) or "default_project").strip()
                return self._build_object(cmd, {"title": title, "project_id": proj})

        # 4. Sensitive Action matches (e.g. "send proposal prop-101 to client usr-55")
        prop_match = re.search(r"send proposal\s+([^\s]+)(?:\s+to client\s+([^\s]+))?", clean, re.IGNORECASE)
        if prop_match:
            cmd = self.registry.get("SEND_PROPOSAL")
            if cmd:
                prop_id = prop_match.group(1).strip()
                client_id = (prop_match.group(2) or "client_target").strip()
                return self._build_object(cmd, {"proposal_id": prop_id, "recipient_id": client_id})

        # 5. Approve Contract matches (e.g. "approve contract ctr-202")
        contract_match = re.search(r"approve contract\s+([^\s]+)", clean, re.IGNORECASE)
        if contract_match:
            cmd = self.registry.get("APPROVE_CONTRACT")
            if cmd:
                ctr_id = contract_match.group(1).strip()
                return self._build_object(cmd, {"contract_id": ctr_id})

        return None

    def _build_object(self, defn, parameters: Dict[str, Any]) -> CommandObject:
        return CommandObject(
            request_id=str(uuid.uuid4()),
            command_id=defn.command_id,
            category=defn.category,
            risk_level=defn.risk_level,
            parameters=parameters,
            requires_confirmation=defn.requires_confirmation,
            requires_approval=defn.requires_approval,
            status=(
                CommandExecutionStatus.APPROVAL_REQUIRED
                if defn.requires_approval
                else (
                    CommandExecutionStatus.CONFIRMATION_REQUIRED
                    if defn.requires_confirmation
                    else CommandExecutionStatus.VALIDATED
                )
            ),
        )
