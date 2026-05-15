"""WebSocket transport for live machine sessions.

Implements the JSON-RPC style protocol used by /v1/machines/{id}:
- Request: {id, method, body}
- Response: {id, data} or {id, error: {type, message}}
- Events: {event, data}
"""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any, Callable, Dict


class WebSocketTransport:
    """WebSocket transport for communicating with a live machine session."""

    def __init__(self, ws: Any) -> None:
        self._ws = ws
        self._pending: Dict[str, asyncio.Future] = {}
        self._event_handlers: Dict[str, Callable] = {}

    async def send(self, method: str, body: Dict[str, Any], timeout: float = 30.0) -> Any:
        """Send a request and wait for the response."""
        request_id = str(uuid.uuid4())
        future: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending[request_id] = future

        await self._ws.send(json.dumps({
            "id": request_id,
            "method": method,
            "body": body,
        }))

        try:
            return await asyncio.wait_for(future, timeout=timeout)
        finally:
            self._pending.pop(request_id, None)

    async def emit(self, method: str, body: Dict[str, Any]) -> None:
        """Fire-and-forget message (no response expected)."""
        await self._ws.send(json.dumps({
            "method": method,
            "body": body,
        }))

    def _handle_message(self, raw: str) -> None:
        """Route an incoming message to the correct pending future or event handler."""
        msg = json.loads(raw)

        # Response to a pending request
        request_id = msg.get("id")
        if request_id and request_id in self._pending:
            future = self._pending.pop(request_id)
            if "error" in msg:
                error = msg["error"]
                future.set_exception(
                    MachineError(error.get("type", "error"), error.get("message", str(error)))
                )
            else:
                future.set_result(msg.get("data"))
            return

        # Server-initiated event
        event = msg.get("event")
        if event and event in self._event_handlers:
            self._event_handlers[event](msg.get("data"))

    async def listen(self) -> None:
        """Read messages from the WebSocket and dispatch them."""
        async for raw in self._ws:
            self._handle_message(raw)

    async def close(self) -> None:
        """Close the WebSocket connection."""
        await self._ws.close()


class MachineError(Exception):
    """Error returned from a machine operation."""

    def __init__(self, error_type: str, message: str) -> None:
        self.error_type = error_type
        self.message = message
        super().__init__(f"{error_type}: {message}")
