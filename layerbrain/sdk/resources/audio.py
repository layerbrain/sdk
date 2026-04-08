from __future__ import annotations

from typing import Any

from .._resource import Resource


class Audio(Resource):
    """Audio API resource (auto-generated)."""

    async def create_speech(self, **kwargs: Any) -> dict:
        """Post create_speech"""
        return await self._post("/audio/speech", json=kwargs)

    async def create_transcription(self, **kwargs: Any) -> dict:
        """Post create_transcription"""
        return await self._post("/audio/transcriptions", json=kwargs)
