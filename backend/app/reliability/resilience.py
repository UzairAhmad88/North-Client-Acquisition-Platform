"""Resilience mechanisms: Bounded Exponential Retries with Jitter, Idempotency Guard, and Graceful Degradation."""

import random
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Set
import threading


class MaxRetriesExceededException(Exception):
    """Raised when an operation fails across all allocated retry attempts."""
    pass


class IdempotencyConflictException(Exception):
    """Raised when an idempotent request is already executing or completed with cached response."""
    pass


class RetryPolicy:
    """Configurable bounded retry policy with exponential backoff and randomized jitter."""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay_seconds: float = 0.5,
        max_delay_seconds: float = 10.0,
        backoff_multiplier: float = 2.0,
        enable_jitter: bool = True,
        retryable_exceptions: Optional[Set[type]] = None,
    ):
        self.max_attempts = max(1, max_attempts)
        self.initial_delay_seconds = initial_delay_seconds
        self.max_delay_seconds = max_delay_seconds
        self.backoff_multiplier = backoff_multiplier
        self.enable_jitter = enable_jitter
        self.retryable_exceptions = retryable_exceptions or {Exception}

    def compute_delay(self, attempt: int) -> float:
        """Calculates backoff delay for a given 1-indexed attempt number."""
        base_delay = self.initial_delay_seconds * (self.backoff_multiplier ** (attempt - 1))
        capped_delay = min(base_delay, self.max_delay_seconds)
        if self.enable_jitter:
            # Full jitter: uniform random between 0 and capped_delay
            return random.uniform(0, capped_delay)
        return capped_delay

    def execute(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes function with bounded retry and backoff."""
        last_exception = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                # Check if exception is retryable
                is_retryable = any(isinstance(e, exc_type) for exc_type in self.retryable_exceptions)
                if not is_retryable or attempt == self.max_attempts:
                    raise e
                
                delay = self.compute_delay(attempt)
                time.sleep(delay)

        if last_exception:
            raise last_exception
        raise MaxRetriesExceededException(f"Failed after {self.max_attempts} attempts.")


class IdempotencyGuard:
    """
    Guarantees exactly-once execution semantics for critical state-changing actions
    such as invoice issuance, payment processing, or contract commitments.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def check_and_set(self, idempotency_key: str, payload_hash: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Checks if key was already executed. If completed, returns cached result.
        If in-flight or new, marks key as in-flight.
        """
        with self._lock:
            if idempotency_key in self._cache:
                entry = self._cache[idempotency_key]
                if entry["status"] == "COMPLETED":
                    return entry["response"]
                elif entry["status"] == "IN_FLIGHT":
                    raise IdempotencyConflictException(
                        f"Request with idempotency key '{idempotency_key}' is currently in-flight."
                    )
            
            # Mark in-flight
            self._cache[idempotency_key] = {
                "status": "IN_FLIGHT",
                "payload_hash": payload_hash,
                "started_at": datetime.now(timezone.utc).isoformat(),
                "response": None,
            }
            return None

    def complete(self, idempotency_key: str, response: Any) -> None:
        """Marks idempotent operation as completed and stores response."""
        with self._lock:
            if idempotency_key in self._cache:
                self._cache[idempotency_key]["status"] = "COMPLETED"
                self._cache[idempotency_key]["response"] = response
                self._cache[idempotency_key]["completed_at"] = datetime.now(timezone.utc).isoformat()

    def clear(self, idempotency_key: str) -> None:
        """Clears an in-flight key if execution failed."""
        with self._lock:
            self._cache.pop(idempotency_key, None)


class GracefulDegradationManager:
    """
    Manages fallback execution paths when dependencies or upstream AI models are degraded,
    ensuring core operations (CRM, Project tracking, Financial recording) continue operating.
    """

    def __init__(self):
        self._degraded_features: Set[str] = set()
        self._lock = threading.Lock()

    def mark_feature_degraded(self, feature_name: str) -> None:
        with self._lock:
            self._degraded_features.add(feature_name)

    def mark_feature_restored(self, feature_name: str) -> None:
        with self._lock:
            self._degraded_features.discard(feature_name)

    def is_feature_degraded(self, feature_name: str) -> bool:
        with self._lock:
            return feature_name in self._degraded_features

    def execute_with_fallback(
        self,
        feature_name: str,
        primary_func: Callable[..., Any],
        fallback_func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if self.is_feature_degraded(feature_name):
            return fallback_func(*args, **kwargs)
        try:
            return primary_func(*args, **kwargs)
        except Exception:
            self.mark_feature_degraded(feature_name)
            return fallback_func(*args, **kwargs)
