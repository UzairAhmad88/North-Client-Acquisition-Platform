"""Standard Exception Hierarchy for North's Agent Runtime."""


class AgentError(Exception):
    """Base exception for all agent runtime errors."""

    def __init__(self, message: str, code: str = "AGENT_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class AgentNotFoundError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_NOT_FOUND")


class AgentDisabledError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_DISABLED")


class AgentPermissionDeniedError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_PERMISSION_DENIED")


class AgentContextInvalidError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_CONTEXT_INVALID")


class AgentStateInvalidError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_STATE_INVALID")


class AgentBudgetExceededError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_BUDGET_EXCEEDED")


class AgentToolNotAllowedError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_TOOL_NOT_ALLOWED")


class AgentToolFailedError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_TOOL_FAILED")


class AgentOutputInvalidError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_OUTPUT_INVALID")


class AgentTimeoutError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_TIMEOUT")


class AgentCancelledError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_CANCELLED")


class AgentExecutionFailedError(AgentError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="AGENT_EXECUTION_FAILED")
