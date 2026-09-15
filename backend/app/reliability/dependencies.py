"""Dependency tracking and Circuit Breaker state machine for external/subsystem resilience."""

import time
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional
import threading

from app.reliability.base import CircuitState, DependencyStatus


class CircuitBreakerOpenException(Exception):
    """Raised when an operation is attempted on an open circuit."""
    pass


class CircuitBreaker:
    """
    Production circuit breaker implementing CLOSED -> OPEN -> HALF_OPEN states.
    Protects against cascading failures and unneeded external calls during outages.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0,
        half_open_success_threshold: int = 2,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = time.time()
        self.last_failure_time: Optional[float] = None
        self._lock = threading.Lock()

    def record_success(self) -> None:
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.half_open_success_threshold:
                    self._transition_to(CircuitState.CLOSED)
                    self.failure_count = 0
                    self.success_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0

    def record_failure(self) -> None:
        with self._lock:
            self.last_failure_time = time.time()
            if self.state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.OPEN)
                self.success_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self._transition_to(CircuitState.OPEN)

    def can_execute(self) -> bool:
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_state_change >= self.recovery_timeout_seconds:
                    self._transition_to(CircuitState.HALF_OPEN)
                    self.success_count = 0
                    return True
                return False
            if self.state == CircuitState.HALF_OPEN:
                return True
            return False

    def execute(self, func: Callable[..., Any], *args: Any, fallback: Optional[Callable[..., Any]] = None, **kwargs: Any) -> Any:
        if not self.can_execute():
            if fallback:
                return fallback(*args, **kwargs)
            raise CircuitBreakerOpenException(
                f"CircuitBreaker '{self.name}' is OPEN. Fast failing to protect system."
            )
        try:
            res = func(*args, **kwargs)
            self.record_success()
            return res
        except Exception as e:
            self.record_failure()
            if fallback:
                return fallback(*args, **kwargs)
            raise e

    def _transition_to(self, new_state: CircuitState) -> None:
        self.state = new_state
        self.last_state_change = time.time()

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "failure_threshold": self.failure_threshold,
                "recovery_timeout_seconds": self.recovery_timeout_seconds,
                "last_failure_time": self.last_failure_time,
            }


class DependencyManager:
    """Tracks registry of platform dependencies and manages associated circuit breakers."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DependencyManager, cls).__new__(cls)
                cls._instance.circuit_breakers = {}
                cls._instance.dependencies = {}
            return cls._instance

    def get_or_create_circuit_breaker(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: float = 30.0,
    ) -> CircuitBreaker:
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(
                name=name,
                failure_threshold=failure_threshold,
                recovery_timeout_seconds=recovery_timeout_seconds,
            )
        return self.circuit_breakers[name]

    def register_dependency(
        self,
        name: str,
        category: str,
        is_critical: bool = True,
        status: DependencyStatus = DependencyStatus.HEALTHY,
    ) -> None:
        self.dependencies[name] = {
            "name": name,
            "category": category,
            "is_critical": is_critical,
            "status": status.value,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def update_dependency_status(self, name: str, status: DependencyStatus) -> None:
        if name in self.dependencies:
            self.dependencies[name]["status"] = status.value
            self.dependencies[name]["updated_at"] = datetime.now(timezone.utc).isoformat()

    def list_dependencies(self) -> List[Dict[str, Any]]:
        return list(self.dependencies.values())
