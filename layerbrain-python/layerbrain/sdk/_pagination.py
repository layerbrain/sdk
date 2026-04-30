"""Auto-pagination iterator for list endpoints.

Usage:
    for machine in client.machines.list():
        print(machine["id"])

    # Or collect all at once
    all_machines = list(client.machines.list())
"""

from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List, Optional


class SyncPage:
    """Synchronous paginated iterator over API list responses."""

    def __init__(
        self,
        *,
        data: List[Dict[str, Any]],
        has_more: bool,
        client: Any,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._data = data
        self._has_more = has_more
        self._client = client
        self._path = path
        self._params = params or {}
        self._page = self._params.get("page", 1)

    @property
    def data(self) -> List[Dict[str, Any]]:
        return self._data

    @property
    def has_more(self) -> bool:
        return self._has_more

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        yield from self._data

    def __len__(self) -> int:
        return len(self._data)

    def next_page(self) -> SyncPage:
        """Fetch the next page of results."""
        self._page += 1
        params = {**self._params, "page": self._page}
        response = self._client._get(self._path, params=params)
        return SyncPage(
            data=response.get("data", []),
            has_more=response.get("has_more", False),
            client=self._client,
            path=self._path,
            params=params,
        )

    def auto_paging_iter(self) -> Iterator[Dict[str, Any]]:
        """Iterate through all pages automatically."""
        page = self
        while True:
            yield from page.data
            if not page.has_more:
                break
            page = page.next_page()


class AsyncPage:
    """Asynchronous paginated iterator over API list responses."""

    def __init__(
        self,
        *,
        data: List[Dict[str, Any]],
        has_more: bool,
        client: Any,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._data = data
        self._has_more = has_more
        self._client = client
        self._path = path
        self._params = params or {}
        self._page = self._params.get("page", 1)

    @property
    def data(self) -> List[Dict[str, Any]]:
        return self._data

    @property
    def has_more(self) -> bool:
        return self._has_more

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        yield from self._data

    def __len__(self) -> int:
        return len(self._data)

    async def next_page(self) -> AsyncPage:
        """Fetch the next page of results."""
        self._page += 1
        params = {**self._params, "page": self._page}
        response = await self._client._get(self._path, params=params)
        return AsyncPage(
            data=response.get("data", []),
            has_more=response.get("has_more", False),
            client=self._client,
            path=self._path,
            params=params,
        )

    async def auto_paging_iter(self) -> AsyncIterator[Dict[str, Any]]:
        """Iterate through all pages automatically."""
        page = self
        while True:
            for item in page.data:
                yield item
            if not page.has_more:
                break
            page = await page.next_page()
