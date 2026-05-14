from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Subscriptions(Resource):
    """Subscriptions API resource (auto-generated)."""

    async def list(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """List active subscriptions"""
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
        """Create a subscription checkout"""
        return await self._post("/subscriptions", json=kwargs)

    async def balance(self, **kwargs: Any) -> dict:
        """Create a balance top-up checkout"""
        return await self._post("/subscriptions/balance", json=kwargs)

    async def downgrade(self, **kwargs: Any) -> dict:
        """Downgrade subscription tier"""
        return await self._post("/subscriptions/downgrade", json=kwargs)

    async def portal(self) -> dict:
        """Create a billing portal session"""
        return await self._post("/subscriptions/portal", json={})

    async def upgrade(self, **kwargs: Any) -> dict:
        """Upgrade subscription tier"""
        return await self._post("/subscriptions/upgrade", json=kwargs)

    async def retrieve(self, subscription_id: str) -> dict:
        """Retrieve a subscription"""
        return await self._get(f"/subscriptions/{subscription_id}", params=None)
