"""
Worker Capability & Tool Access Authorization Subsystem for Phase 52.
Enforces default-deny rules, sensitive capability blocking, and tool call bounds.
"""

from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional, Set

try:
    from backend.app.services.workforce.base import (
        AIWorker,
        SensitiveCapability,
        WorkerCapability,
    )
except ImportError:
    from app.services.workforce.base import (
        AIWorker,
        SensitiveCapability,
        WorkerCapability,
    )

logger = logging.getLogger(__name__)


class CapabilityManager:
    """Evaluates whether an AI Worker is authorized to execute a requested business capability."""

    SENSITIVE_CAPABILITIES = {c.value for c in SensitiveCapability}

    def validate_capability_access(
        self,
        worker: AIWorker,
        required_capability: str,
    ) -> Dict[str, Any]:
        """Verifies capability authorization. Blocks sensitive capabilities without explicit human override."""
        if required_capability in self.SENSITIVE_CAPABILITIES:
            logger.warning(f"Sensitive capability {required_capability} requested by worker {worker.worker_code} - BLOCKED by default policy.")
            return {
                "is_authorized": False,
                "reason": f"Capability '{required_capability}' is classified as SENSITIVE. AI workers cannot execute sensitive capabilities without human ratification.",
                "requires_human_approval": True,
            }

        if required_capability not in worker.capabilities:
            return {
                "is_authorized": False,
                "reason": f"Worker {worker.worker_code} does not possess capability '{required_capability}'.",
                "requires_human_approval": False,
            }

        return {
            "is_authorized": True,
            "reason": "Capability granted under worker governance policy.",
            "requires_human_approval": False,
        }


class ToolPolicyManager:
    """Governs tool access, call limits, and resource permissions for AI workers."""

    def authorize_tool_call(
        self,
        worker: AIWorker,
        tool_name: str,
        current_calls_count: int = 0,
    ) -> Dict[str, Any]:
        """Checks if a tool can be invoked within configured bounds."""
        policy = worker.tool_policy or {}
        allowed_tools = policy.get("allowed_tools", ["retrieve_knowledge", "search_web"])
        max_calls = policy.get("max_calls_per_task", 15)

        if tool_name not in allowed_tools:
            return {
                "is_allowed": False,
                "reason": f"Tool '{tool_name}' is not in worker {worker.worker_code} allowed tools list.",
            }

        if current_calls_count >= max_calls:
            return {
                "is_allowed": False,
                "reason": f"Worker {worker.worker_code} exceeded max allowed tool calls ({max_calls}) for this task.",
            }

        return {
            "is_allowed": True,
            "reason": "Tool execution authorized.",
        }
