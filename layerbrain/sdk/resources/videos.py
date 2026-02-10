from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource


class Videos(Resource):
    """Videos API resource (auto-generated)."""

    async def generations(self, **kwargs: Any) -> dict:
        """Create video generation."""
        return await self._post("/videos/generations", json=kwargs)

    async def retrieve(self, generation_id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Get video generation status and result."""
        return await self._get(f"/videos/generations/{generation_id}", params=None)
