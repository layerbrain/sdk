from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource


class Images(Resource):
    """Images API resource (auto-generated)."""

    async def edits(self, **kwargs: Any) -> dict:
        """Create image edit (image-to-image)."""
        return await self._post("/images/edits", json=kwargs)

    async def generations(self, **kwargs: Any) -> dict:
        """Create image generation."""
        return await self._post("/images/generations", json=kwargs)
