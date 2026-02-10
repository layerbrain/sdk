from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Memberships(Resource):
    """Memberships API resource (auto-generated)."""

    async def list(self, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> SyncPage:
        """List memberships based on query parameters:"""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/memberships", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/memberships",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Create memberships or membership invites."""
        return await self._post("/memberships", json=kwargs)

    async def accept(self, id: str, **kwargs: Any) -> dict:
        """Accept a membership invitation and connect the account to the membership."""
        return await self._post(f"/memberships/invite/{id}/accept", json=kwargs)

    async def cancel(self, id: str, **kwargs: Any) -> dict:
        """Cancel a membership invitation. Both organization members and the invited user can cancel."""
        return await self._post(f"/memberships/invite/{id}/cancel", json=kwargs)

    async def retrieve(self, id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Retrieve a single membership."""
        return await self._get(f"/memberships/{id}", params=None)
