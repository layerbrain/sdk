from __future__ import annotations

from typing import Any

from .._resource import Resource


class Images(Resource):
    """Images API resource (auto-generated)."""

    async def create_edit(self, **kwargs: Any) -> dict:
        """Edit images"""
        return await self._post("/images/edits", json=kwargs)

    async def create_generation(self, **kwargs: Any) -> dict:
        """Generate images"""
        return await self._post("/images/generations", json=kwargs)
