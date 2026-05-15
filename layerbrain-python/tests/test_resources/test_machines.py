"""Tests for the Machines resource."""

from __future__ import annotations

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
                {"id": "mch_1", "object": "machine", "name": "dev", "state": "active"},
                {"id": "mch_2", "object": "machine", "name": "prod", "state": "stopped"},
            ],
            "has_more": False,
        }
        page = await self.machines.list()
        self.assertEqual(len(page), 2)
        self.assertEqual(page.data[0]["id"], "mch_1")
        self.mock_client._get.assert_called_once_with("/machines", params=None)

    async def test_create_returns_machine(self):
        self.mock_client._post.return_value = {
            "id": "mch_new",
            "object": "machine",
            "name": "test-machine",
            "state": "provisioning",
        }
        machine = await self.machines.create(
            name="test-machine",
            cpu=2,
            ram=4,
            disk=20,
            ttl_minutes=60,
        )
        self.assertIsInstance(machine, Machine)
        self.assertEqual(machine.id, "mch_new")
        self.assertEqual(machine.state, "provisioning")
        self.mock_client._post.assert_called_once_with(
            "/machines",
            json={
                "name": "test-machine",
                "cpu": 2,
                "ram": 4,
                "disk": 20,
                "ttl_minutes": 60,
            },
        )

    async def test_create_without_name(self):
        self.mock_client._post.return_value = {
            "id": "mch_new",
            "object": "machine",
            "state": "provisioning",
        }
        await self.machines.create(cpu=1, ram=1)
        self.mock_client._post.assert_called_once_with(
            "/machines",
            json={"cpu": 1, "ram": 1},
        )

    async def test_extend(self):
        self.mock_client._post.return_value = {
            "id": "mch_123",
            "object": "machine",
        }
        payload = await self.machines.extend("mch_123", duration_minutes=30)
        self.mock_client._post.assert_called_once_with(
            "/machines/mch_123/extend",
            json={"duration_minutes": 30},
        )
        self.assertEqual(payload["id"], "mch_123")

    async def test_restore(self):
        self.mock_client._post.return_value = {
            "id": "mch_123",
            "object": "machine",
        }
        payload = await self.machines.restore("mch_123", snapshot="snp_123")
        self.mock_client._post.assert_called_once_with(
            "/machines/mch_123/restore",
            json={"snapshot": "snp_123"},
        )
        self.assertEqual(payload["id"], "mch_123")

    async def test_snapshot(self):
        self.mock_client._post.return_value = {
            "id": "snp_123",
            "object": "snapshot",
        }
        payload = await self.machines.snapshot("mch_123", name="nightly")
        self.mock_client._post.assert_called_once_with(
            "/machines/mch_123/snapshot",
            json={"name": "nightly"},
        )
        self.assertEqual(payload["id"], "snp_123")

    async def test_retrieve_returns_machine(self):
        self.mock_client._get.return_value = {
            "id": "mch_123",
            "object": "machine",
            "name": "my-machine",
            "state": "active",
            "ipv4": "1.2.3.4",
        }
        machine = await self.machines.retrieve("mch_123")
        self.assertIsInstance(machine, Machine)
        self.assertEqual(machine.ipv4, "1.2.3.4")
        self.mock_client._get.assert_called_once_with("/machines/mch_123", params=None)

    async def test_delete(self):
        self.mock_client._delete.return_value = {}
        await self.machines.delete("mch_123")
        self.mock_client._delete.assert_called_once_with("/machines/mch_123")


if __name__ == "__main__":
    unittest.main()
