"""Tests for the Machines resource."""

from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock

from layerbrain.sdk._types import Machine
from layerbrain.sdk.resources.machines import Machines


class TestMachines(unittest.IsolatedAsyncioTestCase):
    """Test async Machines resource."""

    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_client._get = AsyncMock()
        self.mock_client._post = AsyncMock()
        self.mock_client._delete = AsyncMock()
        self.machines = Machines(self.mock_client)

    async def test_list_returns_sync_page(self):
        self.mock_client._get.return_value = {
            "object": "list",
            "data": [
                {"id": "mach_1", "object": "machine", "name": "dev", "state": "active"},
                {"id": "mach_2", "object": "machine", "name": "prod", "state": "stopped"},
            ],
            "has_more": False,
        }
        page = await self.machines.list()
        self.assertEqual(len(page), 2)
        self.assertEqual(page.data[0]["id"], "mach_1")
        self.mock_client._get.assert_called_once_with("/machines", params=None)

    async def test_create_returns_machine(self):
        self.mock_client._post.return_value = {
            "id": "mach_new",
            "object": "machine",
            "name": "test-machine",
            "state": "provisioning",
        }
        machine = await self.machines.create(compute="A100", duration_minutes=30, name="test-machine")
        self.assertIsInstance(machine, Machine)
        self.assertEqual(machine.id, "mach_new")
        self.assertEqual(machine.state, "provisioning")
        self.mock_client._post.assert_called_once_with(
            "/machines",
            json={"compute": "A100", "duration_minutes": 30, "name": "test-machine"},
        )

    async def test_create_without_name(self):
        self.mock_client._post.return_value = {
            "id": "mach_new",
            "object": "machine",
            "state": "provisioning",
        }
        await self.machines.create(compute="H100")
        self.mock_client._post.assert_called_once_with(
            "/machines",
            json={"compute": "H100", "duration_minutes": 15},
        )

    async def test_claim_returns_machine(self):
        self.mock_client._post.return_value = {
            "id": "mach_claimed",
            "object": "machine",
            "environment": "personal",
            "state": "active",
        }
        machine = await self.machines.claim(environment="personal")
        self.assertIsInstance(machine, Machine)
        self.assertEqual(machine.id, "mach_claimed")
        self.mock_client._post.assert_called_once_with(
            "/machines/claim",
            json={"environment": "personal", "name": "sandbox", "autoenv": False},
        )

    async def test_claim_with_zone(self):
        self.mock_client._post.return_value = {
            "id": "mach_zoned",
            "object": "machine",
        }
        await self.machines.claim(environment="personal", zone="us-east-1", name="my-box")
        self.mock_client._post.assert_called_once_with(
            "/machines/claim",
            json={"environment": "personal", "name": "my-box", "autoenv": False, "zone": "us-east-1"},
        )

    async def test_retrieve_returns_machine(self):
        self.mock_client._get.return_value = {
            "id": "mach_123",
            "object": "machine",
            "name": "my-machine",
            "state": "active",
            "ipv4": "1.2.3.4",
        }
        machine = await self.machines.retrieve("mach_123")
        self.assertIsInstance(machine, Machine)
        self.assertEqual(machine.ipv4, "1.2.3.4")
        self.mock_client._get.assert_called_once_with("/machines/mach_123", params=None)

    async def test_delete(self):
        self.mock_client._delete.return_value = {}
        await self.machines.delete("mach_123")
        self.mock_client._delete.assert_called_once_with("/machines/mach_123")


if __name__ == "__main__":
    unittest.main()
