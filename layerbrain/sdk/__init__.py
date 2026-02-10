"""Layerbrain Python SDK.

Usage (sync)::

    with Layerbrain(api_key="sk-...") as client:
        machines = client.machines.list()

Usage (async)::

    async with Layerbrain(api_key="sk-...") as client:
        machines = await client.machines.list()
"""

from __future__ import annotations

import asyncio
from typing import Optional

from ._client import AsyncHTTPClient, SyncHTTPClient
from .resources.accounts import Accounts
from .resources.api_keys import APIKeys
from .resources.audio import Audio
from .resources.auth import Auth
from .resources.brains import Brains
from .resources.chat import Chat
from .resources.compute import Compute
from .resources.embeddings import Embeddings
from .resources.engrams import Engrams
from .resources.environments import Environments
from .resources.images import Images
from .resources.machines import Machines
from .resources.memberships import Memberships
from .resources.models import Models
from .resources.organizations import Organizations
from .resources.secrets import Secrets
from .resources.statements import Statements
from .resources.subscriptions import Subscriptions
from .resources.threed import ThreeD
from .resources.tools import Tools
from .resources.videos import Videos


def _has_running_loop() -> bool:
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


_RESOURCE_CLASSES = {
    "accounts": Accounts,
    "api_keys": APIKeys,
    "audio": Audio,
    "auth": Auth,
    "brains": Brains,
    "compute": Compute,
    "embeddings": Embeddings,
    "engrams": Engrams,
    "environments": Environments,
    "images": Images,
    "machines": Machines,
    "memberships": Memberships,
    "models": Models,
    "organizations": Organizations,
    "secrets": Secrets,
    "subscriptions": Subscriptions,
    "statements": Statements,
    "threed": ThreeD,
    "tools": Tools,
    "videos": Videos,
}


class Layerbrain:
    """Layerbrain API client.

    Auto-detects whether it's created inside a running event loop.
    If yes: async mode -- resource methods return coroutines (use ``await``).
    If no: sync mode -- resource methods return values directly.

    Args:
        api_key: API key. Falls back to LAYERBRAIN_API_KEY env var or ~/.layerbrain/credentials.toml.
        base_url: API base URL. Falls back to LAYERBRAIN_BASE_URL or https://api.layerbrain.com.
        timeout: HTTP request timeout in seconds.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self._async_mode = _has_running_loop()

        if self._async_mode:
            self._client = AsyncHTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)
        else:
            self._client = SyncHTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)

        self.chat = Chat(self._client)

        for name, cls in _RESOURCE_CLASSES.items():
            setattr(self, name, cls(self._client))

    # -- sync context manager --

    def close(self) -> None:
        if not self._async_mode:
            self._client.close()

    def __enter__(self) -> Layerbrain:
        return self

    def __exit__(self, *args) -> None:
        self.close()

    # -- async context manager --

    async def aclose(self) -> None:
        if self._async_mode:
            await self._client.close()

    async def __aenter__(self) -> Layerbrain:
        return self

    async def __aexit__(self, *args) -> None:
        await self.aclose()


__all__ = [
    "Layerbrain",
]
