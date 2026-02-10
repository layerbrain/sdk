from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Subscriptions(Resource):
    """Subscriptions API resource (auto-generated)."""

    async def list(self, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> SyncPage:
        """Get list"""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/subscriptions", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/subscriptions",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Post create"""
        return await self._post("/subscriptions", json=kwargs)

    async def balance(self, **kwargs: Any) -> dict:
        """Add to balance - creates Stripe checkout for one-time payment."""
        return await self._post("/subscriptions/balance", json=kwargs)

    async def downgrade(self, **kwargs: Any) -> dict:
        """Downgrade subscription tier (scheduled at period end)."""
        return await self._post("/subscriptions/downgrade", json=kwargs)

    async def pay_as_you_go(self, **kwargs: Any) -> dict:
        """Post pay_as_you_go"""
        return await self._post("/subscriptions/pay-as-you-go", json=kwargs)

    async def portal(self, **kwargs: Any) -> dict:
        """Create Stripe billing portal session for managing subscription."""
        return await self._post("/subscriptions/portal", json=kwargs)

    async def upgrade(self, **kwargs: Any) -> dict:
        """Upgrade subscription tier (immediate with proration)."""
        return await self._post("/subscriptions/upgrade", json=kwargs)

    async def retrieve(self, subscription_id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Get retrieve"""
        return await self._get(f"/subscriptions/{subscription_id}", params=None)
