"""Models resource (hand-written).

Returns typed Pydantic Model objects and handles URL encoding
for model IDs that contain slashes (e.g. meta-llama/llama-3.1-8b).
This file is preserved by the generator -- do not auto-generate.
"""

from __future__ import annotations

from typing import Any, Optional
from urllib.parse import quote

from .._resource import Resource
from .._pagination import SyncPage
from .._types import Model


class Models(Resource):
    """AI models resource with typed Pydantic responses."""

    async def list(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List all available models."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/models", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/models",
        )

    async def retrieve(self, id: str) -> Model:
        """Get a specific model by ID.

        Model IDs containing slashes (e.g. 'meta-llama/llama-3.1-8b')
        are URL-encoded automatically.
        """
        encoded_id = quote(id, safe="")
        data = await self._get(f"/models/{encoded_id}", params=None)
        return Model(**data)
