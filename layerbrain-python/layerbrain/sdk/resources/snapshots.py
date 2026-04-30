from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Snapshots(Resource):
    """Snapshots API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List snapshots for the authenticated organization."""
        request_path = "/snapshots"
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
        """Create a snapshot for a machine."""
        return await self._post("/snapshots", json=kwargs)

    async def retrieve(self, id: str) -> dict:
        """Retrieve snapshot metadata by ID."""
        return await self._get(f"/snapshots/{id}", params=None)

    async def download(self, id: str) -> dict:
        """Create a download payload for a snapshot."""
        return await self._get(f"/snapshots/{id}/download", params=None)

    async def restore(self, id: str, **kwargs: Any) -> dict:
        """Restore snapshot contents to a target machine."""
        return await self._post(f"/snapshots/{id}/restore", json=kwargs)
