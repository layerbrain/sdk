"""Machines resource (hand-written).

Returns typed Pydantic Machine models and supports SSH session initiation.
This file is preserved by the generator -- do not auto-generate.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .._resource import Resource
from .._pagination import SyncPage
from .._types import Machine


class Machines(Resource):
    """Machines resource with typed Pydantic responses."""

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
