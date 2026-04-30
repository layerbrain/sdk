"""Private CLI-only auth client.

This keeps hidden auth endpoints out of the public SDK surface while still
letting the CLI perform device login and logout flows.
"""

from __future__ import annotations

from typing import Any

import httpx

from layerbrain.sdk._client import _default_user_agent
from layerbrain.sdk._config import Config
from layerbrain.sdk._exceptions import raise_for_status
from layerbrain.sdk._types import AuthToken, DeviceAuthorization


class CLIAuthClient:
    """Private HTTP client for CLI authentication flows."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        config = Config()
        self._api_key = api_key or config.api_key
        raw_url = (base_url or config.base_url).rstrip("/")
        if raw_url.endswith("/v1"):
            raw_url = raw_url[:-3]
        self._base_url = raw_url
        self._http = httpx.Client(
            headers=self._build_headers(),
            follow_redirects=True,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": _default_user_agent(),
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    def _full_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self._base_url}/v1/auth{path}"

    def _post(self, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._http.post(self._full_url(path), json=json)
        body = response.json()
        raise_for_status(response.status_code, body)
        return body

    def device(self, *, client_id: str) -> DeviceAuthorization:
        """Start the CLI device authorization flow."""
        data = self._post("/device", json={"client_id": client_id})
        return DeviceAuthorization(**data)

    def token_exchange(self, **kwargs: Any) -> AuthToken | dict[str, Any]:
        """Exchange a device code grant for an auth token."""
        data = self._post("/token", json=kwargs)
        if data.get("object") == "token":
            return AuthToken(**data)
        return data

    def logout(self) -> dict[str, Any]:
        """Invalidate the current session if possible."""
        return self._post("/logout", json={})

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> CLIAuthClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
