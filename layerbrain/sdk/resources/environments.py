from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Environments(Resource):
    """Environments API resource (auto-generated)."""

    async def list(self, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> SyncPage:
        """List environments for the authenticated user's organization."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/environments", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/environments",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Create (or return) an environment by slug."""
        return await self._post("/environments", json=kwargs)

    async def retrieve(self, id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Retrieve a single environment by id."""
        return await self._get(f"/environments/{id}", params=None)
