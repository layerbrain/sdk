from __future__ import annotations

from typing import Any, Optional

from .._resource import Resource
from .._pagination import SyncPage


class Storage(Resource):
    """Storage API resource (auto-generated)."""

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

    async def create_bucket_folder(self, id: str, **kwargs: Any) -> dict:
        """Post create_bucket_folder"""
        return await self._post(f"/storage/buckets/{id}/folders", json=kwargs)

    async def list_bucket_keys(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_bucket_keys"""
        request_path = f"/storage/buckets/{id}/keys"
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

    async def create_bucket_key(self, id: str, **kwargs: Any) -> dict:
        """Post create_bucket_key"""
        return await self._post(f"/storage/buckets/{id}/keys", json=kwargs)

    async def list_bucket_objects(
        self,
        id: str,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        """Get list_bucket_objects"""
        request_path = f"/storage/buckets/{id}/objects"
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

    async def copy(self, id: str, **kwargs: Any) -> dict:
        """Post copy_bucket_object"""
        return await self._post(f"/storage/buckets/{id}/objects/copy", json=kwargs)

    async def delete_bucket_object(self, id: str, **kwargs: Any) -> dict:
        """Post delete_bucket_object"""
        return await self._post(f"/storage/buckets/{id}/objects/delete", json=kwargs)

    async def head(self, id: str) -> dict:
        """Get head_bucket_object"""
        return await self._get(f"/storage/buckets/{id}/objects/head", params=None)

    async def move(self, id: str, **kwargs: Any) -> dict:
        """Post move_bucket_object"""
        return await self._post(f"/storage/buckets/{id}/objects/move", json=kwargs)

    async def presign_bucket(self, id: str, **kwargs: Any) -> dict:
        """Post presign_bucket"""
        return await self._post(f"/storage/buckets/{id}/presign", json=kwargs)

    async def delete_bucket_key(self, id: str) -> dict:
        """Delete delete_bucket_key"""
        return await self._delete(f"/storage/keys/{id}")
