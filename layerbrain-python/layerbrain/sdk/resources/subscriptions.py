from __future__ import annotations

from typing import Any

from .._pagination import SyncPage
from .._resource import Resource


class Subscriptions(Resource):
    """Subscriptions API resource (auto-generated)."""

    async def list(
        self,
        page: int | None = 1,
        page_size: int | None = 10,
        ordering: str | None = None,
    ) -> SyncPage:
        """List active subscriptions for the authenticated organization."""
        request_path = "/subscriptions"
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get(request_path, params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path=request_path,
        )

    async def create(self, **kwargs: Any) -> dict:
        """Create a hosted checkout intent for a subscription tier."""
        return await self._post("/subscriptions", json=kwargs)

    async def retrieve(self, subscription_id: str) -> dict:
        """Retrieve a subscription by ID."""
        return await self._get(f"/subscriptions/{subscription_id}", params=None)
