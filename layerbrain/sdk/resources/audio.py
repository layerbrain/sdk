from __future__ import annotations

from typing import Any

from .._resource import Resource


class Audio(Resource):
    """Audio API resource (auto-generated)."""

    async def speech(self, **kwargs: Any) -> dict:
        """Create text-to-speech generation."""
        return await self._post("/audio/speech", json=kwargs)

    async def transcriptions(self, **kwargs: Any) -> dict:
        """Create speech-to-text transcription."""
        return await self._post("/audio/transcriptions", json=kwargs)
