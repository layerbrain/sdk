from __future__ import annotations

from typing import Any

from .._resource import Resource


class Videos(Resource):
    """Videos API resource (auto-generated)."""

    async def create(self, **kwargs: Any) -> dict:
        """Post create_generation"""
        return await self._post("/videos/generations", json=kwargs)

    async def retrieve(self, generation_id: str) -> dict:
        """Get retrieve_generation"""
        return await self._get(f"/videos/generations/{generation_id}", params=None)
