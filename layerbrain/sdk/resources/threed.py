from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource


class ThreeD(Resource):
    """Threed API resource (auto-generated)."""

    async def generations(self, **kwargs: Any) -> dict:
        """Create 3D model from image(s)."""
        return await self._post("/3d/generations", json=kwargs)
