"""Auth resource (hand-written).

Returns typed Pydantic models for authentication flows.
This file is preserved by the generator -- do not auto-generate.
"""

from __future__ import annotations

from typing import Any, Dict, Union

from .._resource import Resource
from .._types import AuthIntent, AuthToken, DeviceAuthorization


class Auth(Resource):
    """Authentication resource with typed Pydantic responses."""

    async def login(self, **kwargs: Any) -> Union[AuthToken, AuthIntent]:
        """Login via email/password or magic link.

        Returns AuthToken for direct login, AuthIntent for magic/MFA flows.
        """
        data = await self._post("/auth/login", json=kwargs)
        if data.get("object") == "token":
            return AuthToken(**data)
        return AuthIntent(**data)

    async def signup(self, **kwargs: Any) -> AuthIntent:
        """Create a new account. Returns an AuthIntent for confirmation."""
        data = await self._post("/auth/signup", json=kwargs)
        return AuthIntent(**data)

    async def confirm(self, id: str, **kwargs: Any) -> AuthToken:
        """Confirm an auth intent (email verification, MFA, etc.)."""
        data = await self._post(f"/auth/intents/{id}/confirm", json=kwargs)
        return AuthToken(**data)

    async def refresh(self, **kwargs: Any) -> AuthToken:
        """Refresh an access token."""
        data = await self._post("/auth/token/refresh", json=kwargs)
        return AuthToken(**data)

    async def device(self, **kwargs: Any) -> DeviceAuthorization:
        """Start device authorization flow (CLI login)."""
        data = await self._post("/auth/device", json=kwargs)
        return DeviceAuthorization(**data)

    async def token_exchange(self, **kwargs: Any) -> Union[AuthToken, Dict[str, Any]]:
        """Exchange a device code or grant for tokens.

        Returns AuthToken on success, raw dict on pending/error.
        """
        data = await self._post("/auth/token", json=kwargs)
        if data.get("object") == "token":
            return AuthToken(**data)
        return data

    async def logout(self, **kwargs: Any) -> Dict[str, Any]:
        """Logout and clear session."""
        return await self._post("/auth/logout", json=kwargs)

    async def password_reset(self, **kwargs: Any) -> Dict[str, Any]:
        """Request a password reset."""
        return await self._post("/auth/password-reset", json=kwargs)

    async def password_reset_confirm(self, id: str, **kwargs: Any) -> Dict[str, Any]:
        """Confirm a password reset."""
        return await self._post(f"/auth/password-reset/{id}/confirm", json=kwargs)
