from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Memberships(Resource):
    """Memberships API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List organization memberships"""
        request_path = "/memberships"
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
        """Invite organization members"""
        return await self._post("/memberships", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Remove a membership"""
        return await self._delete(f"/memberships/{id}")

    async def retrieve(self, id: str) -> dict:
        """Retrieve a membership"""
        return await self._get(f"/memberships/{id}", params=None)

    async def update(self, id: str) -> dict:
        """Update a membership"""
        return await self._patch(f"/memberships/{id}", json={})
