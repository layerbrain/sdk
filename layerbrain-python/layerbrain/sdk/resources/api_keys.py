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
        """List API keys"""
        request_path = "/api-keys"
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

    async def api_keys(self, **kwargs: Any) -> dict:
        """Create an API key"""
        return await self._post("/api-keys", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete an API key"""
        return await self._delete(f"/api-keys/{id}")

    async def retrieve(self, id: str) -> dict:
        """Retrieve an API key"""
        return await self._get(f"/api-keys/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Update an API key"""
        return await self._patch(f"/api-keys/{id}", json=kwargs)

    async def rotate(self, id: str) -> dict:
        """Rotate an API key"""
        return await self._post(f"/api-keys/{id}/rotate", json={})
