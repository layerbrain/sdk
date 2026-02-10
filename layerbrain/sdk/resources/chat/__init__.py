"""Chat resource with completions sub-resource."""

from __future__ import annotations

from typing import Any

from .completions import Completions, Stream


class Chat:
    """Chat resource. Access completions via ``chat.completions``."""

    def __init__(self, client: Any) -> None:
        self.completions = Completions(client)


__all__ = ["Chat", "Completions", "Stream"]
