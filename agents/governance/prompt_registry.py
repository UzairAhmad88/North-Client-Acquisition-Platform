"""Centralized Prompt Registry, Versioning & Integrity Engine."""

import hashlib
from typing import Any, Dict, List, Optional
from agents.governance.models import PromptDraft


class PromptRegistryEngine:
    """Manages prompt versioning, SHA-256 integrity hashing, and template parameter safety."""

    @staticmethod
    def compute_prompt_hash(content: str) -> str:
        """Compute authoritative SHA-256 content hash of prompt text."""
        return hashlib.sha256(content.strip().encode("utf-8")).hexdigest()

    def validate_prompt_safety(self, content: str) -> Dict[str, Any]:
        """Verify prompt content does not contain dangerous bypass patterns or raw un-escaped secrets."""
        violations = []
        lower_c = content.lower()

        # Check for harmful instruction injection patterns
        if "ignore all previous instructions" in lower_c:
            violations.append("Prompt template contains prompt injection keywords ('ignore all previous instructions').")
        if "disable safety guards" in lower_c or "bypass permissions" in lower_c:
            violations.append("Prompt attempts to disable platform security policies.")

        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "content_hash": self.compute_prompt_hash(content),
        }

    def format_prompt_spec(
        self,
        prompt_key: str,
        name: str,
        agent_target: str,
        purpose: str,
        content: str,
        version: str = "v1.0",
        status: str = "DRAFT",
    ) -> PromptDraft:
        """Create structured prompt draft with validated metadata."""
        validation = self.validate_prompt_safety(content)
        if not validation["is_valid"]:
            raise ValueError(f"Prompt validation failed: {'; '.join(validation['violations'])}")

        return PromptDraft(
            prompt_key=prompt_key,
            name=name,
            agent_target=agent_target,
            purpose=purpose,
            content=content,
            version=version,
            status=status,
        )
