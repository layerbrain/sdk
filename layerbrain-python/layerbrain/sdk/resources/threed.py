from __future__ import annotations

from typing import Any

from .._resource import Resource


class ThreeD(Resource):
    """3D API resource (auto-generated)."""

    async def generations(self, **kwargs: Any) -> dict:
        """Post create_generation"""
        return await self._post("/3d/generations", json=kwargs)

    async def retrieve(self, generation_id: str) -> dict:
        """Get retrieve_generation"""
        return await self._get(f"/3d/generations/{generation_id}", params=None)
