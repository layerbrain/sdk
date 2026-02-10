from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Engrams(Resource):
    """Engrams API resource (auto-generated)."""

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
        data = await self._get("/engrams", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/engrams",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Post create"""
        return await self._post("/engrams", json=kwargs)

    async def delete_all(self, **kwargs: Any) -> dict:
        """Delete all engrams for the user's organization."""
        return await self._post("/engrams/delete-all", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete delete"""
        return await self._delete(f"/engrams/{id}")

    async def retrieve(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> dict:
        """Get retrieve"""
        return await self._get(f"/engrams/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Patch patch"""
        return await self._patch(f"/engrams/{id}", json=kwargs)

    async def archive(self, id: str, **kwargs: Any) -> dict:
        """Post archive"""
        return await self._post(f"/engrams/{id}/archive", json=kwargs)

    async def restore(self, id: str, **kwargs: Any) -> dict:
        """Post restore"""
        return await self._post(f"/engrams/{id}/restore", json=kwargs)
