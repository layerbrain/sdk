from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Statements(Resource):
    """Statements API resource (auto-generated)."""

    async def list(self, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> SyncPage:
        """List usage statements with filtering and pagination."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/statements", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/statements",
        )

    async def retrieve(self, statement_id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Retrieve a specific statement by ID, creating it if it doesn't exist."""
        return await self._get(f"/statements/{statement_id}", params=None)
