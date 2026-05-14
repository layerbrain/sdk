from __future__ import annotations

from typing import Any

from .._resource import Resource
from .._pagination import SyncPage


class Compute(Resource):
    """Compute API resource (auto-generated)."""

    async def retrieve(self) -> SyncPage:
        """Retrieve compute availability"""
        request_path = "/compute"
        data = await self._get(request_path, params=None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path=request_path,
        )
