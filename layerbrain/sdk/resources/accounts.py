from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Accounts(Resource):
    """Accounts API resource (auto-generated)."""

    async def list(self, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> SyncPage:
        """Get current user's account."""
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if ordering is not None:
            params["ordering"] = ordering
        data = await self._get("/accounts", params=params or None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/accounts",
        )

    async def create(self, **kwargs: Any) -> dict:
        """Create endpoint is not allowed for accounts."""
        return await self._post("/accounts", json=kwargs)

    async def delete(self, id: str) -> dict:
        """Handles DELETE requests to delete account with cascading cleanup."""
        return await self._delete(f"/accounts/{id}")

    async def retrieve(self, id: str, page: Optional[int] = 1, page_size: Optional[int] = 10, ordering: Optional[str] = None) -> dict:
        """Handles GET requests to retrieve account info."""
        return await self._get(f"/accounts/{id}", params=None)

    async def update(self, id: str, **kwargs: Any) -> dict:
        """Handles PATCH requests to update account info."""
        return await self._patch(f"/accounts/{id}", json=kwargs)

    async def clear_data(self, id: str, **kwargs: Any) -> dict:
        """Clear all cloud storage data for the user's organization."""
        return await self._post(f"/accounts/{id}/clear-data", json=kwargs)

    async def export(self, id: str, **kwargs: Any) -> dict:
        """Generate presigned download URL for latest snapshot."""
        return await self._post(f"/accounts/{id}/export", json=kwargs)

    async def onboard(self, id: str, **kwargs: Any) -> dict:
        """Handle onboarding of a new account with activation code."""
        return await self._post(f"/accounts/{id}/onboard", json=kwargs)

    async def switch(self, id: str, **kwargs: Any) -> dict:
        """Switch organization/membership endpoint - returns new token with specified or latest membership."""
        return await self._post(f"/accounts/{id}/switch", json=kwargs)
