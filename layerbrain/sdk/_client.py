"""Core HTTP client for the Layerbrain SDK.

Provides both synchronous (Layerbrain) and asynchronous (AsyncLayerbrain) clients.
"""

from __future__ import annotations

import sys
from typing import Any, AsyncIterator, Dict, Iterator, Optional

import httpx

from ._config import Config
from ._exceptions import (
    AuthenticationError,
    ConnectionError,
    TimeoutError,
    raise_for_status,
)
from .._version import __version__


def _default_user_agent() -> str:
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return f"layerbrain/{__version__} python/{py}"


class _BaseClient:
    """Shared logic for sync and async clients."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self._config = Config()
        self._api_key = api_key or self._config.api_key
        raw_url = (base_url or self._config.base_url).rstrip("/")
        # Strip /v1 suffix if caller included it to prevent double /v1/v1
        if raw_url.endswith("/v1"):
            raw_url = raw_url[:-3]
        self._base_url = raw_url

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "User-Agent": _default_user_agent(),
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    def _require_auth(self) -> None:
        if not self._api_key:
            raise AuthenticationError(
                "No API key provided. Set LAYERBRAIN_API_KEY or pass api_key= to the client."
            )

    def _full_url(self, path: str) -> str:
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self._base_url}/v1{path}"


# ---------------------------------------------------------------------------
# Synchronous client
# ---------------------------------------------------------------------------


class SyncHTTPClient(_BaseClient):
    """Synchronous HTTP client wrapping httpx.Client."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url)
        self._http = httpx.Client(
            headers=self._build_headers(),
            follow_redirects=True,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        self._require_auth()
        url = self._full_url(path)

        try:
            response = self._http.request(
                method, url, params=params, json=json, timeout=timeout
            )
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.ConnectError as e:
            raise ConnectionError(f"Connection failed: {e}") from e

        body = response.json()
        raise_for_status(response.status_code, body)
        return body

    def _get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("GET", path, params=params)

    def _post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("POST", path, json=json)

    def _patch(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("PATCH", path, json=json)

    def _put(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("PUT", path, json=json)

    def _delete(self, path: str) -> Dict[str, Any]:
        return self._request("DELETE", path)

    def _stream_sse(
        self,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
    ) -> Iterator[str]:
        """POST and yield SSE data lines."""
        self._require_auth()
        url = self._full_url(path)
        with self._http.stream("POST", url, json=json) as response:
            if response.status_code >= 400:
                body = {}
                for chunk in response.iter_text():
                    body = {"error": {"message": chunk}}
                    break
                raise_for_status(response.status_code, body)

            for line in response.iter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        return
                    yield data

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> SyncHTTPClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


# ---------------------------------------------------------------------------
# Asynchronous client
# ---------------------------------------------------------------------------


class AsyncHTTPClient(_BaseClient):
    """Asynchronous HTTP client wrapping httpx.AsyncClient."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(api_key=api_key, base_url=base_url)
        self._http = httpx.AsyncClient(
            headers=self._build_headers(),
            follow_redirects=True,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        self._require_auth()
        url = self._full_url(path)

        try:
            response = await self._http.request(
                method, url, params=params, json=json, timeout=timeout
            )
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}") from e
        except httpx.ConnectError as e:
            raise ConnectionError(f"Connection failed: {e}") from e

        body = response.json()
        raise_for_status(response.status_code, body)
        return body

    async def _get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("GET", path, params=params)

    async def _post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("POST", path, json=json)

    async def _patch(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("PATCH", path, json=json)

    async def _put(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("PUT", path, json=json)

    async def _delete(self, path: str) -> Dict[str, Any]:
        return await self._request("DELETE", path)

    async def _stream_sse(
        self,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[str]:
        """POST and yield SSE data lines."""
        self._require_auth()
        url = self._full_url(path)
        async with self._http.stream("POST", url, json=json) as response:
            if response.status_code >= 400:
                body = {}
                async for chunk in response.aiter_text():
                    body = {"error": {"message": chunk}}
                    break
                raise_for_status(response.status_code, body)

            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        return
                    yield data

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncHTTPClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
