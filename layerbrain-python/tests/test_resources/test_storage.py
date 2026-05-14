from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock

from layerbrain.sdk.resources.storage import Storage


class TestStorage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client._get = AsyncMock()
        self.mock_client._post = AsyncMock()
        self.mock_client._patch = AsyncMock()
        self.mock_client._delete = AsyncMock()
        self.storage = Storage(self.mock_client)

    async def test_bucket_paths_use_public_storage_routes(self):
        self.mock_client._get.return_value = {"object": "list", "data": [], "has_more": False}
        await self.storage.list_buckets()
        self.mock_client._get.assert_called_once_with(
            "/buckets",
            params={"page": 1, "page_size": 10},
        )

        self.mock_client._post.return_value = {"id": "bkt_1"}
        await self.storage.create_bucket(name="assets")
        self.mock_client._post.assert_called_with("/buckets", json={"name": "assets"})

        await self.storage.presign_bucket("bkt_1", key="a.txt", operation="download")
        self.mock_client._post.assert_called_with(
            "/buckets/bkt_1/presign",
            json={"key": "a.txt", "operation": "download"},
        )

    async def test_object_operations_use_bucket_routes(self):
        self.mock_client._get.return_value = {"object": "list", "data": [], "has_more": False}
        await self.storage.list_bucket_objects("bkt_1", prefix="docs")
        self.mock_client._get.assert_called_with("/buckets/bkt_1/objects", params={"prefix": "docs"})

        await self.storage.search_objects(q="report")
        self.mock_client._get.assert_called_with("/objects/search", params={"q": "report"})

        self.mock_client._post.return_value = {"object": "storage.object.moved"}
        await self.storage.move_bucket_object("bkt_1", from_key="a.txt", to_key="b.txt")
        self.mock_client._post.assert_called_with(
            "/buckets/bkt_1/objects/move",
            json={"from_key": "a.txt", "to_key": "b.txt"},
        )


if __name__ == "__main__":
    unittest.main()
