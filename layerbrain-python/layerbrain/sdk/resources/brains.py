from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Brains(Resource):
    """Brains API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_brains"""
        request_path = "/brains"
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
        """Create a new brain resource."""
        return await self._post("/brains", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete delete_brain"""
        return await self._delete(f"/brains/{id}")

    async def retrieve(self, id: str) -> dict:
        """Get retrieve_brain"""
        return await self._get(f"/brains/{id}", params=None)

    async def archive(self, id: str) -> dict:
        """Post archive_brain"""
        return await self._post(f"/brains/{id}/archive", json={})
