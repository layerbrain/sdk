from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Secrets(Resource):
    """Secrets API resource (auto-generated)."""

    async def list(self, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> SyncPage:
        """List secrets for the authenticated user's organization."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/secrets", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/secrets",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Handle secret creation."""
        return await self._post("/secrets", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Handle secret deletion."""
        return await self._delete(f"/secrets/{id}")

    async def retrieve(self, id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Handle secret retrieval."""
        return await self._get(f"/secrets/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Handle secret updates via PATCH."""
        return await self._patch(f"/secrets/{id}", json=kwargs)

    async def replace(self, id: str, **kwargs: Any) -> dict:
        """Handle secret updates via PUT."""
        return await self._put(f"/secrets/{id}", json=kwargs)

    async def reveal(self, id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Reveal the unmasked secret value."""
        return await self._get(f"/secrets/{id}/reveal", params=None)
