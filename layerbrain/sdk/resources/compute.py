from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Compute(Resource):
    """Compute API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List all compute specifications with capacity per zone."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/compute", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/compute",
        )

    async def retrieve(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> dict:
        """Get detailed information about a specific compute offering."""
        return await self._get(f"/compute/{id}", params=None)
