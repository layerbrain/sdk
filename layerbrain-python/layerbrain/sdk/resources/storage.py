from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Storage(Resource):
    """Storage API resource (auto-generated)."""

    async def list_backends(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_backends"""
        request_path = "/storage/backends"
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

    async def create_backend(self, **kwargs: Any) -> dict:
        """Post create_backend"""
        return await self._post("/storage/backends", json=kwargs)

    async def delete_backend(self, id: str) -> dict:
        """Delete delete_backend"""
        return await self._delete(f"/storage/backends/{id}")

    async def retrieve_backend(self, id: str) -> dict:
        """Get retrieve_backend"""
        return await self._get(f"/storage/backends/{id}", params=None)

    async def update_backend(self, id: str, **kwargs: Any) -> dict:
        """Patch patch_backend"""
        return await self._patch(f"/storage/backends/{id}", json=kwargs)

    async def validate_backend(self, id: str) -> dict:
        """Post validate_backend"""
        return await self._post(f"/storage/backends/{id}/validate", json={})

    async def list_buckets(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_buckets"""
        request_path = "/storage/buckets"
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

    async def create_bucket(self, **kwargs: Any) -> dict:
        """Post create_bucket"""
        return await self._post("/storage/buckets", json=kwargs)

    async def delete_bucket(self, id: str) -> dict:
        """Delete delete_bucket"""
        return await self._delete(f"/storage/buckets/{id}")

    async def retrieve_bucket(self, id: str) -> dict:
        """Get retrieve_bucket"""
        return await self._get(f"/storage/buckets/{id}", params=None)

    async def update_bucket(self, id: str, **kwargs: Any) -> dict:
        """Patch patch_bucket"""
        return await self._patch(f"/storage/buckets/{id}", json=kwargs)

    async def presign_bucket(self, id: str, **kwargs: Any) -> dict:
        """Post presign_bucket"""
        return await self._post(f"/storage/buckets/{id}/presign", json=kwargs)
