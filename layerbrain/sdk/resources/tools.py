from __future__ import annotations

from typing import Any

from .._resource import Resource


class Tools(Resource):
    """Tools API resource (auto-generated)."""

    async def web_search(self, **kwargs: Any) -> dict:
        """Search the web"""
        return await self._post("/tools/web-search", json=kwargs)
