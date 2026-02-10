"""Tests for the Models resource."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock

from layerbrain.sdk._types import Model
from layerbrain.sdk.resources.models import Models


class TestModels(unittest.IsolatedAsyncioTestCase):
    """Test async Models resource."""

    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client._get = AsyncMock()
        self.models = Models(self.mock_client)

    async def test_list_returns_sync_page(self):
        self.mock_client._get.return_value = {
            "object": "list",
            "data": [
                {"id": "meta-llama/llama-3.1-8b", "object": "model", "type": "chat", "provider": "together"},
                {"id": "stability/sdxl", "object": "model", "type": "image", "provider": "replicate"},
            ],
            "has_more": False,
        }
        page = await self.models.list()
        self.assertEqual(len(page), 2)
        self.assertEqual(page.data[0]["id"], "meta-llama/llama-3.1-8b")

    async def test_retrieve_encodes_model_id(self):
        self.mock_client._get.return_value = {
            "id": "meta-llama/llama-3.1-8b",
            "object": "model",
            "type": "chat",
            "provider": "together",
            "pricing": {"unit": "token"},
        }
        model = await self.models.retrieve("meta-llama/llama-3.1-8b")
        self.assertIsInstance(model, Model)
        self.assertEqual(model.id, "meta-llama/llama-3.1-8b")
        self.assertEqual(model.type, "chat")
        # Verify URL encoding: slash should be encoded as %2F
        self.mock_client._get.assert_called_once_with("/resources/meta-llama%2Fllama-3.1-8b", params=None)


if __name__ == "__main__":
    unittest.main()
