"""Webhooks resource (hand-written).

Provides standard webhook CRUD helpers plus listener request construction
for the CLI's websocket event stream.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence
from urllib.parse import urlencode

from .._pagination import SyncPage
from .._resource import Resource


class Webhooks(Resource):
    """Webhooks resource with CRUD operations and listen URL helpers."""

    async def list(self) -> SyncPage:
        """List webhooks for the authenticated organization."""
        data = await self._get("/webhooks", params=None)
        return SyncPage(
            data=data.get("data", []),
            has_more=data.get("has_more", False),
            client=self._client,
            path="/webhooks",
        )

    async def create(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a webhook endpoint."""
        return await self._post("/webhooks", json=kwargs)

    async def retrieve(self, webhook_id: str) -> Dict[str, Any]:
        """Retrieve a webhook by ID."""
        return await self._get(f"/webhooks/{webhook_id}", params=None)

    async def update(self, webhook_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Update a webhook by ID."""
        return await self._patch(f"/webhooks/{webhook_id}", json=kwargs)

    async def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook by ID."""
        return await self._delete(f"/webhooks/{webhook_id}")

    async def rotate_secret(self, webhook_id: str) -> Dict[str, Any]:
        """Rotate the signing secret for a webhook."""
        return await self._post(f"/webhooks/{webhook_id}/rotate-secret", json={})

    def listen_request(
        self,
        *,
        events: Optional[Sequence[str] | str] = None,
    ) -> tuple[str, dict[str, str]]:
        """Build the websocket listener request for live webhook events."""
        base_url = self._client._base_url
        if base_url.startswith("https://"):
            ws_url = "wss://" + base_url[8:]
        elif base_url.startswith("http://"):
            ws_url = "ws://" + base_url[7:]
        else:
            ws_url = "wss://" + base_url

        query = ""
        if isinstance(events, str):
            raw_events = events.strip()
        elif events:
            raw_events = ",".join(str(event).strip() for event in events if str(event).strip())
        else:
            raw_events = ""
        if raw_events:
            query = "?" + urlencode({"events": raw_events})

        headers: dict[str, str] = {"x-layerbrain-source": "api"}
        if self._client._api_key:
            headers["Authorization"] = f"Bearer {self._client._api_key}"

        return f"{ws_url}/v1/webhooks{query}", headers
