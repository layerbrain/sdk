from __future__ import annotations

from typing import Any

from .._resource import Resource
from .._pagination import SyncPage


class Snapshots(Resource):
    """Snapshots API resource (auto-generated)."""

    async def delete(self) -> dict:
        """Delete snapshots_disabled"""
        return await self._delete("/snapshots")

    async def list(self) -> SyncPage:
        """Get snapshots_disabled"""
        request_path = "/snapshots"
        data = await self._get(request_path, params=None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path=request_path,
        )

    async def create(self, **kwargs: Any) -> dict:
        """Post snapshots_disabled"""
        return await self._post("/snapshots", json=kwargs)

    async def snapshots_path_disabled(self, path: str) -> dict:
        """Delete snapshots_path_disabled"""
        return await self._delete(f"/snapshots/{path}")

    async def retrieve(self, path: str) -> dict:
        """Get snapshots_path_disabled"""
        return await self._get(f"/snapshots/{path}", params=None)

    async def update(self, path: str, **kwargs: Any) -> dict:
        """Patch snapshots_path_disabled"""
        return await self._patch(f"/snapshots/{path}", json=kwargs)

    async def create_snapshots_path_disabled(self, path: str, **kwargs: Any) -> dict:
        """Post snapshots_path_disabled"""
        return await self._post(f"/snapshots/{path}", json=kwargs)
