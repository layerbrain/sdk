"""Exception hierarchy for the Layerbrain SDK.

Mirrors the error types returned by the Layerbrain API:
  {"error": {"type": "...", "message": "..."}}
"""

from __future__ import annotations

from typing import Optional


class LayerbrainError(Exception):
    """Base exception for all Layerbrain SDK errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class APIError(LayerbrainError):
    """An error returned by the Layerbrain API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_type: Optional[str] = None,
        body: Optional[dict] = None,
    ) -> None:
        self.status_code = status_code
        self.error_type = error_type
        self.body = body
        super().__init__(message)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(message={self.message!r}, "
            f"status_code={self.status_code}, error_type={self.error_type!r})"
        )


# ---- 4xx Client Errors ----

class ValidationError(APIError):
    """400 - Request validation failed."""

    def __init__(self, message: str = "Validation failed", **kwargs) -> None:
        super().__init__(message, status_code=400, error_type="validation_error", **kwargs)


class AuthenticationError(APIError):
    """401 - Invalid or missing authentication credentials."""

    def __init__(self, message: str = "Authentication failed", **kwargs) -> None:
        super().__init__(message, status_code=401, error_type="authentication_error", **kwargs)


class InsufficientFundsError(APIError):
    """402 - Insufficient account balance."""

    def __init__(self, message: str = "Insufficient funds", **kwargs) -> None:
        super().__init__(message, status_code=402, error_type="insufficient_funds", **kwargs)


class PermissionDeniedError(APIError):
    """403 - Insufficient permissions for the requested operation."""

    def __init__(self, message: str = "Permission denied", **kwargs) -> None:
        super().__init__(message, status_code=403, error_type="authorization_error", **kwargs)


class NotFoundError(APIError):
    """404 - The requested resource was not found."""

    def __init__(self, message: str = "Resource not found", **kwargs) -> None:
        super().__init__(message, status_code=404, error_type="not_found", **kwargs)


class MethodNotAllowedError(APIError):
    """405 - HTTP method not allowed."""

    def __init__(self, message: str = "Method not allowed", **kwargs) -> None:
        super().__init__(message, status_code=405, error_type="method_not_allowed", **kwargs)


class ConflictError(APIError):
    """409 - Resource conflict."""

    def __init__(self, message: str = "Conflict", **kwargs) -> None:
        super().__init__(message, status_code=409, error_type="conflict", **kwargs)


class RateLimitError(APIError):
    """429 - Too many requests."""

    def __init__(self, message: str = "Rate limit exceeded", **kwargs) -> None:
        super().__init__(message, status_code=429, error_type="rate_limit_exceeded", **kwargs)


# ---- 5xx Server Errors ----

class InternalServerError(APIError):
    """500 - Server-side error."""

    def __init__(self, message: str = "Internal server error", **kwargs) -> None:
        super().__init__(message, status_code=500, error_type="internal_error", **kwargs)


class ProviderError(APIError):
    """502 - Upstream provider error."""

    def __init__(self, message: str = "Provider error", **kwargs) -> None:
        super().__init__(message, status_code=502, error_type="provider_error", **kwargs)


class CapacityError(APIError):
    """503 - No capacity available."""

    def __init__(self, message: str = "No capacity available", **kwargs) -> None:
        super().__init__(message, status_code=503, error_type="capacity_error", **kwargs)


# ---- Network Errors (no HTTP status) ----

class ConnectionError(LayerbrainError):
    """Network-level connection failure."""


class TimeoutError(LayerbrainError):
    """Request timed out."""


# ---- Mappings ----

# Map HTTP status codes to exception classes
STATUS_CODE_TO_EXCEPTION: dict[int, type[APIError]] = {
    400: ValidationError,
    401: AuthenticationError,
    402: InsufficientFundsError,
    403: PermissionDeniedError,
    404: NotFoundError,
    405: MethodNotAllowedError,
    409: ConflictError,
    429: RateLimitError,
    500: InternalServerError,
    502: ProviderError,
    503: CapacityError,
}

# Map API error_type strings to exception classes (for when status code is ambiguous)
ERROR_TYPE_TO_EXCEPTION: dict[str, type[APIError]] = {
    # 400
    "validation_error": ValidationError,
    "invalid_request_error": ValidationError,
    "invalid_request": ValidationError,
    "bad_request": ValidationError,
    # 401
    "authentication_error": AuthenticationError,
    "authentication_failed": AuthenticationError,
    "expired": AuthenticationError,
    # 402
    "insufficient_funds": InsufficientFundsError,
    "amount_exceeded": InsufficientFundsError,
    "subscription_error": InsufficientFundsError,
    # 403
    "authorization_error": PermissionDeniedError,
    "forbidden": PermissionDeniedError,
    # 404
    "not_found": NotFoundError,
    "object_not_found": NotFoundError,
    # 405
    "method_not_allowed": MethodNotAllowedError,
    # 429
    "rate_limit_exceeded": RateLimitError,
    # 500
    "internal_error": InternalServerError,
    "internal_server_error": InternalServerError,
    "server_error": InternalServerError,
    "event_creation_failed": InternalServerError,
    "stripe_error": InternalServerError,
    # 502
    "provider_error": ProviderError,
    # 503
    "capacity_error": CapacityError,
}


def raise_for_status(status_code: int, body: dict) -> None:
    """Raise the appropriate exception based on API response status and body."""
    if 200 <= status_code < 300:
        return

    error_data = body.get("error", {})
    message = error_data.get("message", f"HTTP {status_code}")
    error_type = error_data.get("type")

    # Try error_type first (more specific), then fall back to status code
    exc_class = ERROR_TYPE_TO_EXCEPTION.get(error_type) if error_type else None
    if exc_class is None:
        exc_class = STATUS_CODE_TO_EXCEPTION.get(status_code)

    if exc_class is None:
        # Unknown status code, use generic APIError
        raise APIError(
            message,
            status_code=status_code,
            error_type=error_type,
            body=body,
        )

    raise exc_class(message, body=body)
