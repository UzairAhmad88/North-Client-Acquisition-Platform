"""Deterministic Workflow Transitions and Failure Classification."""

from enum import Enum
from typing import Dict, Set


class FailureType(str, Enum):
    TRANSIENT = "TRANSIENT"
    PERMANENT = "PERMANENT"
    USER_ACTION_REQUIRED = "USER_ACTION_REQUIRED"
    SECURITY_BLOCKED = "SECURITY_BLOCKED"
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"


class TransitionPolicy:
    """Classifies errors to determine retryability."""

    @staticmethod
    def classify_failure(error: Exception) -> FailureType:
        error_name = type(error).__name__

        if "Permission" in error_name or "Denied" in error_name:
            return FailureType.SECURITY_BLOCKED

        if "Budget" in error_name:
            return FailureType.BUDGET_EXCEEDED

        if "Invalid" in error_name or "NotFound" in error_name or "Disabled" in error_name:
            return FailureType.PERMANENT

        if "Timeout" in error_name or "Connection" in error_name or "503" in str(error):
            return FailureType.TRANSIENT

        return FailureType.PERMANENT

    @staticmethod
    def is_retryable(failure_type: FailureType) -> bool:
        """Only transient failures may be automatically retried."""
        return failure_type == FailureType.TRANSIENT
