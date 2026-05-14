from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Secrets(Resource):
    """Secrets API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List secrets"""
        request_path = "/secrets"
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
        """Create a secret"""
        return await self._post("/secrets", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete a secret"""
        return await self._delete(f"/secrets/{id}")

    async def retrieve(self, id: str) -> dict:
        """Retrieve a secret"""
        return await self._get(f"/secrets/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Update a secret"""
        return await self._patch(f"/secrets/{id}", json=kwargs)

    async def reveal(self, id: str) -> dict:
        """Reveal a secret value"""
        return await self._get(f"/secrets/{id}/reveal", params=None)
