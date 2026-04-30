from __future__ import annotations

from typing import Any

from .._resource import Resource


class Brains(Resource):
    """Brains API resource (auto-generated)."""

    async def create(self, **kwargs: Any) -> dict:
        """Create a new brain resource."""
        return await self._post("/brains", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Delete delete_brain"""
        return await self._delete(f"/brains/{id}")

    async def retrieve(self, id: str) -> dict:
        """Get retrieve_brain"""
        return await self._get(f"/brains/{id}", params=None)

    async def archive(self, id: str) -> dict:
        """Post archive_brain"""
        return await self._post(f"/brains/{id}/archive", json={})
