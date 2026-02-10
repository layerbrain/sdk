"""Base resource class with auto sync/async detection.

Resource methods are written as ``async def``. The ``__init_subclass__`` hook
automatically wraps public async methods with ``_auto``, which detects at
call time whether there is a running event loop:

- Running loop: returns the coroutine (caller uses ``await``).
- No loop: runs the coroutine synchronously via ``asyncio.run()``.
"""

from __future__ import annotations

import asyncio
import functools
import inspect
from typing import Any, Dict, Optional


def _auto(fn):
    """Make an async method callable from both sync and async contexts."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        coro = fn(*args, **kwargs)
        try:
            asyncio.get_running_loop()
            return coro  # caller awaits
        except RuntimeError:
            return asyncio.run(coro)  # run synchronously
    return wrapper


class Resource:
    """Base class for all SDK resources.

    Subclass public ``async def`` methods are automatically wrapped by
    ``_auto`` via ``__init_subclass__``, so callers can use them with or
    without ``await`` depending on context.
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for name in list(vars(cls)):
            method = vars(cls)[name]
            if inspect.iscoroutinefunction(method) and not name.startswith("_"):
                setattr(cls, name, _auto(method))

    async def _get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # Strip None values so we don't send ?key=None to the API
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
            if not params:
                params = None
        result = self._client._get(path, params=params)
        if inspect.isawaitable(result):
            return await result
        return result

    async def _post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        result = self._client._post(path, json=json)
        if inspect.isawaitable(result):
            return await result
        return result

    async def _patch(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        result = self._client._patch(path, json=json)
        if inspect.isawaitable(result):
            return await result
        return result

    async def _put(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        result = self._client._put(path, json=json)
        if inspect.isawaitable(result):
            return await result
        return result

    async def _delete(self, path: str) -> Dict[str, Any]:
        result = self._client._delete(path)
        if inspect.isawaitable(result):
            return await result
        return result
