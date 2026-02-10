from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class APIKeys(Resource):
    """Api-Keys API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list"""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/api-keys", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/api-keys",
        )

    async def api_keys(self, **kwargs: Any) -> dict:
        """Post create"""
        return await self._post("/api-keys", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete destroy"""
        return await self._delete(f"/api-keys/{id}")

    async def retrieve(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> dict:
        """Get retrieve"""
        return await self._get(f"/api-keys/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Patch patch"""
        return await self._patch(f"/api-keys/{id}", json=kwargs)

    async def rotate(self, id: str, **kwargs: Any) -> dict:
        """Post rotate"""
        return await self._post(f"/api-keys/{id}/rotate", json=kwargs)
