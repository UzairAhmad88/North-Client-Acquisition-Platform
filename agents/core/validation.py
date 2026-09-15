"""Validation utilities and prompt-injection defense layers for Agent Runtime."""

import re
from typing import Any, Dict, List, Optional, Tuple

from agents.core.errors import AgentOutputInvalidError


class AgentValidator:
    """Validator for AI outputs and untrusted external inputs."""

    @staticmethod
    def sanitize_untrusted_input(text: str) -> str:
        """Isolate external text safely in untrusted data blocks.

        Defends against prompt-injection by ensuring untrusted text cannot mimic system instructions.
        """
        if not text:
            return ""

        # Remove attempts to inject system prompt boundaries
        cleaned = re.sub(r"(?i)<\s*/?\s*system\s*>", "[REDACTED_TAG]", text)
        cleaned = re.sub(r"(?i)<\s*/?\s*instruction\s*>", "[REDACTED_TAG]", cleaned)
        cleaned = re.sub(r"(?i)ignore\s+previous\s+instructions", "[BLOCKED_PROMPT_INJECTION_ATTEMPT]", cleaned)
        cleaned = re.sub(r"(?i)ignore\s+all\s+instructions", "[BLOCKED_PROMPT_INJECTION_ATTEMPT]", cleaned)

        return f"<UNTRUSTED_EXTERNAL_DATA>\n{cleaned}\n</UNTRUSTED_EXTERNAL_DATA>"

    @staticmethod
    def validate_output_schema(
        output: Dict[str, Any],
        required_fields: List[str],
    ) -> Dict[str, Any]:
        """Verify that agent output contains expected top-level keys."""
        missing = [f for f in required_fields if f not in output]
        if missing:
            raise AgentOutputInvalidError(
                f"Agent output validation failed: Missing required fields {missing}."
            )
        return output
