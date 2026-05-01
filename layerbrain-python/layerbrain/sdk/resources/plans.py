from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Plans(Resource):
    """Plans API resource (auto-generated)."""

    async def list_items(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list"""
        request_path = "/plans"
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

    async def create_item(self, **kwargs: Any) -> dict:
        """Post create"""
        return await self._post("/plans", json=kwargs)

    async def retrieve_item(self, id: str) -> dict:
        """Get retrieve"""
        return await self._get(f"/plans/{id}", params=None)

    async def update_item(self, id: str, **kwargs: Any) -> dict:
        """Patch patch"""
        return await self._patch(f"/plans/{id}", json=kwargs)

    async def list_activity(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_activity"""
        request_path = f"/plans/{id}/activity"
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

    async def cancel(self, id: str, **kwargs: Any) -> dict:
        """Post cancel"""
        return await self._post(f"/plans/{id}/cancel", json=kwargs)

    async def list_comments(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_comments"""
        request_path = f"/plans/{id}/comments"
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

    async def create_comment(self, id: str, **kwargs: Any) -> dict:
        """Post create_comment"""
        return await self._post(f"/plans/{id}/comments", json=kwargs)

    async def delete_item(self, id: str) -> dict:
        """Delete delete_items"""
        return await self._delete(f"/plans/{id}/items")

    async def item(self, id: str, **kwargs: Any) -> dict:
        """Patch patch_items"""
        return await self._patch(f"/plans/{id}/items", json=kwargs)

    async def items(self, id: str, **kwargs: Any) -> dict:
        """Post add_items"""
        return await self._post(f"/plans/{id}/items", json=kwargs)

    async def list_item_activity(
        self,
        id: str,
        item: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_item_activity"""
        request_path = f"/plans/{id}/items/{item}/activity"
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

    async def list_item_comments(
        self,
        id: str,
        item: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_item_comments"""
        request_path = f"/plans/{id}/items/{item}/comments"
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

    async def create_item_comment(self, id: str, item: str, **kwargs: Any) -> dict:
        """Post create_item_comment"""
        return await self._post(f"/plans/{id}/items/{item}/comments", json=kwargs)

    async def resume(self, id: str, **kwargs: Any) -> dict:
        """Post resume"""
        return await self._post(f"/plans/{id}/resume", json=kwargs)

    async def start(self, id: str, **kwargs: Any) -> dict:
        """Post start"""
        return await self._post(f"/plans/{id}/start", json=kwargs)
