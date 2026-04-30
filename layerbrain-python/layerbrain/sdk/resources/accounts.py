from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Accounts(Resource):
    """Accounts API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get current user's account."""
        request_path = "/accounts"
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

    async def delete(self, id: str) -> dict:
        """Handles DELETE requests to delete account with cascading cleanup."""
        return await self._delete(f"/accounts/{id}")

    async def retrieve(self, id: str) -> dict:
        """Handles GET requests to retrieve account info."""
        return await self._get(f"/accounts/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Handles PATCH requests to update account info."""
        return await self._patch(f"/accounts/{id}", json=kwargs)
