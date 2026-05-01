from __future__ import annotations

from typing import Any

from .._resource import Resource
from .._pagination import SyncPage


class Compute(Resource):
    """Compute API resource (auto-generated)."""

    async def delete(self) -> dict:
        """Delete compute_disabled"""
        return await self._delete("/compute")

    async def list(self) -> SyncPage:
        """Get compute_disabled"""
        request_path = "/compute"
        data = await self._get(request_path, params=None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path=request_path,
        )

    async def create(self, **kwargs: Any) -> dict:
        """Post compute_disabled"""
        return await self._post("/compute", json=kwargs)

    async def compute_path_disabled(self, path: str) -> dict:
        """Delete compute_path_disabled"""
        return await self._delete(f"/compute/{path}")

    async def retrieve(self, path: str) -> dict:
        """Get compute_path_disabled"""
        return await self._get(f"/compute/{path}", params=None)

    async def update(self, path: str, **kwargs: Any) -> dict:
        """Patch compute_path_disabled"""
        return await self._patch(f"/compute/{path}", json=kwargs)

    async def create_compute_path_disabled(self, path: str, **kwargs: Any) -> dict:
        """Post compute_path_disabled"""
        return await self._post(f"/compute/{path}", json=kwargs)
