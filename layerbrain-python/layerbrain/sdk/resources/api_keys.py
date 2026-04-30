from __future__ import annotations

from typing import Any

from .._pagination import SyncPage
from .._resource import Resource


class APIKeys(Resource):
    """Api-Keys API resource (auto-generated)."""

    async def list(
        self,
        page: int | None = 1,
        page_size: int | None = 10,
        ordering: str | None = None,
    ) -> SyncPage:
        """List API keys for the authenticated organization."""
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

    async def create(self, **kwargs: Any) -> dict:
        """Create a new API key for the authenticated organization."""
        return await self._post("/api-keys", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete an API key."""
        return await self._delete(f"/api-keys/{id}")

    async def retrieve(self, id: str) -> dict:
        """Retrieve a single API key by ID."""
        return await self._get(f"/api-keys/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Update mutable API key fields."""
        return await self._patch(f"/api-keys/{id}", json=kwargs)

    async def rotate(self, id: str) -> dict:
        """Rotate an API key and return a fresh secret."""
        return await self._post(f"/api-keys/{id}/rotate", json={})
