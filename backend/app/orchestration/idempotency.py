"""Idempotency key generation and verification engine for Phase 34."""

import hashlib
from typing import Any, Dict, Optional


class IdempotencyEngine:
    """Generates and verifies deterministic idempotency keys for workflow steps and task attempts."""

    @staticmethod
    def generate_key(workflow_id: str, step_key: str, attempt_group: int = 1, extra_payload: Optional[Dict[str, Any]] = None) -> str:
        """Generate a deterministic SHA-256 idempotency key."""
        base_str = f"{workflow_id}:{step_key}:{attempt_group}"
        if extra_payload:
            import json
            serialized = json.dumps(extra_payload, sort_keys=True, default=str)
            base_str += f":{serialized}"
        return hashlib.sha256(base_str.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_action_hash(content: str, expected_hash: str) -> bool:
        """Verify content SHA-256 against an approved authorization hash."""
        calculated = hashlib.sha256(content.strip().encode("utf-8")).hexdigest()
        return calculated == expected_hash
