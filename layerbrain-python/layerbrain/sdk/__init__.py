"""Layerbrain Python SDK.

Usage (sync)::

    client = Layerbrain(api_key="sk-...")
    models = client.models.list()

Usage (async)::

    client = Layerbrain(api_key="sk-...")
    models = await client.models.list()
"""

from __future__ import annotations

import asyncio

from ._client import AsyncHTTPClient, SyncHTTPClient
from .resources.accounts import Accounts
from .resources.api_keys import APIKeys
from .resources.audio import Audio
from .resources.brains import Brains
from .resources.chat import Chat
from .resources.compute import Compute
from .resources.embeddings import Embeddings
from .resources.events import Events
from .resources.exports import Exports
from .resources.images import Images
from .resources.machines import Machines
from .resources.memberships import Memberships
from .resources.models import Models
from .resources.organizations import Organizations
from .resources.plans import Plans
from .resources.secrets import Secrets
from .resources.snapshots import Snapshots
from .resources.statements import Statements
from .resources.storage import Storage
from .resources.subscriptions import Subscriptions
from .resources.threed import ThreeD
from .resources.videos import Videos
from .resources.webhooks import Webhooks
from .resources.work import Work


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
    "brains": Brains,
    "chat": Chat,
    "compute": Compute,
    "embeddings": Embeddings,
    "events": Events,
    "exports": Exports,
    "images": Images,
    "machines": Machines,
    "memberships": Memberships,
    "models": Models,
    "organizations": Organizations,
    "plans": Plans,
    "secrets": Secrets,
    "snapshots": Snapshots,
    "statements": Statements,
    "storage": Storage,
    "subscriptions": Subscriptions,
    "threed": ThreeD,
    "videos": Videos,
    "webhooks": Webhooks,
    "work": Work,
}


class Layerbrain:
    """Layerbrain API client.

    Resource methods return values directly in normal scripts and return
    awaitable coroutines when called inside an active event loop.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._async_mode = _has_running_loop()

        if self._async_mode:
            self._client = AsyncHTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)
        else:
            self._client = SyncHTTPClient(api_key=api_key, base_url=base_url, timeout=timeout)

        for name, cls in _RESOURCE_CLASSES.items():
            setattr(self, name, cls(self._client))

    def close(self) -> None:
        if not self._async_mode:
            self._client.close()

    def __enter__(self) -> Layerbrain:
        return self

    def __exit__(self, *args) -> None:
        self.close()

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
