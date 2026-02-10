from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Organizations(Resource):
    """Organizations API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List organizations for the authenticated user."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/organizations", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/organizations",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Handle organization creation."""
        return await self._post("/organizations", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete an organization."""
        return await self._delete(f"/organizations/{id}")

    async def retrieve(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> dict:
        """Retrieve a single organization."""
        return await self._get(f"/organizations/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Update an organization."""
        return await self._patch(f"/organizations/{id}", json=kwargs)
