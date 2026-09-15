"""Idempotency and concurrency lock manager preventing duplicate provider calls."""

import uuid
from typing import Set, Tuple

# In-memory send lock set for process synchronization
_ACTIVE_SEND_LOCKS: Set[str] = set()


class IdempotencyManager:
    """Manages send locks and idempotency keys to eliminate race conditions."""

    @staticmethod
    def get_idempotency_key(outreach_id: uuid.UUID, version: int) -> str:
        return f"outreach:{outreach_id}:send:{version}"

    @staticmethod
    def acquire_lock(key: str) -> Tuple[bool, str]:
        """Attempt to acquire a send lock for the given idempotency key."""
        if key in _ACTIVE_SEND_LOCKS:
            return False, f"Concurrency lock conflict: Send operation already in progress for key '{key}'."
        _ACTIVE_SEND_LOCKS.add(key)
        return True, ""

    @staticmethod
    def release_lock(key: str) -> None:
        """Release the send lock after operation completion."""
        _ACTIVE_SEND_LOCKS.discard(key)
