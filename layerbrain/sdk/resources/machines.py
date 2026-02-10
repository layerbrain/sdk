"""Machines resource (hand-written).

Returns typed Pydantic Machine models and supports WebSocket connections
with shell and filesystem sub-interfaces.
This file is preserved by the generator -- do not auto-generate.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .._resource import Resource
from .._pagination import SyncPage
from .._types import Machine
import websockets

from .._connection import MachineConnection
from .._transport import WebSocketTransport


class Machines(Resource):
    """Machines resource with typed Pydantic responses and WebSocket connect."""

    async def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List all active machines for the user's organization."""
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/machines", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/machines",
        )

    async def create(self, *, duration_minutes: int = 15, **kwargs: Any) -> Machine:
        """Create a new machine by purchasing a contract."""
        body = {"duration_minutes": duration_minutes, **kwargs}
        data = await self._post("/machines", json=body)
        return Machine(**data)

    async def claim(
        self,
        *,
        environment: str,
        name: str = "sandbox",
        autoenv: bool = False,
        **kwargs: Any,
    ) -> Machine:
        """Claim a pool machine for active usage within an environment."""
        body = {"environment": environment, "name": name, "autoenv": autoenv, **kwargs}
        data = await self._post("/machines/claim", json=body)
        return Machine(**data)

    async def retrieve(self, machine_id: str) -> Machine:
        """Get machine details."""
        data = await self._get(f"/machines/{machine_id}", params=None)
        return Machine(**data)

    async def delete(self, machine_id: str) -> Dict[str, Any]:
        """Delete a machine by releasing it."""
        return await self._delete(f"/machines/{machine_id}")

    async def connect(self, machine_id: str) -> MachineConnection:
        """Open a WebSocket connection to a machine.

        Returns a MachineConnection with .shell and .filesystem interfaces.

        Usage::

            async with client.machines.connect("mach_abc123") as machine:
                result = await machine.shell.execute("ls -la")
                files = await machine.filesystem.list("~/brain")
        """
        base_url = self._client._base_url
        # Convert http(s) to ws(s)
        if base_url.startswith("https://"):
            ws_url = "wss://" + base_url[8:]
        elif base_url.startswith("http://"):
            ws_url = "ws://" + base_url[7:]
        else:
            ws_url = "wss://" + base_url

        url = f"{ws_url}/v1/machines/{machine_id}/connect"

        headers = {}
        if self._client._api_key:
            headers["Authorization"] = f"Bearer {self._client._api_key}"

        ws = await websockets.connect(url, additional_headers=headers)
        transport = WebSocketTransport(ws)
        connection = MachineConnection(machine_id, transport)
        await connection._start_listener()

        return connection
