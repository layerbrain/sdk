from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Events(Resource):
    """Events API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List organization events"""
        request_path = "/events"
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get(request_path, params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path=request_path,
        )

    async def create(self, **kwargs: Any) -> dict:
        """Create an organization event"""
        return await self._post("/events", json=kwargs)

    async def retrieve(self, id: str) -> dict:
        """Retrieve an event"""
        return await self._get(f"/events/{id}", params=None)
