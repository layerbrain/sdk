"""Live machine session with shell and filesystem sub-interfaces.

Usage:
    client = Layerbrain()
    async with client.machines.connect("mch_abc123") as machine:
        # Shell
        result = await machine.shell.execute("ls -la")
        print(result["stdout"])

        # Filesystem
        items = await machine.filesystem.list("~/brain")
        for item in items:
            print(item["name"], item["kind"])
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from ._transport import WebSocketTransport


class MachineShell:
    """Shell command execution inside a live machine session."""

    def __init__(self, transport: WebSocketTransport) -> None:
        self._transport = transport

    async def execute(self, command: str, cwd: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
        """Execute a shell command.

        Returns:
            Dict with stdout, stderr, code.
        """
        params: Dict[str, Any] = {"command": command, "timeout": timeout}
        if cwd:
            params["cwd"] = cwd
        return await self._transport.send("shell.execute", params, timeout=float(timeout) + 5)


class MachineFilesystem:
    """Filesystem operations inside a live machine session (maps to inodes.* methods)."""

    def __init__(self, transport: WebSocketTransport) -> None:
        self._transport = transport

    async def list(self, path: str = "~", show_all: bool = False) -> list:
        """List directory contents.

        Returns:
            List of dicts with name, path, kind, size, modified.
        """
        result = await self._transport.send("inodes.list", {"path": path, "all": show_all})
        return result.get("data", [])

    async def stat(self, path: str) -> Dict[str, Any]:
        """Get file/folder metadata."""
        return await self._transport.send("inodes.stat", {"path": path})

    async def read(self, path: str) -> Dict[str, Any]:
        """Read file content (base64 encoded).

        Returns:
            Dict with data (base64 string) and encoding.
        """
        return await self._transport.send("inodes.get", {"path": path})

    async def write(self, path: str, data: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Write file content."""
        return await self._transport.send("inodes.put", {
            "path": path,
            "data": data,
            "encoding": encoding,
        })

    async def mkdir(self, path: str) -> Dict[str, Any]:
        """Create directory (recursive)."""
        return await self._transport.send("inodes.mkdir", {"path": path})

    async def delete(self, path: str) -> Dict[str, Any]:
        """Delete file or directory."""
        return await self._transport.send("inodes.delete", {"path": path})

    async def move(self, src: str, dst: str) -> Dict[str, Any]:
        """Move/rename file or directory."""
        return await self._transport.send("inodes.move", {"from": src, "to": dst})

    async def copy(self, src: str, dst: str) -> Dict[str, Any]:
        """Copy file or directory."""
        return await self._transport.send("inodes.copy", {"from": src, "to": dst})

    async def search(self, pattern: str, path: str = "~/brain", limit: int = 50) -> list:
        """Search files by name pattern.

        Returns:
            List of matching file dicts.
        """
        result = await self._transport.send("inodes.search", {
            "pattern": pattern,
            "path": path,
            "limit": limit,
        })
        return result.get("data", [])

    async def recents(self, path: str = "~/brain", limit: int = 20, days: int = 7) -> list:
        """Get recently modified files.

        Returns:
            List of recently modified file dicts.
        """
        result = await self._transport.send("inodes.recents", {
            "path": path,
            "limit": limit,
            "days": days,
        })
        return result.get("data", [])


class MachineConnection:
    """A live WebSocket connection to a machine.

    Provides .shell and .filesystem sub-interfaces for interacting
    with the machine.
    """

    def __init__(self, machine_id: str, transport: WebSocketTransport) -> None:
        self.id = machine_id
        self._transport = transport
        self._listener_task: Optional[asyncio.Task] = None
        self.shell = MachineShell(transport)
        self.filesystem = MachineFilesystem(transport)

    async def _start_listener(self) -> None:
        """Start the background WebSocket listener."""
        self._listener_task = asyncio.create_task(self._transport.listen())

    async def close(self) -> None:
        """Close the connection."""
        if self._listener_task:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
        await self._transport.close()

    async def __aenter__(self) -> MachineConnection:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
