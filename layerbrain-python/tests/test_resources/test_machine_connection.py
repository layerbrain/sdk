"""Tests for machine WebSocket connection, shell, and filesystem."""

from __future__ import annotations

import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from layerbrain.sdk._transport import WebSocketTransport, MachineError
from layerbrain.sdk._connection import (
    MachineConnection,
    MachineShell,
    MachineFilesystem,
)


class FakeWebSocket:
    """Fake WebSocket that records sent messages and allows injecting responses."""

    def __init__(self):
        self.sent: list[str] = []
        self._incoming: asyncio.Queue = asyncio.Queue()
        self.closed = False

    async def send(self, data: str) -> None:
        self.sent.append(data)

    async def close(self) -> None:
        self.closed = True

    def inject(self, message: dict) -> None:
        """Inject a message as if the server sent it."""
        self._incoming.put_nowait(json.dumps(message))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await asyncio.wait_for(self._incoming.get(), timeout=0.5)
        except asyncio.TimeoutError:
            raise StopAsyncIteration


class TestWebSocketTransport(unittest.IsolatedAsyncioTestCase):
    """Test the WebSocket transport layer."""

    async def test_send_and_receive(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)

        async def respond_after_send():
            # Wait for the message to be sent
            await asyncio.sleep(0.05)
            sent = json.loads(ws.sent[0])
            ws.inject({"id": sent["id"], "data": {"stdout": "hello"}})

        asyncio.create_task(respond_after_send())
        listener = asyncio.create_task(transport.listen())

        result = await transport.send("shell.execute", {"command": "echo hello"})
        self.assertEqual(result, {"stdout": "hello"})

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_send_error_response(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)

        async def respond_with_error():
            await asyncio.sleep(0.05)
            sent = json.loads(ws.sent[0])
            ws.inject({
                "id": sent["id"],
                "error": {"type": "not_found", "message": "Path not found"},
            })

        asyncio.create_task(respond_with_error())
        listener = asyncio.create_task(transport.listen())

        with self.assertRaises(MachineError) as ctx:
            await transport.send("inodes.stat", {"path": "/nope"})

        self.assertEqual(ctx.exception.error_type, "not_found")
        self.assertIn("Path not found", ctx.exception.message)

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_emit_fire_and_forget(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)

        await transport.emit("shell.input", {"data": "ls\n"})
        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "shell.input")
        self.assertNotIn("id", sent)

    async def test_close(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)
        await transport.close()
        self.assertTrue(ws.closed)


class TestMachineShell(unittest.IsolatedAsyncioTestCase):
    """Test the MachineShell sub-interface."""

    async def test_execute(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)
        shell = MachineShell(transport)

        async def respond():
            await asyncio.sleep(0.05)
            sent = json.loads(ws.sent[0])
            ws.inject({
                "id": sent["id"],
                "data": {"stdout": "file.txt\n", "stderr": "", "code": 0},
            })

        asyncio.create_task(respond())
        listener = asyncio.create_task(transport.listen())

        result = await shell.execute("ls")
        self.assertEqual(result["stdout"], "file.txt\n")
        self.assertEqual(result["code"], 0)

        # Verify the sent message
        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "shell.execute")
        self.assertEqual(sent["params"]["command"], "ls")
        self.assertEqual(sent["params"]["timeout"], 30)

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_execute_with_cwd(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)
        shell = MachineShell(transport)

        async def respond():
            await asyncio.sleep(0.05)
            sent = json.loads(ws.sent[0])
            ws.inject({"id": sent["id"], "data": {"stdout": "", "stderr": "", "code": 0}})

        asyncio.create_task(respond())
        listener = asyncio.create_task(transport.listen())

        await shell.execute("pwd", cwd="/root/brain")
        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["params"]["cwd"], "/root/brain")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass


class TestMachineFilesystem(unittest.IsolatedAsyncioTestCase):
    """Test the MachineFilesystem sub-interface."""

    def _setup(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)
        fs = MachineFilesystem(transport)
        return ws, transport, fs

    async def _respond(self, ws, data):
        await asyncio.sleep(0.05)
        sent = json.loads(ws.sent[-1])
        ws.inject({"id": sent["id"], "data": data})

    async def test_list(self):
        ws, transport, fs = self._setup()
        items = [
            {"name": "docs", "path": "~/docs", "kind": "folder", "size": 0, "modified": 0},
            {"name": "file.txt", "path": "~/file.txt", "kind": "file", "size": 100, "modified": 0},
        ]

        asyncio.create_task(self._respond(ws, {"data": items}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.list("~")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "docs")

        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "inodes.list")
        self.assertEqual(sent["params"]["path"], "~")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_stat(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {
            "name": "file.txt",
            "path": "/root/file.txt",
            "kind": "file",
            "size": 42,
            "modified": 1700000000,
        }))
        listener = asyncio.create_task(transport.listen())

        result = await fs.stat("/root/file.txt")
        self.assertEqual(result["size"], 42)

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_write(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {"ok": True}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.write("/root/test.txt", "hello world")
        self.assertTrue(result["ok"])

        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "inodes.put")
        self.assertEqual(sent["params"]["data"], "hello world")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_mkdir(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {"ok": True}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.mkdir("/root/newdir")
        self.assertTrue(result["ok"])

        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "inodes.mkdir")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_delete(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {"ok": True}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.delete("/root/oldfile.txt")
        self.assertTrue(result["ok"])

        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "inodes.delete")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_move(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {"ok": True}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.move("/root/a.txt", "/root/b.txt")
        self.assertTrue(result["ok"])

        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "inodes.move")
        self.assertEqual(sent["params"]["from"], "/root/a.txt")
        self.assertEqual(sent["params"]["to"], "/root/b.txt")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_copy(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {"ok": True}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.copy("/root/a.txt", "/root/a_copy.txt")
        self.assertTrue(result["ok"])

        sent = json.loads(ws.sent[0])
        self.assertEqual(sent["method"], "inodes.copy")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass

    async def test_search(self):
        ws, transport, fs = self._setup()

        asyncio.create_task(self._respond(ws, {"data": [
            {"name": "match.py", "path": "/root/match.py", "kind": "file", "size": 0, "modified": 0},
        ]}))
        listener = asyncio.create_task(transport.listen())

        result = await fs.search("match")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "match.py")

        listener.cancel()
        try:
            await listener
        except asyncio.CancelledError:
            pass


class TestMachineConnection(unittest.IsolatedAsyncioTestCase):
    """Test the MachineConnection context manager."""

    async def test_context_manager_closes(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)
        conn = MachineConnection("mch_test", transport)

        self.assertEqual(conn.id, "mch_test")
        self.assertIsInstance(conn.shell, MachineShell)
        self.assertIsInstance(conn.filesystem, MachineFilesystem)

        async with conn:
            pass

        self.assertTrue(ws.closed)

    async def test_has_shell_and_filesystem(self):
        ws = FakeWebSocket()
        transport = WebSocketTransport(ws)
        conn = MachineConnection("mch_test", transport)

        self.assertIsNotNone(conn.shell)
        self.assertIsNotNone(conn.filesystem)


class TestMachinesConnectMethod(unittest.IsolatedAsyncioTestCase):
    """Test the Machines.connect() method builds correct WS URL."""

    @patch("layerbrain.sdk.resources.machines.websockets")
    async def test_connect_builds_wss_url(self, mock_ws_module):
        mock_ws = FakeWebSocket()
        mock_ws_module.connect = AsyncMock(return_value=mock_ws)

        from layerbrain.sdk.resources.machines import Machines

        mock_client = MagicMock()
        mock_client._base_url = "https://api.layerbrain.com"
        mock_client._api_key = "sk-test"
        machines = Machines.__new__(Machines)
        machines._client = mock_client

        conn = await Machines.connect.__wrapped__(machines, "mch_123")

        mock_ws_module.connect.assert_called_once()
        call_args = mock_ws_module.connect.call_args
        self.assertEqual(
            call_args[0][0],
            "wss://api.layerbrain.com/v1/machines/mch_123",
        )
        self.assertEqual(
            call_args[1]["additional_headers"]["Authorization"],
            "Bearer sk-test",
        )
        self.assertEqual(
            call_args[1]["additional_headers"]["x-layerbrain-source"],
            "api",
        )

        await conn.close()

    @patch("layerbrain.sdk.resources.machines.websockets")
    async def test_connect_http_to_ws(self, mock_ws_module):
        mock_ws = FakeWebSocket()
        mock_ws_module.connect = AsyncMock(return_value=mock_ws)

        from layerbrain.sdk.resources.machines import Machines

        mock_client = MagicMock()
        mock_client._base_url = "http://localhost:8000"
        mock_client._api_key = "sk-local"
        machines = Machines.__new__(Machines)
        machines._client = mock_client

        conn = await Machines.connect.__wrapped__(machines, "mch_local")

        call_args = mock_ws_module.connect.call_args
        self.assertEqual(
            call_args[0][0],
            "ws://localhost:8000/v1/machines/mch_local",
        )

        await conn.close()


class TestBaseUrlV1Stripping(unittest.TestCase):
    """Test that base_url /v1 suffix is stripped to prevent double /v1/v1."""

    def test_strips_v1_suffix(self):
        from layerbrain.sdk._client import _BaseClient

        with patch("layerbrain.sdk._client.Config") as MockConfig:
            config_instance = MockConfig.return_value
            config_instance.api_key = "sk-test"
            config_instance.base_url = "https://api.layerbrain.com/v1"

            client = _BaseClient()
            self.assertEqual(client._base_url, "https://api.layerbrain.com")

    def test_no_strip_without_v1(self):
        from layerbrain.sdk._client import _BaseClient

        with patch("layerbrain.sdk._client.Config") as MockConfig:
            config_instance = MockConfig.return_value
            config_instance.api_key = "sk-test"
            config_instance.base_url = "https://api.layerbrain.com"

            client = _BaseClient()
            self.assertEqual(client._base_url, "https://api.layerbrain.com")


if __name__ == "__main__":
    unittest.main()
