from __future__ import annotations

from typing import Any

from .._resource import Resource


class Embeddings(Resource):
    """Embeddings API resource (auto-generated)."""

    async def create(self, **kwargs: Any) -> dict:
        """Create embeddings for input text."""
        return await self._post("/embeddings", json=kwargs)
