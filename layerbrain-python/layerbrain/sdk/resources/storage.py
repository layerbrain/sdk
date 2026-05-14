from __future__ import annotations

from typing import Any, Optional

from .._pagination import SyncPage
from .._resource import Resource


class Storage(Resource):
    """Storage API resource."""

    async def list_buckets(
        self,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        ordering: Optional[str] = None,
    ) -> SyncPage:
        request_path = "/buckets"
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
        return await self._post("/buckets", json=kwargs)

    async def delete_bucket(self, id: str) -> dict:
        return await self._delete(f"/buckets/{id}")

    async def retrieve_bucket(self, id: str) -> dict:
        return await self._get(f"/buckets/{id}", params=None)

    async def update_bucket(self, id: str, **kwargs: Any) -> dict:
        return await self._patch(f"/buckets/{id}", json=kwargs)

    async def presign_bucket(self, id: str, **kwargs: Any) -> dict:
        return await self._post(f"/buckets/{id}/presign", json=kwargs)

    async def search_objects(self, **params: Any) -> dict:
        return await self._get("/objects/search", params=params or None)

    async def list_bucket_objects(self, id: str, **params: Any) -> dict:
        return await self._get(f"/buckets/{id}/objects", params=params or None)

    async def head_bucket_object(self, id: str, **params: Any) -> dict:
        return await self._get(f"/buckets/{id}/objects/head", params=params or None)

    async def create_bucket_folder(self, id: str, **kwargs: Any) -> dict:
        return await self._post(f"/buckets/{id}/folders", json=kwargs)

    async def move_bucket_object(self, id: str, **kwargs: Any) -> dict:
        return await self._post(f"/buckets/{id}/objects/move", json=kwargs)

    async def copy_bucket_object(self, id: str, **kwargs: Any) -> dict:
        return await self._post(f"/buckets/{id}/objects/copy", json=kwargs)

    async def delete_bucket_object(self, id: str, **kwargs: Any) -> dict:
        return await self._post(f"/buckets/{id}/objects/delete", json=kwargs)
