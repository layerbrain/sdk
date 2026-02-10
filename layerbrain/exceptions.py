"""Public exception module for the Layerbrain SDK.

Usage::

    from layerbrain.exceptions import LayerbrainError, NotFoundError
"""

from layerbrain.sdk._exceptions import (
    APIError,
    AuthenticationError,
    CapacityError,
    ConflictError,
    ConnectionError,
    InsufficientFundsError,
    InternalServerError,
    LayerbrainError,
    MethodNotAllowedError,
    NotFoundError,
    PermissionDeniedError,
    ProviderError,
    RateLimitError,
    TimeoutError,
    ValidationError,
    raise_for_status,
)

__all__ = [
    "APIError",
    "AuthenticationError",
    "CapacityError",
    "ConflictError",
    "ConnectionError",
    "InsufficientFundsError",
    "InternalServerError",
    "LayerbrainError",
    "MethodNotAllowedError",
    "NotFoundError",
    "PermissionDeniedError",
    "ProviderError",
    "RateLimitError",
    "TimeoutError",
    "ValidationError",
    "raise_for_status",
]
