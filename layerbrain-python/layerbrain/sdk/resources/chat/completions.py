"""Chat completions resource.

One class. Streaming returns a ``Stream`` object that supports both
``for chunk in stream`` (sync) and ``async for chunk in stream`` (async).
"""

from __future__ import annotations

import json as json_lib
from typing import Any, Dict, List, Union

from ..._types import ChatCompletion, ChatCompletionChunk
from ..._resource import Resource


class Stream:
    """Dual-mode streaming iterator for chat completion chunks.

    Wraps the raw SSE data iterator from either SyncHTTPClient or
    AsyncHTTPClient and parses each line into a ChatCompletionChunk.

    Sync:  ``for chunk in stream: ...``
    Async: ``async for chunk in stream: ...``
    """

    def __init__(self, raw) -> None:
        self._raw = raw

    def __iter__(self):
        for data in self._raw:
            yield ChatCompletionChunk(**json_lib.loads(data))

    async def __aiter__(self):
        async for data in self._raw:
            yield ChatCompletionChunk(**json_lib.loads(data))


class Completions(Resource):
    """Chat completions. Works in both sync and async contexts.

    Non-streaming returns a ``ChatCompletion``.
    Streaming returns a ``Stream`` iterable of ``ChatCompletionChunk``.
    """

    async def create(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[ChatCompletion, Stream]:
        body: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs,
        }
        if stream:
            raw = self._client._stream_sse("/chat/completions", json=body)
            return Stream(raw)
        response = await self._post("/chat/completions", json=body)
        return ChatCompletion(**response)
