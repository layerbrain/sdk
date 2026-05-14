from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Exports(Resource):
    """Exports API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List data exports"""
        request_path = "/exports"
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

    async def create(self) -> dict:
        """Create a data export"""
        return await self._post("/exports", json={})

    async def download(self, id: str) -> dict:
        """Create an export download URL"""
        return await self._get(f"/exports/{id}/download", params=None)
