"""Tests for the Webhooks resource and public SDK surface."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock

from layerbrain.sdk import Layerbrain
from layerbrain.sdk.resources.webhooks import Webhooks


class TestWebhooks(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client._get = AsyncMock()
        self.mock_client._post = AsyncMock()
        self.mock_client._patch = AsyncMock()
        self.mock_client._delete = AsyncMock()
        self.mock_client._base_url = "https://api.layerbrain.test"
        self.mock_client._api_key = "sk_test"
        self.webhooks = Webhooks(self.mock_client)

    async def test_list_returns_sync_page(self):
        self.mock_client._get.return_value = {
            "object": "list",
            "data": [{"id": "whk_123"}],
            "has_more": False,
        }
        page = await self.webhooks.list()
        self.assertEqual(page.data[0]["id"], "whk_123")
        self.mock_client._get.assert_called_once_with("/webhooks", params=None)

    async def test_rotate_secret_posts_to_rotate_endpoint(self):
        self.mock_client._post.return_value = {"id": "whk_123", "secret": "whsec_new"}
        payload = await self.webhooks.rotate_secret("whk_123")
        self.assertEqual(payload["secret"], "whsec_new")
        self.mock_client._post.assert_called_once_with(
            "/webhooks/whk_123/rotate-secret",
            json={},
        )

    def test_listen_request_uses_same_path_websocket(self):
        url, headers = self.webhooks.listen_request(events=["queue.created", "queue.updated"])
        self.assertEqual(
            url,
            "wss://api.layerbrain.test/v1/webhooks?events=queue.created%2Cqueue.updated",
        )
        self.assertEqual(headers["Authorization"], "Bearer sk_test")


class TestPublicSDKSurface(unittest.TestCase):
    def test_client_exposes_public_resources_only(self):
        client = Layerbrain(api_key="sk_test", base_url="https://api.layerbrain.test")
        try:
            for resource_name in (
                "events",
                "exports",
                "plans",
                "storage",
                "webhooks",
                "work",
            ):
                self.assertTrue(hasattr(client, resource_name))
            self.assertFalse(hasattr(client, "auth"))
            self.assertFalse(hasattr(client, "engrams"))
            self.assertFalse(hasattr(client, "tools"))
        finally:
            client.close()


if __name__ == "__main__":
    unittest.main()
