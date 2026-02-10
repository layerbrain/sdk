from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource


class Brains(Resource):
    """Brains API resource (auto-generated)."""

    async def create(self, **kwargs: Any) -> dict:
        """Create a new brain resource."""
        return await self._post("/brains", json=kwargs)
