from typing import Optional


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        request_id: Optional[str] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(code="RESOURCE_NOT_FOUND", message=message, status_code=404)


class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(code="VALIDATION_ERROR", message=message, status_code=422)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(code="AUTH_REQUIRED", message=message, status_code=401)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(code="FORBIDDEN", message=message, status_code=403)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(code="CONFLICT", message=message, status_code=409)
