from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource


class Tools(Resource):
    """Tools API resource (auto-generated)."""

    async def fetch(self, **kwargs: Any) -> dict:
        """Fetch web page content using Playwright."""
        return await self._post("/tools/fetch", json=kwargs)

    async def search(self, **kwargs: Any) -> dict:
        """Search the web using Brave Search API."""
        return await self._post("/tools/search", json=kwargs)
